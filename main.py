from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyperclip
import time
import schedule

'''
    id: 아이디
    pw: 비밀번호
    registrations
        실패시 시도할 분반을 리스트로 작성해주세요
        [[A,B],[C,D]]는 A->C->B->D 순으로 시도합니다.
    
    * 모든 필드는 숫자가 아닌 문자열이어야합니다.
    ex) ['CB15037',0](X) ['CB15037','000'](O)
'''
user_data = {
    'id': '44124066',
    'pw': '020404',
    'registrations': [
        [['ZE10115','219'],['test','a']],
        [['CB15037','100']]
    ],
}

option = {
    'delay': 0.7,
    'start_at': '10:00'
}

def set_value_by_id(id, value):
    '''
    driver.find_element_by_id(id).send_keys(value)
    '''
    pyperclip.copy(value)
    driver.find_element_by_id(id).click()
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('a').send_keys(Keys.BACKSPACE).send_keys('v').key_up(Keys.CONTROL).perform()

def get_succeeded_list():
    dgSinchungList = driver.find_element_by_id('dgSinchungList')
    return dgSinchungList.find_elements_by_tag_name('tr')[1:]

def prepare_login(userid,userpw):
    driver.get('https://sugang.pusan.ac.kr/sugang/login.aspx')
    set_value_by_id('txtid',userid)
    set_value_by_id('txtpassword',userpw)

def login():
    driver.find_element_by_id('btnlogin').click()
    try:
        alert = driver.switch_to_alert()
        print("alert: " + alert.text)
        alert.accept()
        alert.dismiss()
    except:
        pass

def register_course(registration):
    old = len(get_succeeded_list())
    set_value_by_id('txtCode',registration[0])
    set_value_by_id('txtBunban',registration[1])
    driver.find_element_by_id('btninsert').click()
    time.sleep(option['delay'])
    return old != len(get_succeeded_list())

def tostring_registration(registration):
    return registration[0]+'-'+registration[1]

def register_course_by_user_data():
    login()

    failed = user_data['registrations']
    
    while len(failed) != 0:
        todo = failed
        failed = []

        for registration_list in todo:
            if register_course(registration_list[0]):
                print('성공: ' + tostring_registration(registration_list[0]))
            else:
                if len(registration_list) == 1:
                    print('실패: ' + tostring_registration(registration_list[0]))
                else:
                    print('실패: ' + tostring_registration(registration_list[0]) + ' => ' + tostring_registration(registration_list[1]))
                    failed.append(registration_list[1::])
    
    print('성공 과목수: '+driver.find_element_by_id('txtCount').get_attribute("value")+'/'+str(len(user_data['registrations'])))
    print('학점: '+driver.find_element_by_id('txtCurrent').get_attribute("value"))
    print('Ctrl+C를 눌러 프로그램을 종료합니다.')

options = EdgeOptions()
options.use_chromium = True
options.add_extension('./pass-macro-check.crx')
driver = Edge(executable_path='./edgedriver_win64/msedgedriver.exe', options=options, desired_capabilities=DesiredCapabilities.EDGE)

prepare_login(user_data['id'],user_data['pw'])
schedule.every().day.at(option['start_at']).do(register_course_by_user_data)

while True:
    schedule.run_pending()
    time.sleep(0.01)
