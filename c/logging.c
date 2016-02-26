#include <alloca.h>
#include <pthread.h>
#include <stdarg.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

#include <logging.h>


static FILE *logging_stream = NULL;
static pthread_mutex_t logging_stream_mutex = PTHREAD_MUTEX_INITIALIZER;


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


int do_logging(const struct logging_location *loc, int level, const char *fmt, ...)
{
    const char *level_name;
    switch(level)
    {
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

        case LOGGING_TRACE:
            level_name = "TRACE";
            break;

        default:
            return 0;
            break;
    };

    time_t seconds = time(NULL);
    struct tm now = {};
    localtime_r(&seconds, &now);

    char timestr[] = "1999-12-31 23:59:59(0000000000)";
    char timefmt[] = "%F %T(%s)";
    strftime(timestr, sizeof(timestr), timefmt, &now);

    FILE *stream = logging_get_stream();
    int n = 0;

    if (pthread_mutex_lock(&logging_stream_mutex) == 0)
    {
        n += fprintf(stream, "%s %s ", timestr, level_name);

        if (level != LOGGING_INFO)
        {
            char *buffer = alloca(1024);
            LOGGING_LOCATION_STRING(loc, buffer, 1024);
            n += fprintf(stream, " %s ", buffer);
        }

        va_list args;
        va_start(args, fmt);
        n += vfprintf(stream, fmt, args);
        va_end(args);

        n += fprintf(stream, "\n");

        pthread_mutex_unlock(&logging_stream_mutex);
    }

    return n;
}
