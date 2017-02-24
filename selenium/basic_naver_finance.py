# coding: utf-8
# pylint: disable=C0103

"""Naver My finance scraper
"""

import time
import getpass

from selenium import webdriver
import pandas as pd

class NaverScraper:
    """Naver Scraper Class"""
    driver = webdriver.PhantomJS()
    is_login = False
    is_login_problem = False

    def login(self, user_id, user_pw):
        """login ==> Boolean
        Login with given id and password.
        set is_login_problem to True with failure
        Return : True/False
        """
        # check login
        if self.is_login:
            return True
        # STOP when login error!
        if self.is_login_problem:
            print("Login is failure!")
            return False

        self.driver.get('http://www.naver.com')
        time.sleep(1)  # human like sleep
        self.driver.get('https://nid.naver.com/nidlogin.login?url=http%3A%2F%2Fwww.naver.com')
        time.sleep(1)
        element = self.driver.find_element_by_id('id')
        element.send_keys(user_id)
        element = self.driver.find_element_by_id('pw')
        element.send_keys(user_pw)
        element = self.driver.find_element_by_css_selector('input.btn_global')
        element.click()
        time.sleep(1)

        # check success
        if self.driver.current_url != 'http://www.naver.com/':
            print(self.driver.current_url)
            self.is_login_problem = True
            return False

        self.is_login = True
        return True


    def get_stock_index(self):
        """Return index of stock market
        Return : pandas DataFrame object
        """
        self.driver.get('http://finance.naver.com')
        element = self.driver.find_element_by_class_name('section_stock_market')
        els = element.text.split('\n')
        keys = ['코스피', '코스닥', '코스피200']
        results = []
        for key in keys:
            idx = els.index(key)
            results.append([els[idx],
                            els[idx+1].split()[0],
                            els[idx+2] + els[idx+1].split()[1],
                            els[idx+3] + els[idx+4]])

        df_result = pd.DataFrame(results)
        return df_result


    def get_my_finance(self):
        """Return stock valuation in my finance
        Login with login() is needed.
        Return : pandas DataFrame object
        """
        if not self.is_login:
            print('Login is needed! Call login() before.')
            return

        self.driver.get('http://finance.naver.com/mystock/itemList.nhn')
        time.sleep(1)

        self.driver.save_screenshot('my_finance_items.png')

        tbl = self.driver.find_element_by_css_selector('.section_mys .group_mystb .tb_area table')
        df_tbl = pd.read_html('<table>' + tbl.get_attribute('innerHTML') + '</table>')
        return df_tbl[0]

if __name__ == '__main__':
    uid = input('NAVER ID : ')
    upw = getpass.getpass('Password : ')
    scraper = NaverScraper()
    if scraper.login(uid, upw):
        stock_index = scraper.get_stock_index()
        my_finance = scraper.get_my_finance()

        writer = pd.ExcelWriter('finance_%s.xlsx' % (time.strftime('%m%d%H%M%S')))
        stock_index.to_excel(writer, 'stock_index')
        my_finance.to_excel(writer, 'my_finance')
        writer.save()
