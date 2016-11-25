import time
import syslog
import platform

# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

class Logger:

    def __init__(self):
        pass

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def log(self, message, type = None, exception = None, worker_id = None,
            job_id = None, scenario_name = None, unit_name = None, 
            primitive_name = None):
        fmt_msg = []
        if worker_id:
            fmt_msg.append("worker:" + str(worker_id))
            if job_id:
                fmt_msg.append("job:" + str(job_id))
                if scenario_name:
                    fmt_msg.append("scenario:" + str(scenario_name))
                    if unit_name:
                        fmt_msg.append("unit:" + str(unit_name))
                        if primitive_name:
                            fmt_msg.append("primitive:" + str(primitive_name))
        fmt_msg = "/".join(fmt_msg)
        fmt_msg += ": %s" % str(message)
        if exception:
            fmt_msg += " (%s)" % str(exception)

        if type == "debug":
            type = syslog.LOG_DEBUG
        elif type == "info":
            type = syslog.LOG_INFO
        elif type == "warning":
            type = syslog.LOG_WARNING
        elif type == "error":
            type = syslog.LOG_ERR
        else:
            type = syslog.LOG_INFO

        # This is so at least we see something on MacOSX
        if platform.system() == "Darwin":
            type = syslog.LOG_ALERT

        # TODO: remove later
        print fmt_msg

        syslog.syslog(type, fmt_msg)
        return fmt_msg

