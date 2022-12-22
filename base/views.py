from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Upload,TextData
import PyPDF2
import os 
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    return render(
        request,
        "index.html",
        {
            "title": "Django example",
        },
    )

def loginUser(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"Login successful")
            return redirect("index")
        else:
            messages.error(request,"Invalid credentials")
            return render(
                request,
                "login.html"
            )
    return render(
        request,
        "login.html",
    )


def signupUser(request):
    
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST['email']
        password = request.POST["password"]
        confirm_password = request.POST['password2']
        # print(username,email,password,confirm_password)

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                print("user name exit")
                messages.error(request,"Username already exists")
                return render(
                    request,
                    "signup.html"
                )
            elif User.objects.filter(email=email).exists():

                messages.error(request,"Email already exists")
                return render(
                    request,
                    "signup.html"
                )
            else:
                user = User.objects.create_user(username=username,email=email,password=password)
                user.save()
                messages.success(request,"Account created successfully")
                return redirect("login")
        else:
            messages.error(request,"Password does not match")
            return render(
                request,
                "signup.html"
            )
    

    # print("hello nothing is doen")
    return render(
            request,
            "signup.html"
    )

   
def logoutUser(request):
    logout(request)
    messages.success(request,"Logout successful")
    return redirect("index")


def uploadPdf(request):
    if request.method == "POST":
        pdfFile = request.FILES["file"]
        if pdfFile.name.endswith(".pdf"):
            try:

                upload = Upload(user=request.user,file=pdfFile)
                # if uploaded.file exists then first delete it
                upload.save()
                textData = TextData(text=upload,data=pdfToText(upload.file.name))
                textData.save()
                messages.success(request,"File uploaded successfully")
            except:
                messages.error(request,"File not uploaded")
                return render(
                    request,
                    "index.html"
                )
            # uploaded file details
            file = Upload.objects.last()
            print(pdfToText(file.file.name))
            return render(
                request,
                'index.html',
                {
                    'data': pdfToText(file.file.name),
                    'files': Upload.objects.filter(user=request.user)
                }
            )
            
        else:
            messages.error(request,"File not uploaded or Invalid file format")
            return render(
                request,
                "index.html"
            )

    messages.error(request,"File not uploaded")
    return render(
        request,
        "index.html"
    )


def data(request):
    return render(
        request,
        "data.html"
    )

def pdfToText(path):
    pdfreader = PyPDF2.PdfFileReader(path)
    no_of_pages = pdfreader.numPages
    with open('final_txt.txt', 'w') as f:
        for i in range(0, no_of_pages):
            try:
                pagObj = pdfreader.getPage(i)
                f.write(pagObj.extractText())
            except:
                pass
    with open('final_txt.txt', 'r') as f:
        text = f.read()
    if os.path.exists("final_txt.txt"):
        os.remove("final_txt.txt")
        return text

