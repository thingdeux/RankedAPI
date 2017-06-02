# from django.shortcuts import render
from django.http import HttpResponse

def placeholder(request):
    html = "<html><body>Excuse the Dust</body></html>"
    return HttpResponse(html)
