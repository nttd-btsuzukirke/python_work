#!/usr/bin/env python3
#! python3

import datetime
from dateutil.relativedelta import relativedelta, MO
import calendar


def select_dates():
    """
    会議室を取る日にちを決める
    """
    today = datetime.date.today()  # datetimeから日付を取得

    """
    datetimeから各値を取得
        年, 月, 日, 時, 分, 秒

    now.year  # => 2018
    now.month  # => 3
    """

    """
    何ヶ月後か決め、移動させる
    """
    target_month = 2

    dt = datetime.datetime.utcnow()
    # datetime.datetime(2017, 11, 26, 20, 51, 59, 745695)

    #会議室を取る月の初日を求める
    first_date = dt.date() - datetime.timedelta(days=dt.day - 1) + relativedelta(months=target_month)
    print(first_date)
    # 会議室を取る月の最終日を求める
    last_date = first_date + relativedelta(months=1) + datetime.timedelta(days=-1)
    print(last_date)
    # datetime.date(2017, 11, 1)

    #set_month = first_date +
    #print(set_month)

    """
       datetimeから曜日を取得
           weekdayと曜日の対応
           0: 月, 1: 火, 2: 水, 3: 木, 4: 金, 5: 土, 6: 日
    """
    """""
    c1 = calendar.Calendar()
    for ele in c1.itermonthdays2(2018, set_month.month):
        date_list = {}
        date_list = ele# (%2d,%2d)' % (ele[0], ele[1]),
        print(date_list)
        if ele[1] == 6:
            print
            """
    # [x[calendar.MONDAY] for x in calendar.monthcalendar(set_month.year, set_month.month)]

    def next_weekday(d, weekday):
        days_ahead = weekday - d.weekday()
        if days_ahead <= 0:  # Target day already happened this week
            days_ahead += 7
        return d + datetime.timedelta(days_ahead)

    #d = set_month
        #datetime.date(2018, 3, 7)
    #next_monday = next_weekday(d, 6)  # 0 = Monday, 1=Tuesday, 2=Wednesday...
    #print(next_monday)



    """""
    for x in calendar.monthcalendar(set_month.year, set_month.month):
        if set_month.weekday() == 0:
            print('Monday')
        elif set_month.weekday() == 1:
            print('Tuesday')
            """""


select_dates()
