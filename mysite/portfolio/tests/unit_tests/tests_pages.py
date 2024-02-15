from .base import BaseTest
from ...models import *


class PortfolioPagesTest(BaseTest):

    def test_can_get_portfolio_index(self):
        response = self.client.get("/portfolio/")
        self.assertTemplateUsed(response, 'index.html')

    def test_can_get_add_about_page(self):
        response = self.client.get('/portfolio/add/about/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit_about.html")

    def test_can_get_edit_about_page(self):
        about_me = AboutMe(user=self.user, firstname="testname", lastname="lastname",
                           about="about me", picture="url")
        about_me.save()

        response = self.client.get('/portfolio/edit/about/1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit_about.html")

    def test_can_get_add_experience_page(self):
        response = self.client.get('/portfolio/add/experience/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit_experience.html")

    def test_can_get_edit_experience_page(self):
        experience = Experience(job="Developer", description="Test description",
                                start_date="2001-10-21", finish_date="2002-10-23",
                                current=True, link_info="www.google.com",
                                picture="/home/maximo/Firefox_wallpaper.png", user=self.user)
        experience.save()

        response = self.client.get('/portfolio/edit/experience/1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit_experience.html")

    def test_can_get_add_background_page(self):
        response = self.client.get('/portfolio/add/academic-background/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit_background.html")

    def test_can_get_edit_background_page(self):
        background = Background(title="Developer", institution="someone", degree="Bachhelor",
                                start_date="2001-10-21", finish_date="2002-10-23",
                                link_info="www.google.com", picture="/home/maximo/Firefox_wallpaper.png",
                                user=self.user)
        background.save()

        response = self.client.get('/portfolio/edit/academic-background/1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit_background.html")

    def test_can_get_add_project_page(self):
        response = self.client.get('/portfolio/add/project/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit_project.html")

    def test_can_get_edit_project_page(self):
        project = Project(title="Portfolio", description="some description",
                          link_info="http://www.google.com",
                          picture="/home/maximo/Firefox_wallpaper.png",
                          user=self.user)
        project.save()

        response = self.client.get('/portfolio/edit/project/1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit_project.html")