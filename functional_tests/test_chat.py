from .base import FunctionalTest
from selenium import webdriver
import time
from django.contrib.auth import get_user_model
from friendship.models import Friend


User=get_user_model()


def quit_if_possible(browser):
    try:
        browser.quit()
    except:
        pass

def add_friend(browser, email):
    browser.find_element_by_link_text('Find friends').click()
    browser.find_element_by_id('id_email').send_keys(email)
    browser.find_element_by_id('id_search').click()
    browser.find_element_by_id('id_invite').click()

def accept_friend_request(browser):
    browser.find_element_by_class_name('fa-envelope-o').click()
    browser.find_element_by_id('id_accept').click()

def add_new_room(browser, title, add_user=False):
    browser.find_element_by_id('id_title').send_keys(title)
    if add_user:
        browser.find_element_by_id('id_users_0').click()
    browser.find_element_by_id('id_create_room').click()

class SimpleChatTest(FunctionalTest):

    def test_room_chat(self):

        #There's a new chat web app! Alice, Bob and Cecilia goes to check it out
        self.go_to_page_and_log_in('alice@example.com', password='alicepassword', first_name='Alice')
        alice_browser=self.browser
        self.browser = webdriver.Firefox()
        self.go_to_page_and_log_in('bob@example.com', password='bobpassword', first_name='Bob')
        bob_browser = self.browser
        self.browser = webdriver.Firefox()
        self.go_to_page_and_log_in('cecilia@example.com', password='ceciliapassword', first_name='Cecilia')
        cecilia_browser = self.browser

        #Alice and Bob know each other, so Alice invites Bob to be her friend
        add_friend(alice_browser, 'bob@example.com')

        #Bob can see that he has an invite
        self.browser=bob_browser
        self.browser.get(self.server_url)
        accept_friend_request(self.browser)

        #Alice decides to start a chat room
        self.browser=alice_browser
        self.browser.get(self.server_url)

        #Bob is in the list, but Cecilia is not
        time.sleep(10)
        self.browser.find_element_by_class_name('add-new-room').click()
        body=self.browser.find_element_by_tag_name('body').text
        self.assertIn('Bob', body)
        self.assertNotIn('Cecilia', body)

        add_new_room(self.browser, 'Testroom', add_user=True)

        #It creates the room and and opens it
        title=self.browser.find_element_by_tag_name('title').text
        self.assertEqual(title, 'Testroom')

        #Bob sees the room listed, and goes there
        self.browser=bob_browser
        self.browser.get(self.server_url)
        self.browser.find_element_by_class_name("room").click()
        title = self.browser.find_element_by_tag_name('title').text
        self.assertEqual(title, 'Testroom')
        #check_for_bad_request(self)

        #Alice sees an input field and a send button
        #she writes a message and sends it
        self.browser=alice_browser
        self.browser.find_element_by_id('id_text').send_keys("Hello world!")
        self.browser.find_element_by_id('id_send').click()
        #time.sleep(0.5)
        #Her message shows up on the screen
        body=self.browser.find_element_by_tag_name("body").text
        self.assertIn("Hello world!", body)

        #At the same time Bob can see the same message, too!
        self.browser=bob_browser

        body = self.browser.find_element_by_tag_name("body").text
        self.assertIn("Hello world!", body)
        self.assertIn("Alice", body)

        #He decides to answer
        self.browser.find_element_by_id('id_text').send_keys("Hola Alice!")
        self.browser.find_element_by_id('id_send').click()
        time.sleep(0.5)
        #Which Alice can read
        self.browser=alice_browser
        body = self.browser.find_element_by_tag_name("body").text
        self.assertIn("Hola Alice!", body)

        #But then Alice changes to another room and sends a message there
        self.browser.get(self.server_url+'/new_room/')
        add_new_room(self.browser, 'other')

        #check_for_bad_request(self)
        self.browser.find_element_by_id('id_text').send_keys("Hola people!")
        self.browser.find_element_by_id('id_send').click()
        time.sleep(0.5)

        #And since Bob is in the first room, he can't see it
        self.browser=bob_browser
        body = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("Hola people!", body)

        #Cecilia can't even see the room
        self.browser=cecilia_browser
        self.browser.get(self.server_url)
        body=self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Testroom', body)


        #cleanup
        self.addCleanup(lambda: quit_if_possible(alice_browser))
        self.addCleanup(lambda: quit_if_possible(bob_browser))
        self.addCleanup(lambda: quit_if_possible(cecilia_browser))

    def test_chat_messages_are_saved(self):

        #Alice goes to the chat app
        alice=self.go_to_page_and_log_in('alice@example.com', password='alicepassword', first_name='Alice')
        bob=User.objects.create_user(email='bob@example.com', password='bobpassword', first_name='Bob')
        alice_browser = self.browser

        Friend.objects.create(from_user=bob, to_user=alice)

        #She creates a room and writes some messages to bob
        self.browser.find_element_by_class_name('add-new-room').click()
        add_new_room(self.browser, 'Testroom', add_user=True)
        self.browser.find_element_by_id('id_text').send_keys("Hola, Bob!")
        self.browser.find_element_by_id('id_send').click()
        self.browser.find_element_by_id('id_text').send_keys("How are you?")
        self.browser.find_element_by_id('id_send').click()
        time.sleep(0.5)

        #She can click a button and go back to the list of rooms
        self.browser.find_element_by_class_name('back-button').click()
        body=self.browser.find_element_by_tag_name('body').text
        self.assertIn('Testroom', body)

        #List of room shows the time of her last message
        room=self.browser.find_element_by_class_name("details").text
        self.assertIn('Alice', room)
        self.assertIn('ago', room)

        #Then she leaves
        self.browser.find_element_by_link_text('Logout').click()

        #Bob logs in
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_email').send_keys('bob@example.com')
        self.browser.find_element_by_id('id_password').send_keys('bobpassword')
        self.browser.find_element_by_id('id_login').click()
        #He can see the main room in the main page, he clicks on it
        self.browser.find_element_by_class_name('room').click()

        #He can see Alice's earlier message
        body=self.browser.find_element_by_tag_name('body').text
        self.assertIn('Hola, Bob!', body)
        self.assertIn("How are you?", body)
        self.assertIn("Alice", body)


class MakeFriends(FunctionalTest):

    def test_making_friends(self):

        #Alice goes to the chat app
        self.go_to_page_and_log_in('alice@example.com', password='alicepassword', first_name='Alice')
        alice_browser=self.browser
        bob = User.objects.create_user(email='bob@example.com', password='bobpassword', first_name='Bob')

        #She can see that she can add friends, so she looks for bob
        self.browser.find_element_by_link_text('Find friends').click()
        self.browser.find_element_by_id('id_email').send_keys('bob@example.com')
        self.browser.find_element_by_id('id_search').click()

        #Bob's name pops up, with a button to invite him
        body=self.browser.find_element_by_tag_name('body').text
        self.assertIn('Bob', body)
        self.browser.find_element_by_id('id_invite').click()

        #Alice logs out
        self.browser.find_element_by_link_text('Logout').click()

        #Bob logs in
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_email').send_keys('bob@example.com')
        self.browser.find_element_by_id('id_password').send_keys('bobpassword')
        self.browser.find_element_by_id('id_login').click()

        #He can see that he has a new friend request
        accept_friend_request(self.browser)

