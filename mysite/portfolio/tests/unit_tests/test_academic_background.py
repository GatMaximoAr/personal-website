from .base import BaseTest
from ...models import Background


class AcademicBackgroundTest(BaseTest):

    def test_can_create_academic_background(self):
        background = Background(title="Developer", institution="someone", degree="Bachhelor",
                                start_date="2001-10-21", finish_date="2002-10-23",
                                link_info="www.google.com", picture="/home/maximo/Firefox_wallpaper.png",
                                user=self.user)
        background.save()

        query_background = Background.objects.filter(user=self.user)

        self.assertEqual(query_background[0].title, "Developer")

    def test_can_post_new_work_experience(self):
        data = {"title": "Football player", "institution": "someone",
                "degree": "Bachelor", "start_date": "2001-10-21", "finish_date": "2002-10-23",
                "link_info": "https://www.google.com", "picture": self.generate_test_image()}

        response = self.client.post(path="/portfolio/add/academic-background/", data=data)

        query_background = Background.objects.filter(user=self.user)

        self.assertEqual("Football player", query_background[0].title)

    def test_can_redirect_after_post(self):
        data = {"title": "Football player", "institution": "someone",
                "degree": "Bachelor", "start_date": "2001-10-21", "finish_date": "2002-10-23",
                "link_info": "https://www.google.com", "picture": self.generate_test_image()}

        response = self.client.post(path="/portfolio/add/academic-background/", data=data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(expected_url="/portfolio/", response=response)

    def test_can_update_academic_background(self):
        background = Background(title="Developer", institution="someone", degree="Bachhelor",
                                start_date="2001-10-21", finish_date="2002-10-23",
                                link_info="www.google.com", picture="/home/maximo/Firefox_wallpaper.png",
                                user=self.user)
        background.save()

        data = {"title": "Football player", "institution": "someone",
                "degree": "Bachelor", "start_date": "2001-10-21", "finish_date": "2002-10-23",
                "link_info": "https://www.google.com", "picture": self.generate_test_image()}

        response = self.client.post(path="/portfolio/edit/academic-background/1", data=data)

        query_background = Background.objects.filter(pk=1)

        self.assertEqual(query_background[0].title, "Football player")

    def test_can_delete_academic_background(self):
        background = Background(title="Developer", institution="someone", degree="Bachhelor",
                                start_date="2001-10-21", finish_date="2002-10-23",
                                link_info="www.google.com", picture="/home/maximo/Firefox_wallpaper.png",
                                user=self.user)
        background.save()

        self.client.delete(path="/portfolio/delete/academic-background/1")

        query_background = Background.objects.filter(user=self.user)

        self.assertTrue(len(query_background) == 0)