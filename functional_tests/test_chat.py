from .base import FunctionalTest
from selenium import webdriver
import time

def check_for_bad_request(self):
    body=self.browser.find_element_by_tag_name('body').text
    if "Bad Request" in body:
        self.browser.refresh()

class SimpleChatTest(FunctionalTest):

    def test_simple_room_chat(self):

        #There's a new chat web app! Alice goes to check it out
        self.browser.get(self.server_url + '/room/main/')
        check_for_bad_request(self)
        alice_browser=self.browser

        #at the same time Bob opens a browser too
        bob_browser = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
        self.browser=bob_browser
        self.browser.get(self.server_url + '/room/main/')
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

        #But then Alice changes to another room and sends a message there
        self.browser.get(self.server_url + '/room/other/')
        self.browser.find_element_by_id('id_message').send_keys("Hola people!\n")
        time.sleep(0.5)

        #And since Bob is in the first room, he can't see it
        self.browser=bob_browser
        body = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("Hola people!", body)

