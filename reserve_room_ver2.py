#! python3
# -*- coding:utf-8 -*-
from selenium import webdriver
import selenium
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException

import time
import datetime
from dateutil.relativedelta import relativedelta
import calendar
import jholiday

#IE用ドライバー
driver = webdriver.Ie('C:/Users/U621625/PycharmProjects/Work/selenium/webdriver/IEDriverServer.exe')

"""
会議室を取る日にちを決める
"""

#何ヶ月後を予約するかを指定　例）１ヶ月先は１、２ヶ月先は２
target_month = 2

today = datetime.date.today()  # datetimeから今日の日付を取得
get_month = today + relativedelta(months=target_month)


"""
ブラウザ操作開始
"""
#ログイン画面開く
url='https://gg2.groupwide.net/iMRRoomBooking/'
driver.get(url)

#ログイン情報
login_id = ''
com_id = ''
password = ''

"""
LOGIN
"""
def login():
    driver.find_element_by_name("id1").send_keys(login_id) #idボックスのを探し入力
    driver.find_element_by_name("id2").send_keys(com_id) #会社識別子ボックスを探し入力
    driver.find_element_by_name("password").send_keys(password) #パスワードボックスを探し入力
    driver.find_element_by_xpath("//input[@title='Login'][@type='submit']").click() #Loginボタン押下
    driver.implicitly_wait(10)
login()


#指定月まで表示カレンダーを移動。2ヶ月先まで表示するには二回Nextボタン押す必要あり
for i in range(target_month):
    driver.implicitly_wait(10)  # 見つからないときは、10秒まで待つ
    driver.find_element_by_link_text("Next").click() #Nextボタン押下
    time.sleep(3)


def get_dates():
    """
    月の最初の日と最後の日を調べる

    """
    # 会議室を取る月の初日を求める
    first_date = get_month - datetime.timedelta(days=today.day - 1)
    # 会議室を取る月の最終日を求める
    last_date = first_date + relativedelta(months=1) + datetime.timedelta(days=-1)

    return first_date, last_date
first, last = get_dates()



def my_mtg():

    """"
    個人用の予約

    """

    for d in range(first.day, last.day+1, 1): # 月の初めから最後までループ

        iter_date = today + relativedelta(months=target_month) - datetime.timedelta(days=get_month.day - d) # iが増えることで日も増える
        """
        datetimeから曜日を取得
        weekdayと曜日の対応     
        0: 月, 1: 火, 2: 水, 3: 木, 4: 金, 5: 土, 6: 日
        """
        """
        属性の値　data-timeline = "x" ←　以下から該当する数字をxに記入する
    
        1: 応接室,　2: 大会議室,　3: SouthTerrace,　4: Core-A　6: FR事業部長会議室　
        7:流サ事業部長会議室　8: N-A,　9: N-B, 10: N-C, 11: N-D, 12:N-E, 
        13: S-A,　14: S-B, 15: S-C, 16: S-D, 17: S-E
        """

        #祝日セット
        holiday_name = jholiday.holiday_name(date=iter_date)

        if holiday_name is None:

            if iter_date.weekday() == 1: #火曜日だったら以下を予約
                """
                             大会議室　火曜　11:00-12:00を予約
        
                """
                start_time = '11:00'
                end_time = '12:00'
                day_name = '(火)'

                try:
                    driver.implicitly_wait(10)
                    driver.find_element_by_link_text(str(d)).click()  # 日付指定
                    driver.find_element_by_xpath('//div[@class="tl ui-selectee"][@data-timeline="12"]').click()  # 二行目(大会議室)を選択
                    # 時間選択
                    start_time_element = driver.find_element_by_name('StartTime')
                    select_start_time = Select(start_time_element)
                    select_start_time.select_by_value(start_time)
                    end_time_element = driver.find_element_by_name('EndTime')
                    select_end_time = Select(end_time_element)
                    select_end_time.select_by_value(end_time)
                    # 目的選択
                    purpose = driver.find_element_by_name('PurposeCode')
                    select_purpose = Select(purpose)
                    select_purpose.select_by_value('1')
                    driver.find_element_by_name("NumberOfUsers").send_keys('10')
                    # 予約ボタン押下
                    driver.find_element_by_xpath('//button[@class="btn blue submit-form-new"][@type="button"]').click()
                    driver.implicitly_wait(10)

                    # ダブルブッキングした場合
                    alert_msg = driver.find_element_by_xpath('//section[@class="alert error active"]')
                    if alert_msg:
                        print(str(iter_date) + " " + day_name + " " + '大会議室 ' + str(start_time) + '-' + str(
                            end_time) + ' は既に取られています')
                        driver.find_element_by_xpath('//div[@class="btnCircle close"][@id="close-entry"]').click()
                        driver.implicitly_wait(10)
                    else:
                        print(str(iter_date) + " " + day_name + " " + '大会議室 ' + str(start_time) + '-' + str(
                            end_time) + ' は予約完了')

                except selenium.common.exceptions.UnexpectedAlertPresentException:
                    print(str(iter_date) + " " + day_name + " " + str(start_time) + '-' + str(end_time) + ' は祝日です')
                except NoSuchElementException:
                    print("属性が見つかりませんでした。")
                except ElementNotInteractableException:
                    print("クリックできませんでした。")


                """
                            　火曜　14:00-15:00を予約
                
                start_time = '14:00'
                end_time = '15:00'
                 if iter_date.weekday() == 0:
                    day_name = '(月)'
                elif iter_date.weekday() == 1:
                    day_name = '(火)'
                elif iter_date.weekday() == 2:
                    day_name = '(水)'
                elif iter_date.weekday() == 3:
                    day_name = '(木)'
                elif iter_date.weekday() == 4:
                    day_name = '(金)'
                    
                driver.implicitly_wait(10)
                try:
                    driver.find_element_by_link_text(str(d)).click()  # 日付指定
                    driver.find_element_by_xpath('//div[@class="tl ui-selectee"][@data-timeline="12"]').click()  # N-Fを選択
                    start_time_element = driver.find_element_by_name('StartTime')
                    select_start_time = Select(start_time_element)
                    select_start_time.select_by_value(start_time)
                    end_time_element = driver.find_element_by_name('EndTime')
                    select_end_time = Select(end_time_element)
                    select_end_time.select_by_value(end_time)
    
                    #目的選択
                    purpose = driver.find_element_by_name('PurposeCode')
                    select_purpose = Select(purpose)
                    select_purpose.select_by_value('1')
                    driver.find_element_by_name("NumberOfUsers").send_keys('10')
                    
                    # 予約ボタン押下
                    driver.find_element_by_xpath('//button[@class="btn blue submit-form-new"][@type="button"]').click()
                    driver.implicitly_wait(10)
                    
                    # ダブルブッキングした場合
                    alert_msg = driver.find_element_by_xpath('//section[@class="alert error active"]')

                    if alert_msg:
                        print(str(iter_date) + " " + day_name + " " + 'SouthTerrace ' + str(start_time) + '-' + str(
                            end_time) + ' は既に取られています')
                        driver.find_element_by_xpath('//div[@class="btnCircle close"][@id="close-entry"]').click()
                        driver.implicitly_wait(10)
                    else:
                        print(str(iter_date) + " " + day_name + " " + 'SouthTerrace ' + str(start_time) + '-' + str(
                            end_time) + ' は予約完了')

                except selenium.common.exceptions.UnexpectedAlertPresentException:
                     print(str(iter_date) + " " + day_name + " " + str(start_time) + '-' + str(
                    end_time) + ' は祝日です')
                except NoSuchElementException:
                    print("属性が見つかりませんでした。")
                except ElementNotInteractableException:
                    print("クリックできませんでした。")
                """

            elif iter_date.weekday() == 3: # 木曜だったら以下を予約
                """
                            South Terrace 木曜　16:00-18:00を予約
                """
                start_time = '16:00'
                end_time = '18:00'
                day_name = '(木)'

                try:
                    driver.find_element_by_link_text(str(d)).click()  # 日付指定
                    driver.implicitly_wait(10)  # 見つからないときは、10秒まで待つ
                    driver.find_element_by_xpath('//div[@class="tl ui-selectee"][@data-timeline="3"]').click()  # STを選択

                    # 時間選択
                    start_time_element = driver.find_element_by_name('StartTime')
                    select_start_time = Select(start_time_element)
                    select_start_time.select_by_value(start_time)
                    end_time_element = driver.find_element_by_name('EndTime')
                    select_end_time = Select(end_time_element)
                    select_end_time.select_by_value(end_time)
                    # 目的選択
                    purpose = driver.find_element_by_name('PurposeCode')
                    select_purpose = Select(purpose)
                    select_purpose.select_by_value('1')
                    driver.find_element_by_name("NumberOfUsers").send_keys('10')
                    # 予約ボタン押下
                    driver.find_element_by_xpath('//button[@class="btn blue submit-form-new"][@type="button"]').click()
                    driver.implicitly_wait(10)

                    # ダブルブッキングした場合
                    alert_msg = driver.find_element_by_xpath('//section[@class="alert error active"]')

                    if alert_msg:
                        print(str(iter_date) + " " + day_name + " " + 'SouthTerrace ' + str(start_time) + '-' + str(end_time) + ' は既に取られています')
                        driver.find_element_by_xpath('//div[@class="btnCircle close"][@id="close-entry"]').click()
                        driver.implicitly_wait(10)
                    else:
                        print(str(iter_date) + " " + day_name + " " + 'SouthTerrace ' + str(start_time) + '-' + str(end_time) + ' の予約完了')

                except selenium.common.exceptions.UnexpectedAlertPresentException:
                    print(str(iter_date) + " " + day_name + " " + str(start_time) + '-' + str(
                        end_time) + ' は祝日です')
                except NoSuchElementException:
                    print("属性が見つかりませんでした。")
                except ElementNotInteractableException:
                    print("クリックできませんでした。")


def oms_mtg():
    """"
    試験朝会用の予約

    """

    for d in range(first.day, last.day + 1, 1):  # 月の初めから最後までループ

        iter_date = today + relativedelta(months=target_month) - datetime.timedelta(
            days=get_month.day - d)  # iが増えることで日も増える

        holiday_name = jholiday.holiday_name(date=iter_date)
        """
        datetimeから曜日を取得
        weekdayと曜日の対応     
        0: 月, 1: 火, 2: 水, 3: 木, 4: 金, 5: 土, 6: 日
        """
        """
        属性の値　data-timeline = "x" ←　以下から該当する数字をxに記入する

        1: 応接室,　2: 大会議室,　3: SouthTerrace,　4: Core-A　6: 事業部長会議室　
        7: N-A,　8: N-B, 9: N-C, 10: N-D, 11:N-E, 12: N-F 
        13: S-A,　14: S-B, 15: S-C, 16: S-D, 17: S-E
        """
        try:
            if holiday_name is None and not iter_date.weekday() == 5 and not iter_date.weekday() == 6: #祝日以外、平日のとき
                """
                    N-E　平日　9:30-11:00を予約
    
                """
                start_time = '09:30'  # ここを変える
                end_time = '11:00'  # ここを変える

                if iter_date.weekday() == 0:
                    day_name = '(月)'
                elif iter_date.weekday() == 1:
                    day_name = '(火)'
                elif iter_date.weekday() == 2:
                    day_name = '(水)'
                elif iter_date.weekday() == 3:
                    day_name = '(木)'
                elif iter_date.weekday() == 4:
                    day_name = '(金)'


                driver.find_element_by_link_text(str(d)).click()
                driver.implicitly_wait(10)
                driver.find_element_by_xpath('//div[@class="tl ui-selectee"][@data-timeline="2"]').click()  # 大会議室を選択 ここを変える
                # 時間選択
                start_time_element = driver.find_element_by_name('StartTime')
                select_start_time = Select(start_time_element)
                select_start_time.select_by_value(start_time)
                end_time_element = driver.find_element_by_name('EndTime')
                select_end_time = Select(end_time_element)
                select_end_time.select_by_value(end_time)
                # 目的選択
                purpose = driver.find_element_by_name('PurposeCode')
                select_purpose = Select(purpose)
                select_purpose.select_by_value('1')
                driver.find_element_by_name("NumberOfUsers").send_keys('10')
                # 予約ボタン押下
                driver.find_element_by_xpath('//button[@class="btn blue submit-form-new"][@type="button"]').click()
                driver.implicitly_wait(10)

                # ダブルブッキングした場合
                alert_msg = driver.find_element_by_xpath('//section[@class="alert error active"]')

                if alert_msg:
                    print(str(iter_date) + " " + day_name + " " + '大会議室 ' + str(start_time) + '-' + str(end_time) + ' は既に取られています')
                    driver.find_element_by_xpath('//div[@class="btnCircle close"][@id="close-entry"]').click()
                    driver.implicitly_wait(10)
                else:
                    print(str(iter_date) + " " + day_name + " " + '大会議室 ' + str(start_time) + '-' + str(end_time) + ' の予約完了')


        except selenium.common.exceptions.UnexpectedAlertPresentException:
            print(str(iter_date) + " " + day_name + " " + str(start_time) + '-' + str(end_time) + ' は祝日です')
        except NoSuchElementException:
            print("属性が見つかりませんでした。")
        except ElementNotInteractableException:
            print("クリックできませんでした。")


if __name__ == '__main__':
    my_mtg()
    #oms_mtg()
