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


filename = 'skill_1.txt'
_lock = threading.Lock()
key_num = {}
ent1 = ''

root = Tk()
root.geometry("500x150")


def ppage(page, limit):
    print('===========', page, limit)
    for p in range(page, limit):
        print('for -------------------->')
        response = request.urlopen("https://search.51job.com/list/080200,000000,0000,00,9,99," + request.quote(ent1) +
                                   ",2," + str(p) +
                                   ".html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize"
                                   "=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&lin"
                                   "e=&specialarea=00&from=&welfare=")

        res = response.read()
        response.close()

        soup = BeautifulSoup(res, 'html.parser', from_encoding='gbk')
        urls = [k.get('href') for k in soup.select('div.el p.t1 a')]
        # key_num = {}
        f = open(filename, 'a', encoding='utf-8')
        for url in urls:
            try:
                position = request.urlopen(url)
                pos = position.read()
                position.close()
                pos_need = BeautifulSoup(pos, 'html.parser', from_encoding='gbk')
                # print(pos_need)
                needs = pos_need.select(".tCompany_main .job_msg")
                # need = soup.find_all('div',class_='bmsg job_msg inbox').find_all('p')
                # uncn = re.compile(r'[\u0061-\u007a,\u0041-\u005a,\u3001,\u0020,\u002c,\u002e,\u002b,\u002d,\u0023,\u0028,\u0029,\u005c]')

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
                                with _lock:
                                    key_num[txt] = key_num.get(txt, 0) + 1
                    en = ",".join(need_txt)
                    f.write(en)
                    f.write('\n' + need.get_text().encode('utf-8').decode('utf-8') + '\n')
            except Exception as e:
                print(e)
        f.close()
    print('===========end', page, limit)


def ssubmit(page, limit):

    pool = multiprocessing.Pool(processes=16)
    while limit - page >= 20:
        # self.Page(page, page + 20)
        pool.apply_async(ppage, args=(page, page + 20,))
        # p.start()
        page += 20

    # self.Page(page, limit)
    pool.apply_async(ppage, args=(page, limit,))
    pool.close()
    pool.join()
    print('submit', time.time())
    print(key_num)
    # filename = '/Users/NN/Desktop/测试技能统计结果.xlsx'
    test_need = xlsxwriter.Workbook('result_testskill_1.xlsx')
    worksheet = test_need.add_worksheet('skill_needs')
    headings = ['skills', 'count']
    worksheet.write_row('A1', headings)
    row = 1
    col = 0
    for key in key_num:
        worksheet.write(row, col, key)
        worksheet.write(row, col + 1, key_num[key])
        row += 1
    test_need.close()
    print("success", time.time())


class Reg(Frame):
    # global key_num
    key_num = {}
    filename = 'skill_1.txt'
    _lock = threading.Lock()

    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        self.lab1 = Label(frame, text="职位:")
        self.lab1.grid(row=2, column=1, sticky=W)
        self.ent1 = Entry(frame)
        self.ent1.grid(row=2, column=3, sticky=W)
        self.button = Button(frame, text="查询", command=self.Submit)
        self.button.grid(row=4, column=3, sticky=E)

    def Page(self, page, limit):
        print('===========', page, limit)
        for p in range(page, limit):
            response = request.urlopen("https://search.51job.com/list/080200,000000,0000,00,9,99," + request.quote(self.ent1.get()) +
                                       ",2," + str(p) +
                                       ".html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize"
                                       "=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&lin"
                                       "e=&specialarea=00&from=&welfare=")
            res = response.read()
            response.close()

            soup = BeautifulSoup(res, 'html.parser', from_encoding='gbk')
            urls = [k.get('href') for k in soup.select('div.el p.t1 a')]
            # key_num = {}
            f = open(self.filename, 'a', encoding='utf-8')
            for url in urls:
                try:
                    position = request.urlopen(url)
                    pos = position.read()
                    position.close()
                    pos_need = BeautifulSoup(pos, 'html.parser', from_encoding='gbk')
                    # print(pos_need)
                    needs = pos_need.select(".tCompany_main .job_msg")
                    # need = soup.find_all('div',class_='bmsg job_msg inbox').find_all('p')
                    # uncn = re.compile(r'[\u0061-\u007a,\u0041-\u005a,\u3001,\u0020,\u002c,\u002e,\u002b,\u002d,\u0023,\u0028,\u0029,\u005c]')

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
                                    with self._lock:
                                        self.key_num[txt] = self.key_num.get(txt, 0) + 1
                        en = ",".join(need_txt)
                        f.write(en)
                        f.write('\n' + need.get_text().encode('utf-8').decode('utf-8') + '\n')
                except Exception as e:
                    print(e)
            f.close()
        print('===========end', page, limit)

    def Submit(self):
        print('submit', time.time())
        ent1 = self.ent1.get()
        response = request.urlopen("https://search.51job.com/list/080200,000000,0000,00,9,99," + request.quote(self.ent1.get()) +
                                   ",2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize"
                                   "=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&lin"
                                   "e=&specialarea=00&from=&welfare=")
        res = response.read()
        response.close()
        # print(res[0, 100])

        soup = BeautifulSoup(res, 'html.parser', from_encoding='gbk')
        # print(soup)
        # values = [input.attrs.get('value') for input in soup.select('div.el p.t1 input')]
        pages = soup.select_one(".dw_page .td")

        print(pages.get_text()[1:4])
        m = int(pages.get_text()[1:4]) / 30
        print(m)
        urls = [k.get('href') for k in soup.select('div.el p.t1 a')]
        # key_num = {}
        f = open(self.filename, 'w', encoding='utf-8')
        for url in urls:
            position = request.urlopen(url)
            pos = position.read()
            position.close()
            pos_need = BeautifulSoup(pos, 'html.parser', from_encoding='gbk')
            # print(pos_need)
            needs = pos_need.select(".tCompany_main .job_msg")
            # need = soup.find_all('div',class_='bmsg job_msg inbox').find_all('p')
            # uncn = re.compile(r'[\u0061-\u007a,\u0041-\u005a,\u3001,\u0020,\u002c,\u002e,\u002b,\u002d,\u0023,\u0028,\u0029,\u005c]')

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
                            key_num[txt] = key_num.get(txt, 0) + 1
                en = ",".join(need_txt)
                f.write(en)
                f.write('\n' + need.get_text().encode('utf-8').decode('utf-8') + '\n')
                # print(en, '\n============================\n', need.get_text())
                # print(en,'\n========\n')
                # if len(need_txt) ==1:

                # for need in needs:
                #     en = "".join(uncn.findall(need.get_text()))
                #     print(en)
                #     # print(need.get_text())
                # break
                # print(values)
                # print(urls)
                # print(response.read())
                # int(pages.get_text()[1:4])
        f.close()
        print('submit11111111', time.time())
        page = 2
        limit = int(pages.get_text()[1:4])
        limit = 16
        # ssubmit(page, limit)
        multiprocessing.freeze_support()
        pool = multiprocessing.Pool(processes=16)
        for x in range(page, limit, 1):
            pool.apply_async(self.Page, args=(x, x+1,))
        # while limit - page >= 2:
        #     # self.Page(page, page + 20)
        #     pool.apply_async(self.Page, args=(page, page + 20,))
        #     # p.start()
        #     page += 20

        # self.Page(page, limit)
        # pool.apply_async(self.Page, args=(page, limit,))
        pool.close()
        pool.join()
        print('submit', time.time())
        print(self.key_num)
        # filename = '/Users/NN/Desktop/测试技能统计结果.xlsx'
        test_need = xlsxwriter.Workbook('result_testskill_1.xlsx')
        worksheet = test_need.add_worksheet('skill_needs')
        headings = ['skills', 'count']
        worksheet.write_row('A1', headings)
        row = 1
        col = 0
        for key in self.key_num:
            worksheet.write(row, col, key)
            worksheet.write(row, col + 1, self.key_num[key])
            row += 1
        test_need.close()
        print("success", time.time())

# if __name__ == "__main__":

root.title("搜索职位要求")
app = Reg(root)
root.mainloop()