from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from django.contrib.auth.models import User
from ...models import AboutMe
from django.test import LiveServerTestCase
import time


class AboutMeTest(LiveServerTestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user('username', 'email@example.com', 'password')
        self.user.save()

        # op = webdriver.ChromeOptions()
        # op.add_argument('headless')
        self.browser = webdriver.Chrome()

    def tearDown(self) -> None:
        self.browser.quit()

    def login_user_visit(self, url: str):
        self.client.force_login(self.user)
        cookies = self.client.cookies["sessionid"]
        self.browser.get(self.live_server_url + url)
        self.browser.add_cookie({"name": "sessionid", "value": cookies.value, "secure": False, "path": "/"})
        self.browser.refresh()

    def labels_in_form(self, expected_labels):
        form_labels = self.browser.find_elements(By.TAG_NAME, "label")

        find_labels = [labels.text for labels in form_labels]
        self.assertEqual(expected_labels, find_labels)

    def completed_form_fields(self, field_data: dict):
        for k, v in field_data.items():
            form_inputbox = self.browser.find_element(By.ID, k)
            form_inputbox.send_keys(v)

    def finding_data_on_page(self, expected_data: dict):
        for k, v in expected_data.items():
            search_dom_element = self.browser.find_element(By.ID, k)

            self.assertEqual(search_dom_element.text, v)

    def test_can_user_create_about_me(self):
        # Give
        # Loged user without 'about me' visit the website
        # in 'portfolio' index

        self.login_user_visit("/portfolio/")

        # He notices which the title of the browser tab is "Portfolio"
        page_title = self.browser.title
        self.assertEqual(page_title, "Portfolio")

        # He notices a heading that says "About me".
        heading_about = self.browser.find_element(By.ID, "heading-about")
        self.assertEqual(heading_about.text, "About me")

        # and a button 'add about me'
        add_button = self.browser.find_element(By.ID, "add_aboutme")
        self.assertEqual(add_button.text, "Add about me")

        # when he clicked the button is redirected to '/portfolio/edit'
        add_button.click()
        self.browser.implicitly_wait(1)
        edit_url = self.browser.current_url
        self.assertEqual(edit_url, self.live_server_url + "/portfolio/edit/")

        # He notices a form whit Fullname, About and Picture fields
        expected_labels = ['First name:', 'Last name:', 'About:', 'Picture:']
        self.labels_in_form(expected_labels)

        # When completes the form fields
        field_data = {"id_firstname": "Test name", "id_lastname": "test surname",
                      "id_about": "I am a test user to testing",
                      "id_picture": "/home/maximo/Firefox_wallpaper.png"}

        self.completed_form_fields(field_data)

        # And sends the form
        submit_button = self.browser.find_element(By.ID, "submit")
        time.sleep(1)
        submit_button.click()

        # Then is redirected to '/portfolio/' and saw appear the data on the page
        portfolio_url = self.browser.current_url
        self.assertEqual(portfolio_url, self.live_server_url + "/portfolio/")

        search_data_in_page = {
            "create_name": field_data["id_firstname"], "create_lastname": field_data["id_lastname"]
            , "create_about": field_data["id_about"]
        }
        self.finding_data_on_page(search_data_in_page)

        create_img = self.browser.find_element(By.ID, "create_img")
        self.assertTrue(create_img.is_displayed())

    def test_can_view_about_data_if_created(self):
        # User with a about me created visit '/portfolio'
        about_me = AboutMe(user=self.user, firstname="testname", lastname="lastname", about="about me",
                           picture="/home/maximo/Firefox_wallpaper.png")
        about_me.save()
        self.login_user_visit("/portfolio")

        # He notices which the title of the browser tab is "Portfolio"
        page_title = self.browser.title
        self.assertEqual(page_title, "Portfolio")

        # He notices a heading that says "About me".
        heading_about = self.browser.find_element(By.ID, "heading-about")
        self.assertEqual(heading_about.text, "About me")

        # Then he saw appear the data on the page
        search_data_in_page = {
            "create_name": "testname", "create_lastname": "lastname"
            , "create_about": "about me"
        }
        self.finding_data_on_page(search_data_in_page)

        create_img = self.browser.find_element(By.ID, "create_img")
        self.assertTrue(create_img.is_displayed())