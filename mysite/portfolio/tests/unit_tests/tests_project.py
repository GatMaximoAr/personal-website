from .base import BaseTest
from ...models import Project


class ProjectTest(BaseTest):

    def test_can_create_project_model(self):
        project = Project(title="Portfolio", description="some description",
                          link_info="http://www.google.com",
                          picture="/home/maximo/Firefox_wallpaper.png",
                          user=self.user)
        project.save()

        query_project = Project.objects.get(pk=1)

        self.assertEqual(query_project.title, project.title)

    def test_can_post_new_project(self):
        data = {"title": "Portfolio", "description": "someone",
                "link_info": "https://www.google.com", "picture": self.generate_test_image()}

        response = self.client.post(path="/portfolio/add/project/", data=data)

        query_project = Project.objects.get(pk=1)

        self.assertEqual("Portfolio", query_project.title)

    def test_can_redirect_after_post(self):
        data = {"title": "Portfolio", "description": "someone",
                "link_info": "https://www.google.com", "picture": self.generate_test_image()}

        response = self.client.post(path="/portfolio/add/project/", data=data)

        self.assertRedirects(expected_url="/portfolio/", response=response)

    def test_can_update_project(self):
        project = Project(title="Portfolio", description="some description",
                          link_info="http://www.google.com",
                          picture="/home/maximo/Firefox_wallpaper.png",
                          user=self.user)
        project.save()

        data = {"title": "Portfolio web", "description": "someone",
                "link_info": "https://www.google.com", "picture": self.generate_test_image()}

        response = self.client.post(path="/portfolio/edit/project/1", data=data)

        query_project = Project.objects.get(pk=1)

        self.assertEqual("Portfolio web", query_project.title)

    def test_can_delete_project(self):
        project = Project(title="Portfolio", description="some description",
                          link_info="http://www.google.com",
                          picture="/home/maximo/Firefox_wallpaper.png",
                          user=self.user)
        project.save()

        self.client.delete(path="/portfolio/delete/project/1")

        query_project = Project.objects.filter(user=self.user)

        self.assertTrue(len(query_project) == 0)