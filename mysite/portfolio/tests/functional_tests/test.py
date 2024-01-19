from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
import time
from django.contrib.auth.models import User
from django.test import LiveServerTestCase


class UserCreateAboutMeTest(LiveServerTestCase):

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

    def test_can_user_create_about_me(self):
        # user visit the website and login
        self.login_user_visit("/portfolio")

        # He notices which the title of the browser tab is "Portfolio"
        page_title = self.browser.title
        self.assertEqual(page_title, "Portfolio")

        # He notices a heading that says "About me".
        heading_about = self.browser.find_element(By.ID, "heading-about")
        self.assertEqual(heading_about.text, "About me")

        # He also notices a form whit Fullname, About and Picture fields
        expected_labels = ['First name:', 'Last name:', 'About:', 'Picture:']
        self.labels_in_form(expected_labels)

        # He completes the form fields
        field_data = {"id_firstname": "Test name", "id_lastname": "test surname",
                      "id_about": "I am a test user to testing",
                      "id_picture": "/home/maximo/Firefox_wallpaper.png"}

        self.completed_form_fields(field_data)

        # When he finished sends the form
        submit_button = self.browser.find_element(By.ID, "submit")
        time.sleep(1)
        submit_button.click()
        self.browser.implicitly_wait(1)

        # Then he saw appear the data on the page
        create_name = self.browser.find_element(By.ID, "create_name")
        create_lastname = self.browser.find_element(By.ID, "create_lastname")
        create_about = self.browser.find_element(By.ID, "create_about")
        create_img = self.browser.find_element(By.ID, "create_img")

        self.assertTrue(create_img.is_displayed())

        expected_data = [field_data["id_firstname"], field_data["id_lastname"], field_data["id_about"]]
        find_data = [create_name.text, create_lastname.text, create_about.text]

        self.assertEqual(expected_data, find_data)

        # self.fail('Finish the test!')