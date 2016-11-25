#include "connection.h"

Connection::Connection(int c_fd, struct sockaddr_in *c_sin) {
    sock = c_fd;
    sin = c_sin;
    client_addr = (char *)inet_ntoa(sin->sin_addr);
}

int Connection::socket() {
    return sock;
}

char *Connection::address() {
    return client_addr;
}

int Connection::transmit(char *data, unsigned int len) {
    return send(sock, data, len, 0);
}

char *Connection::receive(char *data) {
    size_t total = 0;
    size_t length = 0;
    char buffer[RECV_BUFFER_SIZE];
    
    while (true) {
        memset(buffer, 0x00, RECV_BUFFER_SIZE);
        length = recv(sock, buffer, RECV_BUFFER_SIZE - 1, MSG_DONTWAIT);
        if (length == -1 || length == 0) break;
        if (total + length > RECV_MAX_MSG_SIZE * 1048576) {
            if (data != NULL) free(data);
            throw "Connection::receive(): invalid message size";
        }
        data = (char *)realloc(data, total + length);
        if (data == NULL) {
            throw "Connection::receive(): failed to realloc() data buffer";
        }
        strcpy(data + total, buffer);
        total += length;
    }

    memset(buffer, 0x00, RECV_BUFFER_SIZE);
    return(data);
}

void Connection::terminate() {
    close(sock);
}