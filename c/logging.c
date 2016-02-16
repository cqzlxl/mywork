#include <alloca.h>
#include <stdarg.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

#include <logging.h>


static FILE *logging_stream = NULL;


static int do_logging(int level, const char *fmt, va_list args)
{
    const char *level_name;
    switch(level) {
        case LOGGING_ERROR:
            level_name = "ERROR";
            break;

        case LOGGING_WARN:
            level_name = "WARN";
            break;

        case LOGGING_INFO:
            level_name = "INFO";
            break;

        case LOGGING_DEBUG:
            level_name = "DEBUG";
            break;

        default:
            level_name = "TRACE";
            break;
    };

    time_t seconds = time(NULL);
    struct tm now = {};
    localtime_r(&seconds, &now);

    char timestr[] = "1999-01-01 00:00:00(0000000000)";
    char timefmt[] = "%F %T(%s)";
    strftime(timestr, sizeof(timestr), timefmt, &now);


    FILE *stream = logging_get_stream();
    int n = 0;
    n += fprintf(stream, "%s %s ", timestr, level_name);
    n += vfprintf(stream, fmt, args);
    n += fprintf(stream, "\n");

    return n;
}

#define DO_LOGGING(level,format) do {               \
        va_list args;                               \
        va_start(args, format);                     \
        int n = do_logging(level, format, args);    \
        va_end(args);                               \
        return n;                                   \
} while(0)


int logging(int level, const char *format, ...)
{
    DO_LOGGING(level, format);
}


int logging_error(const char *format, ...)
{
    DO_LOGGING(LOGGING_ERROR, format);
}


int logging_warn(const char *format, ...)
{
    DO_LOGGING(LOGGING_WARN, format);
}


int logging_info(const char *format, ...)
{
    DO_LOGGING(LOGGING_INFO, format);
}


int logging_debug(const char *format, ...)
{
    DO_LOGGING(LOGGING_DEBUG, format);
}


int logging_set_stream(FILE *stream)
{
    logging_stream = stream;
    return 0;
}


FILE* logging_get_stream(void)
{
    if (logging_stream == NULL)
        logging_set_stream(stderr);

    return logging_stream;
}
