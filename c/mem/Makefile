CFLAGS=-std=c99 -I$(PWD) -fpic -Wall -Wextra -Werror -O2 -g
LIB=libmem.so
APP=mem_tests


.PHONY: ut
ut: $(APP) $(LIB)
	LD_PRELOAD=$(PWD)/$(LIB) ./$(APP)


.PHONY: clean
clean:
	rm -rf *.o $(LIB) $(APP)


$(LIB): mem.o
	$(CC) -shared -o $@ $^


$(APP): mem_tests.o
