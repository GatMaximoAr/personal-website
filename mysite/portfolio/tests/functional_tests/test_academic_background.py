from .base import BaseTest
from ...models import Background
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time


class AcademicBackgroundTest(BaseTest):
    reset_sequences = True

    def test_can_create_academic_background(self):
        # Given a loged user in '/portfolio'
        self.login_user_visit("/portfolio/")

        # He notices which the title of the browser tab is "Portfolio"
        page_title = self.browser.title
        self.assertEqual(page_title, "Portfolio")

        # He notices a heading that says "Academic background".
        heading_academic = self.browser.find_element(By.ID, "heading-academic")
        self.assertEqual(heading_academic.text, "Academic background")

        # and a button 'Add item'
        add_button = self.browser.find_element(By.ID, "add_background")
        self.assertEqual(add_button.text, "Add item")

        # when he clicked the button is redirected to '/portfolio/add/academic-background/'
        add_button.click()
        self.browser.implicitly_wait(1)
        edit_url = self.browser.current_url
        self.assertEqual(edit_url, self.live_server_url + "/portfolio/add/academic-background/")

        # He notices a form whit Title, Institution, degree, Link, start and finish date
        # and picture fields
        expected_labels = ["Title:", 'Institution:', 'Degree:', 'Link:',
                           'Start date:', 'Finish date:', 'Picture:']
        self.labels_in_form(expected_labels)

        # When completes the form fields
        field_data = {"id_title": "Full stack developer", "id_institution": "some school",
                      "id_degree": "test data", "id_link_info": "https://www.google.com",
                      "id_start_date": "2023-04-03", 'id_finish_date': '2023-04-01',
                      "id_picture": "/home/maximo/Firefox_wallpaper.png"}

        self.completed_form_fields(field_data)

        # and send the form
        submit_button = self.browser.find_element(By.ID, "submit")
        time.sleep(1)
        submit_button.click()

        # Then is redirected to '/portfolio/'
        portfolio_url = self.browser.current_url
        self.assertEqual(portfolio_url, self.live_server_url + "/portfolio/")
        # time.sleep(20)

        # and see the new data on page

        academic_background = self.browser.find_element(By.ID, "academic_background_1")
        academic_background.is_displayed()

    def test_can_view_academic_background_if_created(self):
        # Given loged user and exiting academic backgrounds
        background = Background(title="Developer", institution="someone", degree="Bachhelor",
                                start_date="2001-10-21", finish_date="2002-10-23",
                                link_info="www.google.com", picture="/home/maximo/Firefox_wallpaper.png",
                                user=self.user)
        background.save()

        # When he visit '/portfolio/'
        self.login_user_visit("/portfolio/")

        # He notices a heading that says "Academic background".
        heading_experience = self.browser.find_element(By.ID, "heading-academic")
        self.assertEqual(heading_experience.text, "Academic background")

        # Then he see the Academic background of the database

        # if any is not found, an exception is thrown
        background_1 = self.browser.find_element(By.ID, "academic_background_1")

    def test_can_update_academic_background(self):
        # Given loged user and exiting academic backgrounds
        background = Background(title="Developer", institution="someone", degree="Bachelor",
                                start_date="2001-10-21", finish_date="2002-10-23",
                                link_info="https://www.google.com", picture="/home/maximo/Firefox_wallpaper.png",
                                user=self.user)
        background.save()

        # When he visit '/portfolio/'
        self.login_user_visit("/portfolio/")

        # He notices an "edit" button next to the academic background

        background_edit_button = self.browser.find_element(By.ID, "edit_academic_background_1")

        # When he clicked in "edit" button
        background_edit_button.click()

        # is redirected to a work experience form page

        # he notices the url is .../portfolio/edit/experience/1
        current_url = self.browser.current_url
        self.assertEqual(self.live_server_url + "/portfolio/edit/academic-background/1", current_url)

        # He notices that the form has the old data in its fields
        old_data = {"id_title": "Developer", "id_institution": "someone",
                    "id_degree": "Bachelor", "id_start_date": "2001-10-21", "id_finish_date": "2002-10-23",
                    "id_link_info": "https://www.google.com"}

        for k, v in old_data.items():
            input_value = self.browser.find_element(By.ID, k)
            self.assertEqual(input_value.get_attribute("value"), v)

            input_value.clear()

        # When completes the form fields
        field_data = {"id_title": "Developer Junior", "id_institution": "someone",
                      "id_degree": "Bachelor", "id_start_date": "2001-10-21",
                      "id_finish_date": "2002-10-23", "id_link_info": "https://www.google.com",
                      "id_picture": "/home/maximo/Firefox_wallpaper.png"}

        self.completed_form_fields(field_data)

        # and send the form
        submit_button = self.browser.find_element(By.ID, "submit")
        time.sleep(1)
        submit_button.click()
        # time.sleep(20)

        # Then is redirected to '/portfolio/'
        portfolio_url = self.browser.current_url
        self.assertEqual(portfolio_url, self.live_server_url + "/portfolio/")

        # He notices witch the data has been updated
        title_edit = self.browser.find_element(By.ID, "background_1_title")
        self.assertEqual(title_edit.text, "Title:Developer Junior")

    def test_can_delete_academic_background(self):
        # Given loged user and exiting academic backgrounds
        background = Background(title="Developer", institution="someone", degree="Bachelor",
                                start_date="2001-10-21", finish_date="2002-10-23",
                                link_info="https://www.google.com", picture="/home/maximo/Firefox_wallpaper.png",
                                user=self.user)
        background.save()

        # When he visit '/portfolio/'
        self.login_user_visit("/portfolio/")

        # He notices a "delete" button next to the academic background

        background_delete_button = self.browser.find_element(By.ID, "delete_academic_background_1")
        time.sleep(5)
        # When he clicked in "delete" button
        background_delete_button.click()

        # Then the page in refreshed and the academic item is gone

        try:
            background_1 = self.browser.find_element(By.ID, "academic_background_1")
            self.assertTrue(False)
        except NoSuchElementException as e:
            self.assertTrue(True)