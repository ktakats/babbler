from .base import FunctionalTest

class SimpleChatTest(FunctionalTest):

    def test_simple_chat(self):

        #There's a new chat web app! Alice goes to check it out
        self.browser.get(self.server_url)

        #Here she sees an input field and a send button
        #she writes a message and sends it
        self.browser.find_element_by_id('id_message').send_keys("Hello world!")
        self.browser.find_element_by_id('id_send').click()

        #Her message shows up on the screen
        chatbox=self.browser.find_element_by_id("id_chat").text
        self.assertContains("Hello world!", chatbox)

        self.fail()