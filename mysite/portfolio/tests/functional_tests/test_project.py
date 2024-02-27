from .base import BaseTest
from ...models import Project
from selenium.webdriver.common.by import By
import time


class ProjectTest(BaseTest):
    reset_sequences = True

    def test_can_create_project(self):
        # Given a loged user in '/portfolio'
        self.login_user_visit("/portfolio/")

        # He notices which the title of the browser tab is "Portfolio"
        page_title = self.browser.title
        self.assertEqual(page_title, "Portfolio")

        # He notices a heading that says "projects".
        heading_project = self.browser.find_element(By.ID, "heading-project")
        self.assertEqual(heading_project.text, "Projects")

        # and a button 'Add item'
        add_button = self.browser.find_element(By.ID, "add_project")
        self.assertEqual(add_button.text, "Add item")

        # when he clicked the button is redirected to '/portfolio/add/project/'
        add_button.click()
        self.browser.implicitly_wait(1)
        edit_url = self.browser.current_url
        self.assertEqual(edit_url, self.live_server_url + "/portfolio/add/project/")

        # He notices a form whit Title, Description, Link and picture fields
        expected_labels = ["Title:", 'Description:', 'Link:', 'Picture:']
        self.labels_in_form(expected_labels)

        # When completes the form fields
        field_data = {"id_title": "Web portfolio", "id_description": "some description",
                      "id_link_info": "https://www.google.com",
                      "id_picture": "/home/maximo/Firefox_wallpaper.png"}

        self.completed_form_fields(field_data)

        # and send the form
        submit_button = self.browser.find_element(By.ID, "submit")
        time.sleep(1)
        submit_button.click()

        # Then is redirected to '/portfolio/'
        portfolio_url = self.browser.current_url
        self.assertEqual(portfolio_url, self.live_server_url + "/portfolio/")

        project = self.browser.find_element(By.ID, "project_1")
        project.is_displayed()

    def test_can_view_project_if_created(self):
        # Given loged user and exiting project
        project = Project(title="Portfolio", description="some description",
                          link_info="http://www.google.com",
                          picture="/home/maximo/Firefox_wallpaper.png",
                          user=self.user)
        project.save()

        # When he visit '/portfolio/'
        self.login_user_visit("/portfolio/")

        # He notices a heading that says "projects".
        heading_project = self.browser.find_element(By.ID, "heading-project")
        self.assertEqual(heading_project.text, "Projects")

        # if any is not found, an exception is thrown
        project_1 = self.browser.find_element(By.ID, "project_1")

    def test_can_update_project(self):
        # Given loged user and exiting project
        project = Project(title="Portfolio", description="some description",
                          link_info="https://www.google.com",
                          picture="/home/maximo/Firefox_wallpaper.png",
                          user=self.user)
        project.save()

        # When he visit '/portfolio/'
        self.login_user_visit("/portfolio/")

        # and a button 'edit'
        edit_button = self.browser.find_element(By.ID, "edit_project_1")
        self.assertEqual(edit_button.text, "edit")

        # when he clicked the button is redirected to '/portfolio/edit/project/1'
        edit_button.click()
        self.browser.implicitly_wait(1)
        edit_url = self.browser.current_url
        self.assertEqual(edit_url, self.live_server_url + "/portfolio/edit/project/1")

        # He notices that the form has the old data in its fields
        old_data = {"id_title": "Portfolio", "id_description": "some description",
                    "id_link_info": "https://www.google.com"}

        for k, v in old_data.items():
            input_value = self.browser.find_element(By.ID, k)
            self.assertEqual(input_value.get_attribute("value"), v)

            input_value.clear()

        # When completes the form fields
        field_data = {"id_title": "Web portfolio", "id_description": "some description",
                      "id_link_info": "https://www.google.com",
                      "id_picture": "/home/maximo/Firefox_wallpaper.png"}

        self.completed_form_fields(field_data)

        # and send the form
        submit_button = self.browser.find_element(By.ID, "submit")
        time.sleep(1)
        submit_button.click()

        # Then is redirected to '/portfolio/'
        portfolio_url = self.browser.current_url
        self.assertEqual(portfolio_url, self.live_server_url + "/portfolio/")

        # He notices witch the data has been updated
        title_edit = self.browser.find_element(By.ID, "project_1_title")
        self.assertEqual(title_edit.text, "Title:Web portfolio")

    def test_can_delete_project(self):
        # Given loged user and exiting project
        project = Project(title="Portfolio", description="some description",
                          link_info="https://www.google.com",
                          picture="/home/maximo/Firefox_wallpaper.png",
                          user=self.user)
        project.save()

        # When he visit '/portfolio/'
        self.login_user_visit("/portfolio/")

        # and a button 'delete'
        delete_button = self.browser.find_element(By.ID, "delete_project_1")
        self.assertEqual(delete_button.text, "delete")

        # When he clicked in "delete" button
        delete_button.click()

        # Then the page in refreshed and the project item is gone

        self.element_is_not_in_page("project_1")

    def test_anonymous_user_cant_crud_project(self):
        project = Project(title="Portfolio", description="some description",
                          link_info="https://www.google.com",
                          picture="/home/maximo/Firefox_wallpaper.png",
                          user=self.user)
        project.save()

        # if anonymous view portfolio page he can't see Create, Update, Delete
        # buttons

        self.browser.get(self.live_server_url + "/portfolio")

        # He can't see add about me button

        self.element_is_not_in_page("add_project")

        # He can't see update about me button

        self.element_is_not_in_page("edit_project_1")

        # He can't see delete about me button

        self.element_is_not_in_page("delete_project_1")