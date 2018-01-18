from .base import FunctionalTest

class SignupAndLogin(FunctionalTest):

    def test_signup_and_login(self):
        # There's a new chat web app! Alice goes to check it out
        self.browser.get(self.server_url)
        # check_for_bad_request(self)
        alice_browser = self.browser

        #She realizes that she needs to sign up
        self.browser.find_element_by_link_text('Sign up').click()
        self.browser.find_element_by_id('id_email').send_keys('alice@bla.com')
        self.browser.find_element_by_id('id_first_name').send_keys('Alice')
        self.browser.find_element_by_id('id_password1').send_keys('blabla')
        self.browser.find_element_by_id('id_password2').send_keys("blabla")
        self.browser.find_element_by_id('id_signup').click()

        body=self.browser.find_element_by_tag_name('body').text
        self.assertIn('Hi, Alice', body)
        self.assertIn('Logout', body)

        #She logs out
        self.browser.find_element_by_link_text("Logout").click()
        body = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Sign up', body)
        self.assertNotIn('Hi Alice', body)

        #At her next visit, she can simply log in with the form on the home page
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_email').send_keys('alice@bla.com')
        self.browser.find_element_by_id('id_password').send_keys('blabla')
        self.browser.find_element_by_id('id_login').click()
        #Now she's logged in and create rooms
        body=self.browser.find_element_by_tag_name('body').text
        self.assertIn('Hi, Alice', body)