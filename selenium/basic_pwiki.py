# coding: utf-8
# pylint: disable=C0103

"""SKP Wiki comment automation
"""

import time
import getpass

from selenium import webdriver
import pandas as pd

class PWikiScraper:
    """SKP Wiki Scraper Class"""
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

        self.driver.get('http://wiki.skplanet.com/login.action')
        time.sleep(1)
        element = self.driver.find_element_by_id('os_username')
        element.send_keys(user_id)
        element = self.driver.find_element_by_id('os_password')
        element.send_keys(user_pw)
        element = self.driver.find_element_by_id('loginButton')
        element.click()
        time.sleep(1)

        # check success
        if self.driver.current_url != 'http://wiki.skplanet.com/':
            print(self.driver.current_url)
            self.is_login_problem = True
            return False

        self.is_login = True
        return True


    def comment_sandbox(self):
        """comment_sandbox
        """
        self.driver.get('http://wiki.skplanet.com/display/O2Osd/Sandbox01')
        element = self.driver.find_element_by_css_selector('div.quick-comment-prompt')
        element.click()
        element.screenshot('pwiki.png')
        return


if __name__ == '__main__':
    uid = input('ID : ')
    upw = getpass.getpass('Password : ')
    scraper = PWikiScraper()
    if scraper.login(uid, upw):
        scraper.comment_sandbox()
