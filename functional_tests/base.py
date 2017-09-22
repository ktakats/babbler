from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
import sys
from channels.test import ChannelLiveServerTestCase
from django.contrib import auth

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

    def create_preauthenticated_session(self, email, password, first_name):
        user=User.objects.create_user(email=email, password=password, first_name=first_name)
        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session.save()
        ## to set a cookie we need to first visit the domain.
        ## 404 pages load the quickest!
        self.browser.get(self.server_url)
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session.session_key,
            path='/',
        ))
        return self.browser