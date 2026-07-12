from django.http import HttpResponse

def home_page_view():

    return HttpResponse("<h1>Welcome to the Home Page</h1>")