#include <assert.h>
#include <stdlib.h>

#include <pthread.h>

#include <event.h>
#include <list.h>
#include <logging.h>


int event_channel_init(event_channel_t *channel, int event_type)
{
    assert(channel != NULL);

    channel->event_type = event_type;
    channel->event_times = 0;

    pthread_mutex_init(&channel->mutex, NULL);
    pthread_cond_init(&channel->occurred, NULL);

    list_head_init(&channel->link);

    return 0;
}


event_channel_t *event_channel_new(int event_type)
{
    event_channel_t *c = malloc(sizeof(event_channel_t));
    assert(c != NULL);

    event_channel_init(c, event_type);

    return c;
}


int event_bus_init(event_bus_t *bus)
{
    assert(bus != NULL);

    list_init(&bus->channels);
    pthread_mutex_init(&bus->mutex, NULL);

    return 0;
}


event_bus_t *event_bus_new(void)
{
    event_bus_t *bus = malloc(sizeof(event_bus_t));
    assert(bus != NULL);

    event_bus_init(bus);

    return bus;
}


int event_bus_wait(event_bus_t *bus, int event_type)
{
    if (event_type == EVENT_NONE) return 0;
    assert(bus != NULL);

    pthread_mutex_lock(&bus->mutex);

    event_channel_t *channel = NULL;
    list_for_each(&bus->channels,link)
    {
        event_channel_t *c = event_channel_entry(link);
        if (c->event_type == event_type)
        {
            channel = c;
            break;
        }
    }
    if (channel == NULL)
    {
        channel = event_channel_new(event_type);
        list_prepend(&bus->channels, &channel->link);
    }

    pthread_mutex_lock(&channel->mutex);
    pthread_mutex_unlock(&bus->mutex);

    while (channel->event_times < 1)
        pthread_cond_wait(&channel->occurred, &channel->mutex);
    channel->event_times--;

    pthread_mutex_unlock(&channel->mutex);

    return 0;
}


int event_bus_signal(event_bus_t *bus, int event_type)
{
    if (event_type == EVENT_NONE) return 0;
    assert(bus != NULL);

    pthread_mutex_lock(&bus->mutex);

    event_channel_t *channel = NULL;
    list_for_each(&bus->channels,link)
    {
        event_channel_t *c = event_channel_entry(link);
        if (c->event_type == event_type)
        {
            channel = c;
            break;
        }
    }
    if (channel == NULL)
    {
        channel = event_channel_new(event_type);
        list_prepend(&bus->channels, &channel->link);
    }
    pthread_mutex_lock(&channel->mutex);
    pthread_mutex_unlock(&bus->mutex);

    channel->event_times++;
    pthread_cond_signal(&channel->occurred);

    pthread_mutex_unlock(&channel->mutex);

    return 0;
}
