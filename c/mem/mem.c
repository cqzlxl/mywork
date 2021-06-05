#define _BSD_SOURCE

#include <stdbool.h>
#include <stdint.h>

#include <pthread.h>
#include <unistd.h>

#include <list.h>
#include <mem.h>


typedef struct header {
  bool free;
  size_t size;
  struct list_head list;
} header_t;


LIST_HEAD(free_blocks_list_head);
struct list_head *free_blocks = &free_blocks_list_head;

pthread_mutex_t free_blocks_mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_t *free_blocks_lock = &free_blocks_mutex;


static header_t* search(size_t size) {
  header_t *match = NULL;
  header_t *block = NULL;
  size_t diff = SIZE_MAX;
  list_for_each_entry(block, free_blocks, list) {
    if (block->free && block->size >= size && block->size < size + diff) {
	  diff = block->size - size;
	  match = block;
    }
  }
  return match;
}


void* malloc(size_t size) {
  pthread_mutex_lock(free_blocks_lock);

  header_t *block = search(size);
  if (block) {
    block->free = false;
    pthread_mutex_unlock(free_blocks_lock);
    return (void *) (block + 1);
  }

  void *address = sbrk(sizeof(header_t) + size);
  if (address == (void *) -1) {
    pthread_mutex_unlock(free_blocks_lock);
    return NULL;
  }

  block = address;
  block->size = size;
  block->free = false;

  INIT_LIST_HEAD(&block->list);
  list_add_tail(&block->list, free_blocks);

  pthread_mutex_unlock(free_blocks_lock);
  return (void *) (block + 1);
}


void free(void *address) {
  if (address) {
    void *current_brk = sbrk(0);

    header_t *block = (header_t *) address - 1;
    size_t size = sizeof(header_t) + block->size;

    pthread_mutex_lock(free_blocks_lock);

    if (current_brk ==  (char *) block + size) {
      list_del(&block->list);
      sbrk(-size);
    } else {
      block->free = true;
    }

    pthread_mutex_unlock(free_blocks_lock);
  }
}


__attribute__((constructor)) void init() {
}
