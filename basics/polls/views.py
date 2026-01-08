from django.http import HttpResponse

def index(request):
    return HttpResponse("this is poll index and we learning basics of django")


"""

- most basic view you can build, to acces it in browser -> we need to map it to URL
- There URl configurations are define in each django app, and they are file named urls.py

"""