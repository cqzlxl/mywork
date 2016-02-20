#ifndef LOGGING_H
#define LOGGING_H        1

#include <errno.h>
#include <stdio.h>
#include <string.h>


#define LOGGING_ERROR     50
#define LOGGING_WARN      40
#define LOGGING_INFO      30
#define LOGGING_DEBUG     20
#define LOGGING_TRACE     10
#define LOGGING_NONE      0


extern int logging(int level, const char *format, ...);


extern int logging_error(const char *format, ...);


extern int logging_warn(const char *format, ...);


extern int logging_info(const char *format, ...);


extern int logging_debug(const char *format, ...);


#define logging_syscall_error(syscall) do {                             \
        logging(LOGGING_ERROR, "system call failed: %s: %d(%s)", syscall, errno, strerror(errno)); \
} while(0)


extern int logging_set_stream(FILE *stream);


extern FILE* logging_get_stream(void);


#endif
