from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
import sys
from channels.test import ChannelLiveServerTestCase
from django.contrib import auth
from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY

User=auth.get_user_model()

#For testing locally two redis instances are necessary. See https://gist.github.com/ctavan/4482825



class FunctionalTest(ChannelLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super(FunctionalTest, cls).tearDownClass()

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(20)

    def tearDown(self):
        self.browser.quit()
        super(FunctionalTest, self).tearDown()

    def go_to_page_and_log_in(self, email, password, first_name):
        self.browser.get(self.server_url)
        User.objects.create_user(email=email, password=password, first_name=first_name)
        self.browser.find_element_by_id('id_email').send_keys(email)
        self.browser.find_element_by_id('id_password').send_keys(password)
        self.browser.find_element_by_tag_name('button').click()