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

    def gerar():
        ficheiro = open(HTML,"w")

        i=0
        ficheiro.write("<html>\n<head>\n<title>" + TITLE + "</title>\n</head>\n<body>\n<b><center>" + TITLE + "</b>\n</font>\n<br><br>\n")
        for thumb in imgthumb:
            i=i+1
            print str(i) + " imagem inserida na pagina"
            ficheiro.write(thumb)
        ficheiro.write("\n</body>\n</html>")
        ficheiro.close()


    def test_insecure(self):
        URL = json.loads(open('testinsecure.json').read())

        count=0
        while(count < len(URL['bd'])):
            driver = self.driver
            #vuln ="<script>alert(\"XSS\")</script>"
            driver.get(URL['url'] + URL['var'][0] + URL['bd'][count])
            try:
                WebDriverWait(driver, 3).until(EC.alert_is_present(),
                                       'Timed out waiting for PA creation ' +
                                       'confirmation popup to appear.')
                alert = driver.switch_to_alert()
                alert.accept()
                print "alert accepted - "+URL['bd'][count]
            except TimeoutException:
                print "no alert - "+URL['bd'][count]

            count=count+1

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
