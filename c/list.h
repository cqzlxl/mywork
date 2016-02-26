#ifndef LIST_H
#define LIST_H           1

#include <stddef.h>


typedef struct list_head {
    struct list_head *prev;
    struct list_head *next;
} list_head_t;


typedef struct list {
    int count;
    list_head_t head;
} list_t;


extern int list_head_init(list_head_t *entry);
extern list_head_t *list_head_new(void);
extern void list_head_dumps(const list_head_t *entry);

extern int list_init(list_t *list);
extern list_t *list_new(void);
extern void list_dumps(const list_t *list);


#define list_entry(type,member,link) ((type*) ((char *)(link) - offsetof(type,member)))
#define list_iterate(list,direction,entry) for (list_head_t *entry=(list)->head.direction; entry!=&(list)->head; entry=entry->direction)
#define list_iterate_forward(list,entry) list_iterate(list,next,entry)
#define list_iterate_backward(list,entry) list_iterate(list,prev,entry)
#define list_for_each(list,entry) list_iterate_forward(list,entry)

extern int list_contains(const list_t *list, const list_head_t *entry);
extern void list_prepend(list_t *list, list_head_t *new);
extern void list_append(list_t *list, list_head_t *new);
extern void list_delete(list_t *list, list_head_t *entry);
extern void list_reverse(list_t *list);

static inline int list_empty(const list_t *list)
{
    const list_head_t *head = &list->head;
    return head->prev == head && head == head->next;
}


#endif
