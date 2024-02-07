from django.test import LiveServerTestCase
from django.contrib.auth.models import User
from selenium import webdriver
from selenium.webdriver.common.by import By


class BaseTest(LiveServerTestCase):

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
        self.browser.implicitly_wait(3)
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