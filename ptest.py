#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 7/4/2018 2:12 PM
# @Author  : HH
import time
import multiprocessing
import threading
import re


def work(name, ti, f):
    print(name, '=========', ti)
    if ti > 8:
        ti -= 8
    time.sleep(ti)
    f = open(f, 'a', encoding='utf-8')
    f.write('%d========%d\n' % (name, ti))
    print(name, '=========', ti)
    f.close()


class Pt:
    def __init__(self):
        self.num = 16

    @staticmethod
    def work(n, ti):
        if ti > 8:
            ti -= 8
        time.sleep(ti)
        print(n, '------>', ti)

    def start(self):

        pool = multiprocessing.Pool(processes=8)

        for i in range(self.num):
            pool.apply_async(self.work, args=(i, i + 1,))

        pool.close()
        pool.join()


def sub(filename):
    # pt = Pt()
    #
    # pt.start()
    # f = open(filename, 'w', encoding='utf-8')
    pool = multiprocessing.Pool(processes=8)
    for i in range(16):
        pool.apply_async(work, args=(i, i+1, filename,))

    pool.close()
    pool.join()

    # f.close()


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
    # sub('temp.txt')

    # s = 'dasda+dad/dad123'
    # rsplit = re.compile('\+|/')
    # nre = re.compile('(\d+)')
    # n_res = re.search(nre, s)
    # print(n_res, n_res.group())
    # print('----', n_res.group(0))
    # print(s.find('dad2'))
    # n_list = re.split(rsplit, s)
    # print(n_list)
    print(time.time() - t0)
