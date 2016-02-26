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


struct logging_location
{
    const char *function;
    const char *filename;
    int line;
    void *udata;
};

#define LOGGING_LOCATION_INITIALIZER(udata) {__FUNCTION__, __FILE__, __LINE__, (udata)}
#define LOGGING_LOCATION_LINE(n) #n
#define LOGGING_LOCATION_HERE __FUNCTION__ "() @" __FILE__ ": " LOGGING_LOCATION_LINE(__LINE__)
#define LOGGING_LOCATION_STRING(p,buffer,n) snprintf(buffer,n, "%s() @ %s: %d", p->function, p->filename, p->line)


extern int logging_set_stream(FILE *stream);
extern FILE* logging_get_stream(void);


extern int do_logging(const struct logging_location *location, int level, const char *format, ...);


#define logging(level,format,...) do {                                  \
        struct logging_location loc = LOGGING_LOCATION_INITIALIZER(NULL); \
        do_logging(&loc, level, format, ##__VA_ARGS__);                 \
} while (0)


#define logging_error(format,...) logging(LOGGING_ERROR, format, ##__VA_ARGS__)


#define logging_warn(format,...) logging(LOGGING_WARN, format, ##__VA_ARGS__)


#define logging_info(format,...) logging(LOGGING_INFO, format, ##__VA_ARGS__)


#define logging_debug(format,...) logging(LOGGING_DEBUG, format, ##__VA_ARGS__)


#define logging_trace(format,...) logging(LOGGING_TRACE, format, ##__VA_ARGS__)


#define logging_syscall_error(syscall) logging_error("system call failed: %s: %d(%s)", syscall, errno, strerror(errno))


#endif
