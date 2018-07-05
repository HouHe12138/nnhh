#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 7/4/2018 11:42 AM
# @Author  : HH
from tkinter import *
from urllib import request
from bs4 import BeautifulSoup
import re
import time
import multiprocessing
import threading
import xlsxwriter


class TSkillTK:
    key_num = {}
    ent = ''
    _lock = threading.Lock()

    def __init__(self, fn='skill_1.txt'):
        self.filename = fn

    def page(self, url, fn):
        # print('page------------->', url)
        position = request.urlopen(url)
        pos = position.read()
        position.close()
        pos_need = BeautifulSoup(pos, 'html.parser', from_encoding='gbk')
        needs = pos_need.select(".tCompany_main .job_msg")
        uncn = re.compile('([a-zA-Z/_\-+# ]+)?', re.M)
        num_re = re.compile('([a-zA-Z/_\-+# ]+)?', re.M)
        blank_re = re.compile('\s+', re.M)
        judge = ['!', '(', ')', '/', '.', '+', '-', '*', '#', '（', '）', 'a', 'b', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        f = open(fn, 'a', encoding='utf-8')
        kn = {}
        for need in needs:
            uncn_txt = uncn.findall(need.get_text())
            need_txt = []
            for txt in uncn_txt:
                txt = txt.strip().lower()
                if txt != '' and (not txt in judge):
                    if num_re.search(re.sub(blank_re, '', txt)):
                        need_txt.append(txt)
                        kn[txt] = kn.get(txt, 0) + 1
            en = ",".join(need_txt)
            f.write(en)
            f.write(need.get_text().encode('utf-8').decode('utf-8') + '\n')
        f.close()
        return kn

    def ppage(self, pg, limit, fn):
        f = open(fn, 'a', encoding='utf-8')
        kn = {}
        for p in range(pg, limit):
            response = request.urlopen("https://search.51job.com/list/080200,000000,0000,00,9,99," + request.quote(self.ent) +
                                       ",2," + str(p) +
                                       ".html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize"
                                       "=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&lin"
                                       "e=&specialarea=00&from=&welfare=")

            res = response.read()
            response.close()

            soup = BeautifulSoup(res, 'html.parser', from_encoding='gbk')
            urls = [k.get('href') for k in soup.select('div.el p.t1 a')]
            for url in urls:
                try:
                    position = request.urlopen(url)
                    pos = position.read()
                    position.close()
                    pos_need = BeautifulSoup(pos, 'html.parser', from_encoding='gbk')
                    needs = pos_need.select(".tCompany_main .job_msg")

                    uncn = re.compile('([a-zA-Z/_\-+# ]+)?', re.M)
                    num_re = re.compile('([a-zA-Z/_\-+# ]+)?', re.M)
                    blank_re = re.compile('\s+', re.M)
                    judge = ['!', '(', ')', '/', '.', '+', '-', '*', '#', '（', '）', 'a', 'b', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

                    for need in needs:
                        uncn_txt = uncn.findall(need.get_text())
                        need_txt = []
                        for txt in uncn_txt:
                            txt = txt.strip().lower()
                            if txt != '' and (not txt in judge):
                                if num_re.search(re.sub(blank_re, '', txt)):
                                    need_txt.append(txt)
                                    kn[txt] = kn.get(txt, 0) + 1
                        en = ",".join(need_txt)
                        f.write(en)
                        f.write(need.get_text().encode('utf-8').decode('utf-8') + '\n')
                except Exception as e:
                    print(e)
        print('ppage end ===========', pg, limit)
        f.close()
        return kn

    def callback(self, kn):
        with self._lock:
            for k, v in kn.items():
                self.key_num[k] = self.key_num.get(k, 0) + v

    def submit(self, ent):
        self.ent = ent
        t0 = time.time()
        f = open(self.filename, 'w', encoding='utf-8')
        f.close()
        print('submit', t0)
        response = request.urlopen("https://search.51job.com/list/080200,000000,0000,00,9,99," + request.quote(ent) +
                                   ",2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize"
                                   "=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&lin"
                                   "e=&specialarea=00&from=&welfare=")
        res = response.read()
        response.close()

        soup = BeautifulSoup(res, 'html.parser', from_encoding='gbk')
        pages = soup.select_one(".dw_page .td")

        print(pages.get_text()[1:4])
        m = int(pages.get_text()[1:4]) / 30
        print(m)
        urls = [k.get('href') for k in soup.select('div.el p.t1 a')]
        pool = multiprocessing.Pool(processes=multiprocessing.cpu_count()*2)
        for url in urls:
            pool.apply_async(self.page, args=(url, self.filename,), callback=self.callback)

        pg = 2
        limit = int(pages.get_text()[1:4])
        # limit = 100
        for x in range(pg, limit, 1):
            pool.apply_async(self.ppage, args=(x, x + 1, self.filename,), callback=self.callback)
        pool.close()
        pool.join()

        t1 = time.time()
        print('submit==================', t1 - t0)
        # print(self.key_num)
        test_need = xlsxwriter.Workbook('result_testskill_1.xlsx')
        worksheet = test_need.add_worksheet('skill_needs')
        headings = ['skills', 'count']
        worksheet.write_row('A1', headings)
        row = 1
        col = 0
        for key in self.key_num:
            if len(key) <= 20:
                worksheet.write(row, col, key)
                worksheet.write(row, col + 1, self.key_num[key])
                row += 1
        test_need.close()
        print("success", time.time() - t1)


class Reg(Frame):
    tstk = TSkillTK()

    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        self.lab1 = Label(frame, text="职位:")
        self.lab1.grid(row=2, column=1, sticky=W)
        self.ent1 = Entry(frame)
        self.ent1.grid(row=2, column=3, sticky=W)
        self.button = Button(frame, text="查询", command=self.Submit)
        self.button.grid(row=4, column=3, sticky=E)

    def Submit(self):

        self.button.configure(**{'state': DISABLED})
        ent = self.ent1.get()
        self.tstk.submit(ent)
        self.button.configure(**{'state': NORMAL})


if __name__ == "__main__":
    root = Tk()
    root.geometry("500x150")
    root.title("搜索职位要求")
    app = Reg(root)
    root.mainloop()
