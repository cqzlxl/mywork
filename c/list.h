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

extern int list_init(list_t *list);
extern list_t *list_new(void);

#define list_entry(type,member,link) ((type*) ((char *)(link) - offsetof(type,member)))
#define list_for_each(list,entry) for (list_head_t *entry=(list)->head.next; entry!=&(list)->head; entry=entry->next)

extern int list_contains(const list_t *list, const list_head_t *entry);
extern void list_prepend(list_t *list, list_head_t *new);
extern void list_append(list_t *list, list_head_t *new);
extern void list_delete(list_t *list, list_head_t *entry);

extern void dumps_list_head(const list_head_t *entry);
extern void dumps_list(const list_t *list);


static inline int list_empty(const list_t *list)
{
    const list_head_t *head = &list->head;
    return head->prev == head && head == head->next;
}


#endif
