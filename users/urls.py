from django.urls import path
from .views import AdminRegisterView, LoginView



urlpatterns = [
    path("admin/register/", AdminRegisterView.as_view(), name="admin-register"),
    path("login/", LoginView.as_view(), name="login"),

]
