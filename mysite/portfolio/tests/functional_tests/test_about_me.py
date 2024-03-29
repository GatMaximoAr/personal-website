from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from ...models import AboutMe
from .base import BaseTest
import time


class AboutMeTest(BaseTest):
    reset_sequences = True

    def test_can_user_create_about_me(self):
        # Give
        # Loged user without 'about me' visit the website
        # in 'portfolio' index

        self.login_user_visit("/portfolio/")

        # He notices which the title of the browser tab is "Portfolio"
        page_title = self.browser.title
        self.assertEqual(page_title, "Portfolio")

        # and a button 'add about me'
        add_button = self.browser.find_element(By.ID, "add_aboutme")
        self.assertEqual(add_button.text, "Add about me")

        # when he clicked the button is redirected to '/portfolio/edit/about/'
        add_button.click()
        self.browser.implicitly_wait(1)
        edit_url = self.browser.current_url
        self.assertEqual(edit_url, self.live_server_url + "/portfolio/add/about/")

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

        # Then is redirected to '/portfolio/'
        portfolio_url = self.browser.current_url
        self.assertEqual(portfolio_url, self.live_server_url + "/portfolio/")

        # and see the new data on page

        search_data_in_page = {
            "create_name": field_data["id_firstname"] + " " + field_data["id_lastname"],
            "create_about": field_data["id_about"]
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

        # Then he saw appear the data on the page
        search_data_in_page = {
            "create_name": "testname lastname"
            , "create_about": "about me"
        }
        self.finding_data_on_page(search_data_in_page)

        create_img = self.browser.find_element(By.ID, "create_img")
        self.assertTrue(create_img.is_displayed())

    def test_can_update_aboutme(self):
        # User with a about me created visit '/portfolio'
        about_me = AboutMe(user=self.user, firstname="testname", lastname="lastname", about="about me",
                           picture="/home/maximo/Firefox_wallpaper.png")
        about_me.save()
        self.login_user_visit("/portfolio")

        # and a button 'add about me'
        edit_button = self.browser.find_element(By.ID, "edit_aboutme")
        self.assertEqual(edit_button.text, "Edit about me")

        # when he clicked the button is redirected to '/portfolio/edit'
        edit_button.click()
        self.browser.implicitly_wait(1)
        edit_url = self.browser.current_url
        self.assertEqual(edit_url, self.live_server_url + "/portfolio/edit/about/1")

        # He notices that the form has the old data in its fields
        old_data = {"id_firstname": "testname", "id_lastname": "lastname",
                      "id_about": "about me",
                    }

        for k, v in old_data.items():
            input_value = self.browser.find_element(By.ID, k)
            self.assertEqual(input_value.get_attribute("value"), v)

            input_value.clear()

        # when he completed the form with modified data
        field_data = {"id_firstname": "Test name", "id_lastname": "test surname",
                      "id_about": "I am a test user to testing",
                      "id_picture": "/home/maximo/Descargas/mile-portada.jpeg"}

        self.completed_form_fields(field_data)

        # And sends the form
        submit_button = self.browser.find_element(By.ID, "submit")
        time.sleep(1)
        submit_button.click()

        # Then is redirected to '/portfolio/' and saw appear the data on the page
        portfolio_url = self.browser.current_url
        self.assertEqual(portfolio_url, self.live_server_url + "/portfolio/")

        # and see the new data on page
        search_data_in_page = {
            "create_name": field_data["id_firstname"] + " " + field_data["id_lastname"],
            "create_about": field_data["id_about"]
        }
        self.finding_data_on_page(search_data_in_page)

        create_img = self.browser.find_element(By.ID, "create_img")
        self.assertTrue(create_img.is_displayed())

    def test_can_delete_about_me(self):
        # User with a about me created visit '/portfolio'
        about_me = AboutMe(user=self.user, firstname="testname", lastname="lastname", about="about me",
                           picture="/home/maximo/Firefox_wallpaper.png")
        about_me.save()
        self.login_user_visit("/portfolio")

        # a button 'Edit about me'
        edit_button = self.browser.find_element(By.ID, "edit_aboutme")
        self.assertEqual(edit_button.text, "Edit about me")

        # a button 'Delete about me'
        delete_button = self.browser.find_element(By.ID, "delete_aboutme")
        self.assertEqual(delete_button.text, "Delete about me")

        # when he clicked the button the page is reloaded
        # and appear in page a button what say "Add about me"
        delete_button.click()
        add_button = self.browser.find_element(By.ID, "add_aboutme")
        self.assertEqual(add_button.text, "Add about me")

    def test_anonymous_user_cant_crud_about(self):
        about_me = AboutMe(user=self.user, firstname="testname", lastname="lastname", about="about me",
                           picture="/home/maximo/Firefox_wallpaper.png")
        about_me.save()

        # if anonymous view portfolio page he can't see Create, Update, Delete
        # buttons

        self.browser.get(self.live_server_url + "/portfolio")

        # He can't see add about me button

        self.element_is_not_in_page("add_aboutme")

        # He can't see update about me button

        self.element_is_not_in_page("edit_aboutme")

        # He can't see delete about me button

        self.element_is_not_in_page("delete_aboutme")