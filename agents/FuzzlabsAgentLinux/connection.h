/* 
 * File:   connection.h
 * Author: keyman
 *
 * Created on 14 August 2015, 14:18
 */

#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <errno.h>

#include <syslog.h>

#ifndef CONNECTION_H
#define	CONNECTION_H

#define RECV_BUFFER_SIZE    1024    // In KB
#define RECV_MAX_MSG_SIZE   4       // In MB

class Connection {
private:
    int sock;
    struct sockaddr_in *sin;
    char *client_addr;
public:
    Connection(int c_fd, struct sockaddr_in *c_sin);
    int socket();
    void terminate();
    char *address();
    int transmit(char *data, unsigned int len);
    char *receive(char *data);
};

#endif	/* CONNECTION_H */

