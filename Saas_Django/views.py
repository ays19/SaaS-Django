
import pathlib
from django.http import HttpResponse

this_dir = pathlib.Path(__file__).parent

def home_page_view(request, *args, **kwargs):
    my_title = "My Page"
    my_context = {
        "page_title": my_title
    }
    html_ = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <h1>{page_title} anything</h1>
</body>
</html>
""".format(**my_context) # page_title = my_title
    #html_file_path = this_dir / "home.html"
    #html_ = html_file_path.read_text()

    return HttpResponse(html_)


def home_page_view(request, *args, **kwargs):
    my_title = "My Page"
    my_context = {
        "page_title": my_title
    }
    html_ = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <h1>{page_title} anything</h1>
</body>
</html>
""".format(**my_context) # page_title = my_title
    #html_file_path = this_dir / "home.html"
    #html_ = html_file_path.read_text()

    return HttpResponse(html_)