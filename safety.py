# Generated by Selenium IDE
from asyncore import poll
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import sys, os
import winsound as sd
from bs4 import BeautifulSoup

url = "https://lc.multicampus.com/safetyedu-samsung/"

timeout_wait = 2
time_sleep = 5
poll_frequency = 0.01

try:
    f = open('settings.ini', 'rt', encoding='utf-8')
    infos = f.read().splitlines()
    id = infos[0]
    pw = infos[1]
    timeout_wait = float(infos[2])
    time_sleep = float(infos[3])
    poll_frequency = float(infos[4])
    f.close()
except FileNotFoundError:
    pass
except IndexError:
    pass

page_1, page_2, page_3 = 0, 0 ,0


class Selenium():
  def __init__(self):
      super().__init__()
      
  def setup_method(self, method):
      # flag = 0x08000000  # No-Window flag
      # flag = 0x00000008  # Detached-Process flag, if first doesn't work

      options = webdriver.ChromeOptions()
      options.add_experimental_option("excludeSwitches", ["enable-logging"]) # 필요없는 로그 없애기 https://scribblinganything.tistory.com/20
      # usb_device_handle_win.cc:1020 Failed to read descriptor from node connection:  시스템에 부착된 장치가 작동하지 않습니다.

      options.add_argument("--start-maximized") #헤드리스 시에는 적용이 안된다..
      args = ["hide_console", ] #셀레니움으로 브라우저를 키면 콘솔창이 뜨는데, 파일을 수정해 추가 옵션을 넣어 콘솔을 뜨지 않게 해줌.

      self.driver = webdriver.Chrome('./chromedriver', service_args=args, options=options)

  #셀레니움 종료
  def teardown_method(self, method):
      self.driver.quit()
  
  def wait_for_window(self, timeout = 2):
    time.sleep(round(timeout / 1000))
    wh_now = self.driver.window_handles
    wh_then = self.vars["window_handles"]
    if len(wh_now) > len(wh_then):
      return set(wh_now).difference(set(wh_then)).pop()
  
  def test_untitled(self):

    self.login()
    sleep(time_sleep)
    self.start()
    sleep(time_sleep)
    self.play()
  
  def login(self):
    self.driver.get(url)
    sleep(time_sleep)
    
    elem = WebDriverWait(self.driver, timeout_wait, poll_frequency).until(
      EC.visibility_of_element_located(
        (By.XPATH, "//input[@placeholder='Knox ID를 입력하세요.']")))
    elem.send_keys(id)
    
    elem = WebDriverWait(self.driver, timeout_wait, poll_frequency).until(
      EC.visibility_of_element_located(
        (By.XPATH, "//input[@placeholder='비밀번호를 입력해주세요.']")))
    elem.send_keys(pw)

    self.driver.find_element(By.CSS_SELECTOR, ".login-btn").click()

  def start(self):
    page_1 = self.driver.current_window_handle
    
    self.driver.find_element(By.CSS_SELECTOR, ".btn-type01").click()
    sleep(time_sleep)
    
    for handle in self.driver.window_handles:
      if handle != page_1:
          page_2 = handle
    
    self.driver.switch_to.window(page_2)
    
    self.driver.find_element(By.ID, "btnNextLrn").click()
    sleep(time_sleep)
    
    for handle in self.driver.window_handles:
      if handle != page_1 and handle != page_2:
          page_3 = handle
    
    self.driver.switch_to.window(page_3)
    
  def play(self):
    while True:
      # html에서 찾기
      soup=BeautifulSoup(self.driver.page_source, 'html.parser')
      time_current = soup.find("span", "fp-elapsed").text
      time_finish = soup.find("span", "fp-duration").text
      if time_current == time_finish:
        sleep(time_sleep/2)
        self.driver.find_element(By.CLASS_NAME, "next-link").click()
        try:
          sleep(time_sleep/2)
          elem = self.driver.find_element(By.XPATH, "//button[starts-with(@id,'btnOk')]")
          # self.driver.execute_script("arguments[0].click();", elem)
          elem.click()
        except Exception as e:
          print(e)
          pass
      sleep(time_sleep)

  

if __name__ == "__main__":
  selenium = Selenium() #셀레니움 객체 생성
  selenium.setup_method(1)
  sleep(time_sleep)
  selenium.test_untitled()
