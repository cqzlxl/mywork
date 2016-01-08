##-*-coding: utf-8;-*-##
from py import coroutine


@coroutine
def averager():
    total = 0.0
    count = 0
    average = None

    while True:
        term = yield average
        total += term
        count += 1
        average = total / count

a = averager()
for n in range(10):
    print a.send(n)
