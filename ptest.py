#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 7/4/2018 2:12 PM
# @Author  : HH
import time
import multiprocessing
import threading


def work(name, ti):
    if ti > 8:
        ti -= 8
    time.sleep(ti)
    print(name, '=========', ti)


class Pt:

    def __init__(self):
        self.num = 16

    def work(self, n, ti):
        if ti>8:
            ti-=8
        time.sleep(ti)
        print(n, '------>', ti)

    def start(self):

        pool = multiprocessing.Pool(processes=8)

        for i in range(self.num):
            pool.apply_async(self.work, args=(i, i+1,))

        pool.close()
        pool.join()


if __name__ == '__main__':
    t0 = time.time()
    print(t0)
    # pool = multiprocessing.Pool(processes=8)
    # for i in range(16):
    #     pool.apply_async(work, args=(i, i+1,))
    #
    # pool.close()
    # pool.join()
    # tp = []
    # for i in range(16):
    #     t = threading.Thread(target=work, args=(i, i+1,))
    #     tp.append(t)
    #
    # for t in tp:
    #     t.start()
    #     t.join()
    pt = Pt()

    pt.start()

    print(time.time()-t0)
