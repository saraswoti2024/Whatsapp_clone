from django.urls import path
from accounts import views

urlpatterns = [
    path('register/',views.RegisterView.as_view(),name="registerview"),
    path('login_after/',views.LoginAfter.as_view(),name="loginafter"),
]