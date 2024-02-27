from .base import BaseTest
from ...models import Experience
from selenium.webdriver.common.by import By
import time


class ExperienceTest(BaseTest):
    reset_sequences = True

    def test_can_create_work_experience(self):
        # Given a loged user in '/portfolio'
        self.login_user_visit("/portfolio/")

        # He notices which the title of the browser tab is "Portfolio"
        page_title = self.browser.title
        self.assertEqual(page_title, "Portfolio")

        # He notices a heading that says "Work experience".
        heading_experience = self.browser.find_element(By.ID, "heading-experience")
        self.assertEqual(heading_experience.text, "Work experience")

        # and a button 'Add experience'
        add_button = self.browser.find_element(By.ID, "add_experience")
        self.assertEqual(add_button.text, "Add experience")

        # when he clicked the button is redirected to '/portfolio/add/experience'
        add_button.click()
        self.browser.implicitly_wait(1)
        edit_url = self.browser.current_url
        self.assertEqual(edit_url, self.live_server_url + "/portfolio/add/experience/")

        # He notices a form whit Job, Description, Start date,
        # Finish date, Current, Link, and Picture fields
        expected_labels = ['Job:', 'Description:', 'Start date:',
                           'Finish date:', 'Current:', 'Link:', 'Picture:']
        self.labels_in_form(expected_labels)

        # When completes the form fields
        field_data = {"id_job": "Developer", "id_description": "test data",
                      "id_start_date": "2023-04-03",
                      'id_finish_date': '2023-04-01', "id_link_info": "www.google.com",
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

        experience_developer = self.browser.find_element(By.ID, "experience_1")
        experience_developer.is_displayed()

    def test_can_view_works_experience_if_created(self):
        # Given loged user and exiting work experience
        experience = Experience(job="Developer", description="Test description",
                                start_date="2001-10-21", finish_date="2002-10-23",
                                current=True, link_info="www.google.com",
                                picture="/home/maximo/Firefox_wallpaper.png", user=self.user)

        experience1 = Experience(job="Football player", description="Test description",
                                 start_date="2001-10-21", finish_date="2002-10-23",
                                 current=True, link_info="www.google.com",
                                 picture="/home/maximo/Firefox_wallpaper.png", user=self.user)
        experience.save()
        experience1.save()

        # When he visit '/portfolio/'
        self.login_user_visit("/portfolio/")

        # He notices which the title of the browser tab is "Portfolio"
        page_title = self.browser.title
        self.assertEqual(page_title, "Portfolio")

        # He notices a heading that says "Work experience".
        heading_experience = self.browser.find_element(By.ID, "heading-experience")
        self.assertEqual(heading_experience.text, "Work experience")

        # Then he see the experience of the database

        # if any is not found, an exception is thrown
        experience_1 = self.browser.find_element(By.ID, "experience_1")
        experience_2 = self.browser.find_element(By.ID, "experience_2")

    def test_can_update_work_experience(self):
        # Given a user loged and work experience in database
        experience = Experience(job="Developer", description="Test description",
                                start_date="2001-10-21", finish_date="2002-10-23",
                                current=True, link_info="www.google.com",
                                picture="/home/maximo/Firefox_wallpaper.png", user=self.user)
        experience.save()

        self.login_user_visit("/portfolio/")

        # He notices an "edit" button next to the work experience

        experience_edit_button = self.browser.find_element(By.ID, "edit_experience_1")

        # When he clicked in "edit" button
        experience_edit_button.click()

        # is redirected to a work experience form page

        # he notices the url is .../portfolio/edit/experience/1
        current_url = self.browser.current_url
        self.assertEqual(self.live_server_url + "/portfolio/edit/experience/1", current_url)

        # He notices that the form has the old data in its fields
        old_data = {"id_job": "Developer", "id_description": "Test description",
                                "id_start_date": "2001-10-21", "id_finish_date": "2002-10-23",
                                "id_link_info": "www.google.com",

                    }

        for k, v in old_data.items():
            input_value = self.browser.find_element(By.ID, k)
            self.assertEqual(input_value.get_attribute("value"), v)

            input_value.clear()

        # When completes the form fields
        field_data = {"id_job": "Developer edited", "id_description": "test data edit",
                      "id_start_date": "2001-04-03",
                      'id_finish_date': '2023-04-01', "id_link_info": "www.google.com",
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
        job_edit = self.browser.find_element(By.ID, "experience_1_job")
        self.assertEqual(job_edit.text, "Job:Developer edited")

    def test_can_delete_work_experience(self):
        # Given a user loged and work experience in database
        experience = Experience(job="Developer", description="Test description",
                                start_date="2001-10-21", finish_date="2002-10-23",
                                current=True, link_info="www.google.com",
                                picture="/home/maximo/Firefox_wallpaper.png", user=self.user)
        experience.save()

        self.login_user_visit("/portfolio/")

        # He notices a "delete" button next to the work experience
        # time.sleep(30)
        experience_delete_button = self.browser.find_element(By.ID, "delete_experience_1")

        # When he clicked in "delete" button
        experience_delete_button.click()

        # Then the page in refreshed and the work experience item is gone

        self.element_is_not_in_page("experience_1")

    def test_anonymous_user_cant_crud_experience(self):
        experience = Experience(job="Developer", description="Test description",
                                start_date="2001-10-21", finish_date="2002-10-23",
                                current=True, link_info="www.google.com",
                                picture="/home/maximo/Firefox_wallpaper.png", user=self.user)
        experience.save()

        # if anonymous view portfolio page he can't see Create, Update, Delete
        # buttons

        self.browser.get(self.live_server_url + "/portfolio")

        # He can't see add experience me button

        self.element_is_not_in_page("add_experience")

        # He can't see update experience me button

        self.element_is_not_in_page("edit_experience_1")

        # He can't see delete experience me button

        self.element_is_not_in_page("delete_experience_1")