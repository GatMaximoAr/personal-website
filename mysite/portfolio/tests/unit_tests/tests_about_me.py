from .base import BaseTest
from ...models import AboutMe


class AboutMeTest(BaseTest):

    def test_can_saving_and_retrieving_model(self):
        about_me = AboutMe(user=self.user, firstname="testname", lastname="lastname",
                           about="about me", picture="url")
        about_me.save()
        about_query = AboutMe.objects.first()
        # print(about_query)
        self.assertEqual(about_me, about_query)

    def test_can_post_new_aboutme(self):
        test_image = self.generate_test_image()
        response = self.client.post(path="/portfolio/edit/about/", data={
            "firstname": "testname", "lastname": "lastname", "about": "about me", "picture": test_image
        })

        about_query = AboutMe.objects.filter(user=self.user).first()
        self.assertEquals(about_query.firstname, "testname")

    def test_can_redirect_after_post(self):
        test_image = self.generate_test_image()
        response = self.client.post(path="/portfolio/edit/about/", data={
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
        test_image = self.generate_test_image()
        response = self.client.post(path="/portfolio/edit/about/", data={
            "firstname": "another name", "lastname": "lastname", "about": "about me", "picture": test_image
        })

        about_query_after = AboutMe.objects.get(user=self.user)

        self.assertNotEqual(about_query_before.firstname, about_query_after.firstname)

    def test_can_delete_aboutme(self):
        about_me = AboutMe(user=self.user, firstname="testname", lastname="lastname",
                           about="about me", picture="url")
        about_me.save()
        response = self.client.delete(path="/portfolio/delete/about/")

        about_query = AboutMe.objects.first()

        self.assertIsNone(about_query)