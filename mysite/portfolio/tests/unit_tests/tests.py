from django.test import TestCase, Client
from django.contrib.auth.models import User
from ...models import AboutMe


class PortfolioPageTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('username', 'email@example.com', 'password')
        self.client = Client()
        self.client.login(username='username', password='password')

    def test_can_get_portfolio_index(self):
        response = self.client.get("/portfolio/")
        self.assertTemplateUsed(response, 'index.html')

    def test_can_saving_and_retrieving_model(self):
        about_me = AboutMe(user=self.user, firstname="testname", lastname="lastname", about="about me", picture="url")
        about_me.save()
        about_query = AboutMe.objects.first()
        print(about_query)
        self.assertEqual(about_me, about_query)