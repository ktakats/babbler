from .base import FunctionalTest
from selenium import webdriver
import time

def check_for_bad_request(self):
    body=self.browser.find_element_by_tag_name('body').text
    if "Bad Request" in body:
        self.browser.refresh()

class SimpleChatTest(FunctionalTest):

    def test_simple_chat(self):

        #There's a new chat web app! Alice goes to check it out
        self.browser.get(self.server_url)
        check_for_bad_request(self)
        alice_browser=self.browser

        #at the same time Bob opens a browser too
        bob_browser = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
        self.browser=bob_browser
        self.browser.get(self.server_url)
        check_for_bad_request(self)

        #Alice sees an input field and a send button
        #she writes a message and sends it
        self.browser=alice_browser
        self.browser.find_element_by_id('id_message').send_keys("Hello world!")
        self.browser.find_element_by_id('id_send').click()
        time.sleep(0.5)
        #Her message shows up on the screen
        body=self.browser.find_element_by_tag_name("body").text
        self.assertIn("Hello world!", body)

        #At the same time Bob can see the same message, too!
        self.browser=bob_browser

        body = self.browser.find_element_by_tag_name("body").text
        self.assertIn("Hello world!", body)
        #He decides to answer
        self.browser.find_element_by_id('id_message').send_keys("Hola Alice!")
        self.browser.find_element_by_id('id_send').click()
        time.sleep(0.5)
        #Which Alice can read
        self.browser=alice_browser
        body = self.browser.find_element_by_tag_name("body").text
        self.assertIn("Hola Alice!", body)
