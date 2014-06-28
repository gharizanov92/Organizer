from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re
import urllib.request
from utils.db import *
from bson.objectid import ObjectId
import time

def is_unauthorized(element):
    return element.get_attribute('innerHTML') == "Error: 401 Unauthorized"

driver = webdriver.Firefox()
driver.implicitly_wait(40)

class Tests(unittest.TestCase):
    def setUp(self):
        #self.driver = webdriver.Firefox()
        self.base_url = "http://localhost:8080"
        #self.driver.implicitly_wait(20)
        self.verificationErrors = []
        self.accept_next_alert = True


    def test_file_listing_service_security_raises(self):
        self.assertRaises(urllib.error.HTTPError, lambda : urllib.request.urlopen(self.base_url + "/files/all"))

    def test_file_listing_service_security_raises_401(self):
        try:
            urllib.request.urlopen(self.base_url + "/files/all").read()
        except urllib.error.HTTPError as err:
            self.assertEqual(err.code, 401)

    def test_category_listing_service_security_raises(self):
        self.assertRaises(urllib.error.HTTPError, lambda : urllib.request.urlopen(self.base_url + "/categories/all"))

    def test_category_listing_service_security_raises_401(self):
        try:
            urllib.request.urlopen(self.base_url + "/categories/all").read()
        except urllib.error.HTTPError as err:
            self.assertEqual(err.code, 401)

    def test_notes_page_security_raises(self):
        self.assertRaises(urllib.error.HTTPError, lambda : urllib.request.urlopen(self.base_url + "/notes"))

    def test_notes_page_security_raises_401(self):
        try:
            urllib.request.urlopen(self.base_url + "/notes").read()
        except urllib.error.HTTPError as err:
            self.assertEqual(err.code, 401)

    def test_todo_page_security_raises(self):
        self.assertRaises(urllib.error.HTTPError, lambda : urllib.request.urlopen(self.base_url + "/todo"))

    def test_todo_page_security_raises_401(self):
        try:
            urllib.request.urlopen(self.base_url + "/todo").read()
        except urllib.error.HTTPError as err:
            self.assertEqual(err.code, 401)

    def test_manager_page_security_raises(self):
        self.assertRaises(urllib.error.HTTPError, lambda : urllib.request.urlopen(self.base_url + "/manager"))

    def test_manager_page_security_raises_401(self):
        try:
            urllib.request.urlopen(self.base_url + "/manager").read()
        except urllib.error.HTTPError as err:
            self.assertEqual(err.code, 401)


    def test_selenium(self):

        db.users.remove({})
        db.notes.remove({})
        db.todos.remove({})
        driver.get(self.base_url + "/")
        test = driver.find_element_by_id("username")
        driver.find_element_by_id("username").send_keys("test")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("test")
        driver.find_element_by_id("register").click()
        self.assertTrue(self.is_alert_present())
        self.close_alert()

        new_user = db.users.find_one({"username":"test", "password":"test"})
        self.assertTrue(new_user is not None)

        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        self.assertTrue(self.is_element_present("id","menu"))

        id = str(ObjectId())

        driver.find_element_by_id("caption").send_keys("selenium_entry_caption")
        driver.find_element_by_id("body").send_keys("selenium_entry_body")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()

        new_entry = db.notes.find_one({"caption":'selenium_entry_caption'})
        time.sleep(1)
        self.assertTrue(new_entry is not None)
        self.assertTrue(new_entry['caption'] == 'selenium_entry_caption')
        self.assertTrue(new_entry['body'] == 'selenium_entry_body')

        self.assertTrue(self.is_element_present("id",id))
        driver.find_element_by_id(id).click()

        deleted_entry = db.notes.find_one({"caption":'selenium_entry_caption'})
        self.assertTrue(new_entry is None)

        driver.find_element_by_link_text("TODO").click()

        driver.find_element_by_id("text").send_keys("Pay the rent")
        new_entry = db.todos.find({"text":"Pay the rent"})
        #driver.find_element_by_link_text(u"Файлове").click()
        #driver.find_element_by_link_text("Manager").click()
        #driver.find_element_by_link_text(u"Бележки").click()
       
        
    
    def is_element_present(self, how, what):
        driver.find_element(by=how, value=what)
        return True
    
    def is_alert_present(self):
        driver.switch_to_alert()
        return True
    
    def close_alert(self):
        alert = driver.switch_to_alert()
        alert.accept()

if __name__ == "__main__":
    unittest.main()
