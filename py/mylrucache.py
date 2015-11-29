import functools
import heapq
import itertools
import sys
import time


class LruCache(object):
    ''' for small cache only '''


    def __init__(self, capacity=512, timeout=30000):
        self.__capacity = capacity
        self.__timeout = timeout
        self.__store = dict()
        self.__miss = 0
        self.__hit = 0


    def __str__(self):
        d = dict()
        d['capacity'] = self.capacity
        d['timeout'] = self.timeout
        d['size'] = self.size
        d['miss'] = self.miss
        d['hit'] = self.hit
        return str(d)


    @property
    def capacity(self):
        return self.__capacity

    @property
    def size(self):
        return len(self.__store)


    @property
    def timeout(self):
        return self.__timeout


    def get(self, key, default=None):
        r = self.__store.get(key)
        if r is None or not r.fresh:
            self.__miss += 1
            return default
        else:
            self.__hit += 1
            return r.value


    def put(self, key, value):
        if self.size >= self.capacity:
            lru = heapq.heapify(self.__store.values())[0]
            self.__store.pop(lru.key)

        if key in self.__store:
            r = self.__store[key]
            r.value = value
        else:
            self.__store[key] = LruCache.Record(key, value, self.timeout)


    def clear(self):
        self.__store.clear()


    @property
    def hit(self):
        return self.__hit

    @property
    def miss(self):
        return self.__miss



    class Record(object):
        def __init__(self, key, value, timeout):
            self.__key = key
            self.__timeout = timeout
            self.value = value
            # refresh
            self.value


        def __str__(self):
            d = dict()
            d['key'] = self.key
            d['value'] = self.value
            d['timeout'] = self.timeout
            d['last_read'] = self.last_read
            d['last_write'] = self.last_write
            return str(d)


        def __cmp__(self, other):
            diff = self.last_read - other.last_read
            if diff != 0:
                return diff
            else:
                return self.last_write - other.write


        @property
        def key(self):
            return self.__key


        @property
        def value(self):
            self.__last_read = self.now
            return self.__val

        @value.setter
        def value(self, v):
            self.__val = v
            self.__last_write = self.now


        @property
        def timeout(self):
            return self.__timeout


        @property
        def fresh(self):
            return (self.now - self.last_read) * 1000 - self.timeout <= 0 \
                or (self.now - self.last_write) * 1000 - self.timeout <= 0


        @property
        def last_read(self):
            return self.__last_read


        @property
        def last_write(self):
            return self.__last_write


        @property
        def now(self):
            return time.time()


if __name__ == '__main__':
    def lru_cache(func):
        cache = LruCache()

        @functools.wraps(func)
        def wrapper(*vargs, **kargs):
            sig_args = ', '.join( '{}={}({})'.format(k,v,v.__class__.__name__) for k,v in itertools.chain(enumerate(vargs), kargs.items()))

            result = cache.get(sig_args)
            if result is not None:
                return result

            result = func(*vargs, **kargs)
            cache.put(sig_args, result)
            return result

        return wrapper


    @lru_cache
    def fib1(n):
        if n < 2:
            return n
        else:
            return fib1(n-1) + fib1(n-2)


    def fib2(n):
        if n < 2:
            return n

        a = 0
        b = 1
        i = 1
        while i < n:
            i += 1
            c = a + b
            a = b
            b = c

        return b


    def fib3(n):
        if n < 2:
            return n
        else:
            return fib3(n-1) + fib3(n-2)



    if len(sys.argv) < 2:
        n = 512
    else:
        n = int(sys.argv[1])

    t0 = time.time()
    v1 = fib1(n)
    t1 = time.time()
    v2 = fib2(n)
    t2 = time.time()
    v3 = fib3(n)
    t3 = time.time()

    assert v1 == v2 == v3
    print (t1 - t0) / (t2 - t1), (t1 - t0) / (t3 - t2)
