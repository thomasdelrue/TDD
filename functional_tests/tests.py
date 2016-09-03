import sys

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(StaticLiveServerTestCase):

	@classmethod
	def setUpClass(cls):
		for arg in sys.argv:
			if 'liveserver' in arg:
				cls.server_url = 'http://'+ arg.split('=')[1]
				cls.live_server_url = cls.server_url
				return
		super().setUpClass()
		cls.server_url = cls.live_server_url
		
	@classmethod
	def tearDownClass(cls):
		if cls.server_url == cls.live_server_url:
			super().tearDownClass()
			
	
	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)
	
	def tearDown(self):
		self.browser.quit()
		
	def check_for_row_in_list_table(self, row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows])
		
	def test_can_start_a_list_and_retrieve_it_later(self):
		# Edith has heard about a cool new online to-do app. She goes
		# to check out its homepage
		self.browser.get(self.server_url)

		# She notices the page title and header mention to-do lists
		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)

		# She is invited to enter a to-do item straight away
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a to-do item'
		)

		# She types "Buy peacock food" into a text box (Edith's hobby
		# is feeding peacocks at a shelter)
		inputbox.send_keys('Buy peacock food')
		
		# When she hits enter, she is taken to a new URL, 
		# and now the page lists "1: Buy peacock food" as an item in a 
		#to-do list table
		inputbox.send_keys(Keys.ENTER)
		edith_list_url = self.browser.current_url
		self.assertRegex(edith_list_url, '/lists/.+')
		self.check_for_row_in_list_table('1: Buy peacock food')
		
		# There is still a text box inviting her to add another item. She
		# enters "Bring peacock food to the shelter" (Edith is very methodical)
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Bring peacock food to the shelter')
		inputbox.send_keys(Keys.ENTER)
		
		# The page updates again, and now shows both items on her list
		self.check_for_row_in_list_table('1: Buy peacock food')
		self.check_for_row_in_list_table('2: Bring peacock food to the shelter')
		
		# Now a new user, Francis, comes along to the site

		## We use a new browser session to make sure that no information
		## of Edith's is coming through from cookies etc #
		self.browser.quit()
		self.browser = webdriver.Firefox()
		
		# Francis visits the home page. There is no sign of Edith's
		# list
		self.browser.get(self.server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock food', page_text)
		self.assertNotIn('Bring peacock food to the shelter', page_text)
		
		# Francis starts a new list by entering a new item. He 
		# is less interesting than Edith
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy soy milk')
		inputbox.send_keys(Keys.ENTER)
		
		# Francis gets his own unique URL
		francis_list_url = self.browser.current_url
		self.assertRegex(francis_list_url, '/lists/.+')
		self.assertNotEqual(francis_list_url, edith_list_url)
		
		# Again, there is no trace of Edith's list
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock food', page_text)
		self.assertIn('Buy soy milk', page_text)
		
		# Satisfied, they both go back to sleep
		
		
	def test_layout_and_styling(self):
		# Edith goes to the home page
		self.browser.get(self.server_url)
		self.browser.set_window_size(1024, 768)
		
		# She notices the input box is nicely centered
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2,
			512, delta=10)
			
		# She starts a new list and sees the input is nicely 
		# centered there too
		inputbox.send_keys('testing\n')
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2,
			512, delta=10)
