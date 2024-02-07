from .base import BaseTest
from ...models import Experience


class ExperienceTest(BaseTest):

    def test_can_create_work_experience(self):
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

        query_experience = Experience.objects.filter(user=self.user)
        # print(query_experience)

        self.assertEqual(experience.job, query_experience[0].job)

    def test_can_post_new_work_experience(self):
        data = {"job": "Football player", "description": "Test description",
                "start_date": "2001-10-21", "finish_date": "2002-10-23",
                "current": True, "link_info": "www.google.com",
                "picture": self.generate_test_image()}

        response = self.client.post(path="/portfolio/edit/experience/", data=data)

        query_experience = Experience.objects.filter(user=self.user)

        self.assertEqual("Football player", query_experience[0].job)

    def test_redirect_after_post(self):
        data = {"job": "Football player", "description": "Test description",
                "start_date": "2001-10-21", "finish_date": "2002-10-23",
                "current": True, "link_info": "www.google.com",
                "picture": self.generate_test_image()}

        response = self.client.post(path="/portfolio/edit/experience/", data=data)

        self.assertRedirects(response, "/portfolio/")

    def test_can_update_work_experience(self):
        experience = Experience(job="Football player", description="Test description",
                                 start_date="2001-10-21", finish_date="2002-10-23",
                                 current=True, link_info="www.google.com",
                                 picture="/home/maximo/Firefox_wallpaper.png", user=self.user)
        experience.save()

        data = {"job": "Football player edited", "description": "Test description edited",
                "start_date": "2001-10-21", "finish_date": "2002-10-23",
                "current": True, "link_info": "www.google.com",
                "picture": self.generate_test_image()}

        response = self.client.post(path="/portfolio/edit/experience/1", data=data)

        query_experience = Experience.objects.filter(user=self.user)

        self.assertEqual("Football player edited", query_experience[0].job)

    def test_can_delete_work_experience(self):
        experience = Experience(job="Football player", description="Test description",
                                start_date="2001-10-21", finish_date="2002-10-23",
                                current=True, link_info="www.google.com",
                                picture="/home/maximo/Firefox_wallpaper.png", user=self.user)
        experience.save()

        response = self.client.delete(path="/portfolio/delete/experience/1")

        query_experience = Experience.objects.filter(user=self.user)
        # print(len(query_experience))

        self.assertTrue(len(query_experience) == 0)