from django.urls import path
from chat import views

urlpatterns = [
    path('profile/',views.ProfileView.as_view(),name="profileview"),
    path('searchbar/<int:reciever_id>/',views.SearchBarPersonal.as_view(),name="searchbar"),
    path('searchbar2/<str:group_name>/',views.SearchBarGroup.as_view(),name="searchbargroup"),
    path('searchall/',views.SearchAll.as_view(),name="searchall"),
 ]