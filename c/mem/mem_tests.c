#define _BSD_SOURCE

#include <stdio.h>
#include <stdlib.h>

#include <list.h>
#include <mem.h>


typedef struct {
  long data;
  struct list_head list;
} random_long_t;


int main(int argc, char *argv[]) {
  (void) argc;
  (void) argv;

  LIST_HEAD(random_numbers_head);
  struct list_head *random_numbers = &random_numbers_head;

  random_long_t *r = NULL;

  for (int i = 0; i < 10; ++i) {
    r = malloc(sizeof(random_long_t));
    r->data = random();

    INIT_LIST_HEAD(&r->list);
    list_add_tail(&r->list, random_numbers);
  }

  list_for_each_entry(r, random_numbers, list) {
    printf("%ld\n", r->data);
    free(r);
  }

  return 0;
}
