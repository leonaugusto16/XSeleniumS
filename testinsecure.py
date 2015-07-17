# -*- coding: utf-8 -*-
#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re, json

class Testinsecure(unittest.TestCase):

    #URL = "http://www.insecurelabs.org/" #sys.argv[1] #
    #TAG = "/Search.aspx?query=" #sys.argv[2] #
    #VECTOR = "<script>alert(1)</script>" #sys.argv[3] #
    THUMBSIZE = 230, 153
    HTML = "teste.html"
    TITLE = "XSS" # Alterar para o titulo do site

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        #self.base_url = "http://www.insecurelabs.org/Search.aspx?query=" #sys.argv[1]
        self.verificationErrors = []
        self.accept_next_alert = True

    def treatmenturl(self,URL,count,countt):
        if(countt==0 and len(URL['var'])>0):
            return URL['url'] + URL['var'][0]+"="+ URL['bd'][count]
        if(countt>0 and len(URL['var'])>0):
            return URL['url'] + URL['var'][0]+"=test"+"&"+URL['var'][countt]+"="+URL['bd'][count]
        else:
            print "ERROR: Variable Not Set"
            return 0

    def test_insecure(self):
        URL = json.loads(open('testinsecure.json').read())

        countt=0
        while(countt < len(URL['var'])):
            count=0
            print "\n######### Test Variable "+URL['var'][countt]
            while(count < len(URL['bd'])):
                driver = self.driver
                driver.get(self.treatmenturl(URL,count,countt))
                #driver.get(URL['url'] + URL['var'][countt]+"="+ URL['bd'][count])
                try:
                    WebDriverWait(driver, 1).until(EC.alert_is_present(),
                                           'Timed out waiting for PA creation ' +
                                           'confirmation popup to appear.')
                    alert = driver.switch_to_alert()
                    alert.accept()
                    print "alert accepted - "+URL['bd'][count]
                except TimeoutException:
                    print "no alert - "+URL['bd'][count]
                count=count+1
            countt=countt+1

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True

    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
