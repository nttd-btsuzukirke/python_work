#!/usr/bin/env python3

import datetime
from dateutil.relativedelta import relativedelta
import calendar

def select_dates():
    """
    会議室を取る日にちを決める
    """
    today = datetime.date.today()  # datetimeから日付を取得
    print(today)
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
    set_month = today + relativedelta(months=target_month)
    print('今日から2ヶ月後は' + str(set_month) + 'です。')
    """
       datetimeから曜日を取得
           weekdayと曜日の対応
           0: 月, 1: 火, 2: 水, 3: 木, 4: 金, 5: 土, 6: 日
    """
    c1 = calendar.Calendar()
    for ele in c1.itermonthdays2(2018, set_month.month):
        print(ele)  # (%2d,%2d)' % (ele[0], ele[1]),
        if ele[1] == 6:
            print
    #[x[calendar.MONDAY] for x in calendar.monthcalendar(set_month.year, set_month.month)]
    """""
    for x in calendar.monthcalendar(set_month.year, set_month.month):
        if set_month.weekday() == 0:
            print('Monday')
        elif set_month.weekday() == 1:
            print('Tuesday')
            """""


select_dates()
