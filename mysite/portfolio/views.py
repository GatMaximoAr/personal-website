from django.http import HttpResponse


def index(request):
    """Hello World."""
    return HttpResponse("Hello, world. You're at the portfolio index.")
