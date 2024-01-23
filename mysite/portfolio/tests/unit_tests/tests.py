import io
from PIL import Image
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from ...models import AboutMe


def generate_test_image():
    # Create a new image using PIL
    image = Image.new('RGB', (100, 100), color='red')
    # Save the image to a BytesIO object
    image_io = io.BytesIO()
    image.save(image_io, 'JPEG')
    # Go to the beginning of the BytesIO stream
    image_io.seek(0)
    return image_io


class BaseTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('username', 'email@example.com', 'password')
        self.client = Client()
        self.client.login(username='username', password='password')


class PortfolioPagesTest(BaseTest):

    def test_can_get_portfolio_index(self):
        response = self.client.get("/portfolio/")
        self.assertTemplateUsed(response, 'index.html')

    def test_can_get_edit_page(self):
        response = self.client.get("/portfolio/edit/")
        self.assertTemplateUsed(response, "edit.html")


class AboutMeTest(BaseTest):

    def test_can_saving_and_retrieving_model(self):
        about_me = AboutMe(user=self.user, firstname="testname", lastname="lastname",
                           about="about me", picture="url")
        about_me.save()
        about_query = AboutMe.objects.first()
        # print(about_query)
        self.assertEqual(about_me, about_query)

    def test_can_post_new_aboutme(self):
        test_image = generate_test_image()
        response = self.client.post(path="/portfolio/edit/", data={
            "firstname": "testname", "lastname": "lastname", "about": "about me", "picture": test_image
        })

        about_query = AboutMe.objects.filter(user=self.user).first()
        self.assertEquals(about_query.firstname, "testname")

    def test_can_redirect_after_post(self):
        test_image = generate_test_image()
        response = self.client.post(path="/portfolio/edit/", data={
            "firstname": "testname", "lastname": "lastname", "about": "about me", "picture": test_image
        })

        self.assertRedirects(response, "/portfolio/")

    def test_can_update_aboutme(self):
        # existing data
        about_me = AboutMe(user=self.user, firstname="testname", lastname="lastname",
                           about="about me", picture="url")
        about_me.save()

        about_query_before = AboutMe.objects.get(user=self.user)

        # update post
        test_image = generate_test_image()
        response = self.client.post(path="/portfolio/edit/", data={
            "firstname": "another name", "lastname": "lastname", "about": "about me", "picture": test_image
        })

        about_query_after = AboutMe.objects.get(user=self.user)

        self.assertNotEqual(about_query_before.firstname, about_query_after.firstname)

    def test_can_delete_aboutme(self):
        about_me = AboutMe(user=self.user, firstname="testname", lastname="lastname",
                           about="about me", picture="url")
        about_me.save()
        response = self.client.delete(path="/portfolio/delete_about/")

        about_query = AboutMe.objects.first()

        self.assertIsNone(about_query)