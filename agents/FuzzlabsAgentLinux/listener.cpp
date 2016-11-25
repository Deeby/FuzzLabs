#include "listener.h"
#include "connection.h"

// ----------------------------------------------------------------------------
//
// ----------------------------------------------------------------------------

static void *start_monitor(void *m) {
    Monitor *monitor = (Monitor *)m;
    monitor->start();
}

// ----------------------------------------------------------------------------
//
// ----------------------------------------------------------------------------

cJSON *createRegisterObject(char *reg_name, unsigned long long int value) {
    char *reg_str = (char *)malloc(64);
    memset(reg_str, 0x00, 64);    
    sprintf(reg_str, "0x%X", value);
    
    cJSON *r_obj = cJSON_CreateObject();  
    cJSON_AddStringToObject(r_obj, "register", reg_name);
    cJSON_AddStringToObject(r_obj, "value", reg_str);
    
    free(reg_str);
    return r_obj;
}

// ----------------------------------------------------------------------------
//
// ----------------------------------------------------------------------------

int handle_command_kill(Connection *conn, Monitor *monitor) {
    if (monitor != NULL) {
        if (monitor->terminate()) {
            conn->transmit("{\"command\": \"kill\", \"data\": \"success\"}", 38);
        } else {
            conn->transmit("{\"command\": \"kill\", \"data\": \"failed\"}", 37);
        }
    } else {
        conn->transmit("{\"command\": \"kill\", \"data\": \"failed\"}", 37);
    }
    return(0);
}

// ----------------------------------------------------------------------------
//
// ----------------------------------------------------------------------------

int handle_command_ping(Connection *conn) {
    conn->transmit("{\"command\": \"ping\", \"data\": \"pong\"}", 35);
    return(0);
}

// ----------------------------------------------------------------------------
//
// ----------------------------------------------------------------------------

int handle_command_status(Connection *conn, Monitor *monitor) {
    if (monitor == NULL || monitor->isRunning() == 0) {
        conn->transmit("{\"command\": \"status\", \"data\": \"OK\"}", 35);
        return(0);
    }
    Status *m_status = monitor->status();
    
    if (m_status->getPid() < 1 || 
        m_status->getState() <= P_RUNNING) {
        conn->transmit("{\"command\": \"status\", \"data\": \"OK\"}", 35);
        return(0);
    }
    
    cJSON *j_data = cJSON_CreateObject();

    cJSON_AddStringToObject(j_data, "status", "terminated");
    cJSON_AddNumberToObject(j_data, "process_id", m_status->getPid());
    cJSON_AddNumberToObject(j_data, "term_condition", m_status->getState());
    cJSON_AddNumberToObject(j_data, "exit_code", m_status->getExitCode());
    cJSON_AddNumberToObject(j_data, "signal_num", m_status->getSignalNum());
    char *signame = (char *)malloc(256);
    m_status->getSignalStr(signame, 256);
    cJSON_AddStringToObject(j_data, "signal_str", signame);

    cJSON *root = cJSON_CreateObject();
    cJSON_AddStringToObject(root, "command", "status");
    cJSON_AddItemToObject(root, "data", j_data);
    
    char *t_json = cJSON_Print(root);
    if (t_json != NULL) conn->transmit(t_json, strlen(t_json));
    
    cJSON_Delete(root);
    free(signame);
    monitor->terminate();
    monitor->stop();
    return(1);
}

// ----------------------------------------------------------------------------
//
// ----------------------------------------------------------------------------

int handle_command_start(Connection *conn, Monitor *monitor, char *data) {
    pthread_t tid;
    
    if (data == NULL) {
        syslog(LOG_ERR, "[%s]: target not specified in data", 
                conn->address());
        conn->transmit("{\"command\": \"start\", \"data\": \"failed\"}", 38);
        return(0);
    }
    
    if (monitor->setTarget(data)) {
        syslog(LOG_ERR, "[%s]: monitor failed to process command line", 
                conn->address());
        conn->transmit("{\"command\": \"start\", \"data\": \"failed\"}", 38);
        return(0);
    }

    if (pthread_create(&tid, NULL, &start_monitor, monitor) != 0) {
        syslog(LOG_ERR, "[%s]: monitor failed to start process", 
                conn->address());
        conn->transmit("{\"command\": \"start\", \"data\": \"failed\"}", 38);
        return(0);
    }
    conn->transmit("{\"command\": \"start\", \"data\": \"success\"}", 39);
    return(1);
}

// ----------------------------------------------------------------------------
//
// ----------------------------------------------------------------------------

void process_command(Connection *conn, Monitor *monitor, char *data) {
    cJSON *json = cJSON_Parse(data);
    if (json == NULL) return;
    char *cmd = cJSON_GetObjectItem(json, "command")->valuestring;
    if (cmd == NULL) return;
    
    syslog(LOG_INFO, "command received from %s: %s", conn->address(), cmd);
    
    if (!strcmp(cmd, "ping")) {
        handle_command_ping(conn);
    } else if (!strcmp(cmd, "kill")) {
        handle_command_kill(conn, monitor);
    } else if (!strcmp(cmd, "start")) {
        handle_command_start(conn, monitor, 
                cJSON_GetObjectItem(json, "data")->valuestring);
    } else if (!strcmp(cmd, "status")) {
        handle_command_status(conn, monitor);
    }
    
    if (json != NULL) cJSON_Delete(json);
}

// ----------------------------------------------------------------------------
//
// ----------------------------------------------------------------------------

static void *handle_connection(void *c) {
    size_t r_len = 1;
    Monitor *monitor = new Monitor();
    Connection *conn = (Connection *)c;
    char *data = NULL;
    
    syslog(LOG_INFO, "accepted connection from engine: %s", conn->address());

    while(r_len != 0) {
        try {
            data = conn->receive(data);
            if (r_len < 1 || data == NULL) continue;
            process_command(conn, monitor, data);
            free(data);
            data = NULL;
        } catch(char const* ex) {
            syslog(LOG_ERR, "%s", ex);
            continue;
        }
    }

    syslog(LOG_INFO, "disconnected from engine: %s", conn->address());

    if (monitor != NULL) {
        monitor->terminate();
        monitor->stop();
        delete monitor;
    }
    conn->terminate();
    delete conn;
}

// ----------------------------------------------------------------------------
//
// ----------------------------------------------------------------------------

void listener(unsigned int port, unsigned int max_conn) {
    int sd, n_sd;
    socklen_t c_len;
    struct sockaddr_in s_addr, c_addr;
    unsigned int running = 1;
    pthread_t tid[max_conn];

    sd = socket(AF_INET, SOCK_STREAM, 0);
    if (sd < 0) throw "failed to create socket for listener";

    bzero((char *) &s_addr, sizeof(s_addr));
    s_addr.sin_family = AF_INET;
    s_addr.sin_addr.s_addr = INADDR_ANY;
    s_addr.sin_port = htons(port);
    if (bind(sd, (struct sockaddr *) &s_addr, sizeof(s_addr)) < 0) 
        throw "failed to bind listener to address";

    if (listen(sd, max_conn) != 0) throw "failed to set up listener";
    c_len = sizeof(c_addr);

    while (running) {
        n_sd = accept(sd, (struct sockaddr *) &c_addr, &c_len);
        if (n_sd < 0) continue;
        Connection *conn = new Connection(n_sd, &c_addr);
        if (pthread_create(&(tid[0]), NULL, &handle_connection, conn) != 0)
            throw "failed to accept connection";
    }
}
