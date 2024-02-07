import io
from PIL import Image
from django.test import TestCase, Client
from django.contrib.auth.models import User


class BaseTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('username', 'email@example.com', 'password')
        self.client = Client()
        self.client.login(username='username', password='password')

    @staticmethod
    def generate_test_image():
        # Create a new image using PIL
        image = Image.new('RGB', (100, 100), color='red')
        # Save the image to a BytesIO object
        image_io = io.BytesIO()
        image.save(image_io, 'JPEG')
        # Go to the beginning of the BytesIO stream
        image_io.seek(0)
        return image_io