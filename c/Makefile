CFLAGS    := -std=c99 -Wall -Werror -g -O0
LDFLAGS   := -lpthread
CPPFLAGS  := -D_BSD_SOURCE -I . 

SRCS    := job_test.c job.c event.c logging.c list.c
OBJS    := $(SRCS:.c=.o)


.PHONY: all
.PHONY: clean


all: t
	./t

clean:
	rm $(OBJS) t


t: $(OBJS)
	cc -o $@ $^ $(LDFLAGS)
