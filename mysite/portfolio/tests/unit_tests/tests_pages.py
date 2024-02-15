from django.urls import reverse

from .base import BaseTest


class PortfolioPagesTest(BaseTest):

    def test_can_get_portfolio_index(self):
        response = self.client.get("/portfolio/")
        self.assertTemplateUsed(response, 'index.html')

    def test_can_get_edit_about_page(self):
        response = self.client.get('/portfolio/add/about/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit_about.html")

    def test_can_get_edit_experience_page(self):
        response = self.client.get('/portfolio/add/experience/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit_experience.html")

    def test_can_get_edit_background_page(self):
        response = self.client.get('/portfolio/add/academic-background/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit_background.html")