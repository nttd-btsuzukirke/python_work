#! python3

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import datetime
from dateutil.relativedelta import relativedelta
import calendar

driver = webdriver.Ie('C:/Users/U621625/PycharmProjects/Work/selenium/webdriver/IEDriverServer.exe')

#ログイン画面開く
url='https://gg2.groupwide.net/iMRRoomBooking/'

driver.get(url)

#ログイン情報記入
login_id = ''
com_id = ''
password = ''

"""
LOGIN
"""
driver.find_element_by_name("id1").send_keys(login_id) #idボックスのを探し入力
driver.find_element_by_name("id2").send_keys(com_id) #会社識別子ボックスを探し入力
driver.find_element_by_name("password").send_keys(password) #パスワードボックスを探し入力
driver.find_element_by_xpath("//input[@title='Login'][@type='submit']").click() #Loginボタン押下
time.sleep(5)

#何ヶ月後を予約するかを指定
target_month = 2

#2ヶ月先まで表示するには二回Nextボタン押す必要あり
for i in range(target_month):
    driver.implicitly_wait(10)  # 見つからないときは、10秒まで待つ
    driver.find_element_by_link_text("Next").click() #Nextボタン押下
    time.sleep(3)

"""
会議室を取る日にちを決める
"""
today = datetime.date.today()  # datetimeから日付を取得

get_month = today + relativedelta(months=target_month)


def get_dates():
    """
    最初の日と最後の日を調べる

    """
    # 会議室を取る月の初日を求める
    first_date = get_month - datetime.timedelta(days=today.day - 1)
    # 会議室を取る月の最終日を求める
    last_date = first_date + relativedelta(months=1) + datetime.timedelta(days=-1)

    return first_date, last_date


first, last = get_dates()


for i in range(first.day, last.day+1, 1): # 月の初めから最後までループ

    iter_date = today + relativedelta(months=target_month) - datetime.timedelta(days=get_month.day - i) # iが増えることで日も増える
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

    if iter_date.weekday() == 1: #火曜日だったら以下を予約
        """
                     大会議室　火曜　11:00-12:00を予約

        """
        start_time = '11:00'
        end_time = '12:00'
        day_name = '(火)'
        driver.find_element_by_link_text(str(i)).click()  # 日付指定
        driver.find_element_by_xpath('//div[@class="tl ui-selectee"][@data-timeline="2"]').click()  # 二行目(大会議室)を選択
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

        #except NoSuchElementException:
        #    print("属性が見つかりませんでした。")

        #ダブルブッキングした場合
        alert_msg = driver.find_element_by_xpath('//section[@class="alert error active"]')
        if alert_msg:
            print(str(iter_date) + " " + day_name + " " + str(start_time) + '-' + str(end_time) + ' is already booked.')
            driver.find_element_by_xpath('//div[@class="btnCircle close"][@id="close-entry"]').click()


        """
                    大会議室　火曜　14:00-15:00を予約
        """
        start_time = '14:00'
        end_time = '15:00'
      
        driver.find_element_by_link_text(str(i)).click()  # 日付指定
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
        #driver.find_element_by_class_name("btnbluesubmit-form-new").click()
        # 予約ボタン押下
        driver.find_element_by_xpath('//button[@class="btn blue submit-form-new"][@type="button"]').click()

        # ダブルブッキングした場合
        if alert_msg:
            print(str(iter_date) + " " + day_name + " " + str(start_time) + '-' + str(end_time) + ' is already booked.')
            driver.find_element_by_xpath('//div[@class="btnCircle close"][@id="close-entry"]').click()


    elif iter_date.weekday() == 4: # 木曜だったら以下を予約
        """
                    South Terrace 木曜　16:00-18:00を予約
        """
        start_time = '16:00'
        end_time = '18:00'
        day_name = '(木)'
        driver.find_element_by_link_text(str(i)).click()  # 日付指定
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

        # ダブルブッキングした場合
        if alert_msg:
            print(str(iter_date) + " " + day_name + " " + str(start_time) + '-' + str(end_time) + ' is already booked.')
            driver.find_element_by_xpath('//div[@class="btnCircle close"][@id="close-entry"]').click()










