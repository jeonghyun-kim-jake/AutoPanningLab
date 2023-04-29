#ifndef COMMON_LOGS_H
#define COMMON_LOGS_H

#include <stdio.h>
#include <iostream>
#include <string.h>

#define LOG_TAG "APN@"

#define PARAM_CHECK(expr)           RET_MSG_IF(!(expr),"INVALID PARAM RETURN")
#define PARAM_CHECK_FALSE(expr)     RETV_MSG_IF(!(expr),FALSE,"INVALID PARM RETURN FALSE")
#define PARAM_CHECK_VAL(expr, val)  RETV_MSG_IF(!(expr),val,"INVALID PARM RETURN NULL")
#define PARAM_CHECK_NULL(expr)      RETV_MSG_IF(!(expr),NULL,"INVALID PARM RETURN NULL")

#define BOOL(x) (x?("TRUE"):("FALSE"))
#define ARRAY_LEN(X) (sizeof(X)/sizeof((X)[0]))

typedef enum LogLevel{
    INFO,
    WARN,
    DEBUG,
    ERROR
}LogLevel;

#define __CALL_INFO__ (strrchr(__FILE__, '/') ? strrchr(__FILE__, '/') + 1 : __FILE__)

#define LOG_(level, fmt, args...) \
{ \
    char tag[100] = {'\0',};\
    snprintf(tag, 100, ("%s:%s"), LOG_TAG, __CALL_INFO__);\
    char msg[100] = {'\0',};\
    snprintf(msg, 100, ("(%s:%d) " fmt), __func__, __LINE__, ##args);\
    printf("[%s] %s\n", tag, msg);\
    fflush(stdout);\
}

#define LOGD(fmt, args...) LOG_(DEBUG, fmt, ##args)
#define LOGI(fmt, args...) LOG_(INFO, fmt, ##args)
#define LOGW(fmt, args...) LOG_(WARN, fmt, ##args)
#define LOGE(fmt, args...) LOG_(ERROR, fmt, ##args)

#ifdef DEBUG_MODE
    #define LOGDEBUG(fmt, arg...) LOG_(DEBUG, fmt, ##args)
#else
    #define LOGDEBUG(fmt, arg...) 
#endif

#endif