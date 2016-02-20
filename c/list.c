#include <assert.h>
#include <stdlib.h>

#include <list.h>
#include <logging.h>


static inline void list_head_insert(list_head_t *location, list_head_t *entry)
{
    assert(location != NULL);
    assert(entry != NULL);

    list_head_t *prev = location->prev;
    list_head_t *next = location;
    entry->prev = prev;
    entry->next = next;
    prev->next = entry;
    next->prev = entry;
}


static inline void list_head_leave(list_head_t *entry)
{
    assert(entry != NULL);

    list_head_t *prev = entry->prev;
    list_head_t *next = entry->next;
    prev->next = next;
    next->prev = prev;

    entry->prev = entry->next = entry;
}


int list_head_init(list_head_t *entry)
{
    assert(entry != NULL);

    entry->prev = entry->next = entry;
    return 0;
}


list_head_t *list_head_new(void)
{
    list_head_t *e = malloc(sizeof(list_head_t));
    assert(e != NULL);

    list_head_init(e);
    return e;
}


int list_init(list_t *list)
{
    assert(list != NULL);

    list->count = 0;
    list_head_init(&list->head);
    return 0;
}


list_t *list_new(void)
{
    list_t *e = malloc(sizeof(list_t));
    assert(e != NULL);

    list_init(e);
    return e;
}


int list_contains(const list_t *list, const list_head_t *entry)
{
    assert(list != NULL);
    assert(entry != NULL);

    list_for_each(list, e)
    {
        if (e == entry) return 1;
    }
    return 0;
}


void list_prepend(list_t *list, list_head_t *new)
{
    list_head_insert(list->head.next, new);
    list->count++;
}


void list_append(list_t *list, list_head_t *new)
{
    list_head_insert(&list->head, new);
    list->count++;
}


void list_delete(list_t *list, list_head_t *entry)
{
    if (list_contains(list, entry)) list_head_leave(entry);
    list->count--;
}


void dumps_list_head(const list_head_t *entry)
{
    assert(entry != NULL);

    logging_debug("list head %p: prev=>%p, next=>%p", entry, entry->prev, entry->next);
}


void dumps_list(const list_t *list)
{
    assert(list != NULL);

    logging_debug("list %p, length: %d", list, list->count);
    dumps_list_head(&list->head);

    int i = 0;
    list_for_each(list,e)
    {
        ++i;

        logging_debug("list %p, item %d:", list, i);
        dumps_list_head(e);

        if (i > list->count)
        {
            logging_debug("list %p pointers may be wrong", list);
            break;
        }
    }
}
