#ifndef EVENT_H
#define EVENT_H          1

#include <pthread.h>

#include <list.h>


#define EVENT_NONE               -1


typedef struct event_channel
{
    int event_type;
    int event_times;

    pthread_mutex_t mutex;
    pthread_cond_t occurred;

    list_head_t link;
} event_channel_t;


typedef struct event_bus
{
    list_t channels;

    pthread_mutex_t mutex;
} event_bus_t;


#define event_channel_entry(ref) list_entry(event_channel_t,link,ref)

extern int event_channel_init(event_channel_t *channel, int event_type);
extern event_channel_t *event_channel_new(int event_type);

extern int event_bus_init(event_bus_t *bus);
extern event_bus_t *event_bus_new(void);

extern int event_bus_wait(event_bus_t *bus, int event_type);
extern int event_bus_signal(event_bus_t *bus, int event_type);


#endif
