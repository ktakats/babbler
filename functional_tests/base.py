from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
import sys
from channels.test import ChannelLiveServerTestCase

#For testing locally two redis instances are necessary. See https://gist.github.com/ctavan/4482825

class FunctionalTest(ChannelLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                cls.against_staging = True
                return
        super(FunctionalTest, cls).setUpClass()
        cls.against_staging = False
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super(FunctionalTest, cls).tearDownClass()

    def setUp(self):
        self.browser = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
        self.browser.implicitly_wait(20)

    def tearDown(self):
        self.browser.quit()
        super(FunctionalTest, self).tearDown()

    def create_session(self, id):
        session = SessionStore()
        session[SESSION_KEY] = id
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