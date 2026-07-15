from django.http import HttpResponse

def home_page_view(request, *args, **kwargs):

    return HttpResponse("<h1>Welcome to the Home Page</h1>")