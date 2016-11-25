#include "monitor.h"

// ----------------------------------------------------------------------------
//
// ----------------------------------------------------------------------------

Monitor::Monitor() {
    p_status = new Status();
    pid = 0;
    p_args = NULL;
    p_full = NULL;
}

// ----------------------------------------------------------------------------
//
// ----------------------------------------------------------------------------

Monitor::~Monitor() {
    if (pid != 0) {
        terminate();
    }
}

// ----------------------------------------------------------------------------
// Get the command name from the first argument. The result will be used as
// the second argument for exec...()
//
// Returns:
//   - Pointer to the original string if no "/" character found in string
//   - NULL if the original string was NULL or was shorter than 1 byte
//
//   Otherwise, returns the command name extracted from the original string.
//
// ----------------------------------------------------------------------------

char *Monitor::getCommandName(char *str) {
    if (str == NULL || strlen(str) < 1) return(NULL);
    if (strchr(str, 0x2F) == NULL) return(str);

    char *temp = NULL;

    char *t = strtok(str, "/");
    if (t != NULL) temp = t;
    while(t) {
        t = strtok(NULL, "/");
        if (t != NULL) temp = t;
    }
    return(temp);
}

// ----------------------------------------------------------------------------
// Parse a command line where arguments are separated by space. After parsing
// an array of string pointers is returned where each item in the array points
// to an argument string. The last item in the array is always NULL.
//
// Returns:
//
//  - NULL if the original string is NULL or the length of the string is less
//    than 1.
//
//  Otherwise, it returns an array of string pointers.
//
// ----------------------------------------------------------------------------

char **Monitor::parseArgs(char *str) {
    if (str == NULL || strlen(str) < 1) return(NULL);

    char **res = NULL;
    int n_spaces = 0;
    int i = 0;

    char *p = strtok(str, " ");

    while(p) {
        res = (char **)realloc(res, sizeof(char*) * ++n_spaces);
        if (res == NULL) exit(-1);
        res[n_spaces-1] = p;
        p = strtok(NULL, " ");
    }

    res = (char **)realloc(res, sizeof(char*) * (n_spaces+1));
    res[n_spaces] = 0;

    return(res);
}

// ----------------------------------------------------------------------------
//
// ----------------------------------------------------------------------------

int Monitor::setTarget(char *cmd_line) {
    if (p_args != NULL) free(p_args);
    p_full = NULL;
    
    p_args = Monitor::parseArgs((char *)cmd_line);
    if (p_args == NULL) return(1);
    
    if (p_args != NULL && p_args[0] != NULL) {
        p_full = (char *)malloc(strlen((char *)p_args[0]) + 1);
        memset(p_full, 0x00, strlen((char *)p_args[0]) + 1);
        strcpy(p_full, p_args[0]);
        p_args[0] = getCommandName(p_args[0]);
    }
    if (p_args[0] == NULL) return(1);
    return(0);
}

// ----------------------------------------------------------------------------
//
// ----------------------------------------------------------------------------

int Monitor::terminate() {
    if (pid < 1) return 1;
    int rc = 0;
    int error;

    // If we attached to a live process, detach from it.
    if (do_attach) {
        syslog(LOG_INFO, "detaching from process: %d", pid);
        if (ptrace(PTRACE_DETACH, pid, NULL, SIGSTOP) == -1) {
            rc = 0;
            syslog(LOG_ERR, "failed to detach from process: %d", pid);
        } else {
            rc = 1;
        }
    }

    // If we started the process or failed to detach from it, kill it.
    if (!do_attach || rc == 0) {
        syslog(LOG_INFO, "killing process: %d", pid);
        if (kill(pid, SIGKILL) == -1) {
            error = errno;
            if (error == EINVAL || error == EPERM) rc = 0;
            if (error == ESRCH) rc = 1;         // Even if it is considered as
                                                 // an error that the process
                                                 // does not exist, this is how
                                                 // we report that we got rid
                                                 // of it anyway. So, this is
                                                 // good for us.
        } else {
            rc = 1;
        }
    } else {
        rc = 1;
    }

    if (rc == 0) syslog(LOG_ERR, "failed to kill process: %d", pid);
    p_status->reset();
    pid = 0;
    return(rc);
}

// ----------------------------------------------------------------------------
//
// ----------------------------------------------------------------------------

Status *Monitor::status() {
    return p_status;
}

// ----------------------------------------------------------------------------
//
// ----------------------------------------------------------------------------

void Monitor::stop() {
    running = 0;
}

// ----------------------------------------------------------------------------
//
// ----------------------------------------------------------------------------

int Monitor::isRunning() {
    return(running);
}

// ----------------------------------------------------------------------------
//
// ----------------------------------------------------------------------------

int Monitor::start() {
    running = 1;
    int status = 0;
    pid_t child = 0;

    // XXX HORRIBLE HACK OF DEATH
    if (p_args[0] != NULL && p_args[0][0] == 0) {
        free(p_args[0]);
        p_args[0] = p_full;
    }

    p_status->reset();
    syslog(LOG_INFO, "starting process: %s (%s)", p_full, p_args[0]);

    // Look for a live process first
    char cmdline[256];
    int x = 0;
    int y = 0;
    memset(cmdline, 0, sizeof(cmdline));
    strncpy(cmdline, p_args[0], sizeof(cmdline) - 1);
    while (p_args[x] != NULL) {
        y += strlen( & cmdline[y] ) + 1;
        cmdline[y] = 0;
        strncpy(&cmdline[y], p_args[x], sizeof(cmdline) - y - 1);
        x++;
    }

    do_attach = false;
    DIR *proc = opendir("/proc");
    if (proc != NULL) {
        while (1) {
            dirent * entry = readdir(proc);
            if (entry == NULL) break;
            pid_t cur_pid = atoi(entry->d_name);
            if (cur_pid == 0) continue;
            int i_tmp = strlen(entry->d_name) + 16;
            char *p_tmp = (char *) malloc(i_tmp);
            if (p_tmp != NULL) {
                p_tmp[0] = 0;
                snprintf(p_tmp, i_tmp - 1, "/proc/%s/cmdline", entry->d_name);
                FILE *file = fopen(p_tmp, "r");
                if (file != NULL) {
                    char tmpbuf[256];
                    memset(tmpbuf, 0, sizeof(tmpbuf));
                    fread(tmpbuf, 1, sizeof(tmpbuf) - 1, file);
                    fclose(file);
                    if (strcmp(tmpbuf, (char *) cmdline) == 0) {
                        syslog(LOG_INFO, "found live process already, PID: %d", cur_pid);
                        child = cur_pid;
                        do_attach = true;
                        break;
                    }
                } else {
                    syslog(LOG_ERR, "failed to open file: %s (%d)", p_tmp, errno);
                }
            } else {
                syslog(LOG_ERR, "failed to allocate memory: %d", errno);
            }
        }
        closedir(proc);
    } else {
        syslog(LOG_ERR, "failed to scan for live processes: %d", errno);
    }

    // At this point either we found the child process (no forking is needed)
    // or we didn't (then we fork and execute, to get a child process)
    if (child == 0) child = fork();
    if (child == 0) {
        if (p_full != NULL && p_args != NULL && p_args[0] != NULL) {
            ptrace(PTRACE_TRACEME, 0, NULL, NULL);
            p_status->setState(P_RUNNING);
            execv(p_full, p_args);
            p_status->setPid(-1);
            p_status->setState(P_ERROR);
            syslog(LOG_ERR, "failed to start process: %d", errno);
        } else {
            p_status->setPid(-1);
            p_status->setState(P_ERROR);
        }
    } else {
        pid = child;
        if (do_attach) {
            if (ptrace(PTRACE_ATTACH, child, NULL, NULL) == -1) {
                syslog(LOG_ERR, "failed to attach to process: %d", errno);
                p_status->setPid(-1);
                p_status->setState(P_ERROR);
                syslog(LOG_INFO, "monitor for %s stopped", p_full);
                return 0;
            }
        }

        wait(NULL);
        ptrace(PTRACE_CONT, child, NULL, NULL);
        syslog(LOG_INFO, "process started with pid: %d", child);
        p_status->setPid(child);
        while(running) {
            wait(&status);
            if (WIFEXITED(status)) {
                p_status->setState(P_TERM);
                p_status->setExitCode(WEXITSTATUS(status));
                syslog(LOG_INFO, "process exited with exit code: %d",
                        WEXITSTATUS(status));
                break;
            }
            if (WIFSIGNALED(status)) {
                p_status->setState(P_SIGTERM);
                p_status->setSignal(WTERMSIG(status));
                syslog(LOG_INFO, "process terminated by signal: %d",
                        WTERMSIG(status));
                break;
            }
            if (WIFSTOPPED(status)) {
                p_status->setState(P_TERM);
                p_status->setSignal(WSTOPSIG(status));
                syslog(LOG_INFO, "process stopped by signal: %d",
                        WSTOPSIG(status));
                break;
            }
        }
        syslog(LOG_INFO, "monitor for %s stopped", p_full);
    }
}
