/* 
 * File:   listener.h
 * Author: keyman
 *
 * Created on 14 August 2015, 13:09
 */

#ifndef LISTENER_H
#define	LISTENER_H

#include <cstdio>
#include <exception>
#include <stdlib.h>
#include <pthread.h>
#include <syslog.h>
#include <string.h>
#include "monitor.h"
#include "cJSON.h"

#define AGENT_MAX_CONN          10

void listener(unsigned int port, unsigned int max_conn);

#endif	/* LISTENER_H */

