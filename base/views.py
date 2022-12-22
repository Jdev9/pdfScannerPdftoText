from django.shortcuts import render

# Create your views here.

def index(request):
    return render(
        request,
        "index.html",
        {
            "title": "Django example",
        },
    )


def signupUser(request):
    return render(request,'signup.html')

def loginUser(request):
    return render(request,"login.html")
