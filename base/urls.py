from .import views
from django.urls import path

urlpatterns = [
    path("",views.index,name="index"),
    path("login",views.loginUser,name="login"),
    path("signup",views.signupUser,name="signup"),
    path("logout",views.logoutUser,name="logout"),
    path("upload",views.uploadPdf,name="upload"),
    path("view",views.data,name="data"),
]