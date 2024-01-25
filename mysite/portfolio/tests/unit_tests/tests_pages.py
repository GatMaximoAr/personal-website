from .base import BaseTest


class PortfolioPagesTest(BaseTest):

    def test_can_get_portfolio_index(self):
        response = self.client.get("/portfolio/")
        self.assertTemplateUsed(response, 'index.html')

    def test_can_get_edit_about_page(self):
        response = self.client.get("/portfolio/edit/about/")
        self.assertTemplateUsed(response, "edit_about.html")

    def test_can_get_edit_experience_page(self):
        response = self.client.get("/portfolio/edit/experience/")
        self.assertTemplateUsed(response, "edit_experience.html")