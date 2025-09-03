from django.urls import path
from chat import views

urlpatterns = [
    path('profile/',views.ProfileView.as_view(),name="profileview"),
    path('searchbar/',views.SearchBarPersonal.as_view(),name="searchbar"),
 ]