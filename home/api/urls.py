from django.urls import path
from home.api.views import (
    api_blog_detail_view,
    api_blog_update_view,
    api_blog_delete_view,
    api_blog_create_view,
    api_blog_view,
    registration_api_view,
    PaginationListView,
    profile_property_view,
    profile_update_view
) 
from rest_framework.authtoken.views import obtain_auth_token#this generate token on login
app_name='home'

urlpatterns = [
    #When visiting through browser,it directly append / at end of url so must put / in path
    path('get/',api_blog_view,name="detail"),
    path('<int:pk>/',api_blog_detail_view,name="detail"),
    path('<slug>/update/',api_blog_update_view,name="update"),
    path('<slug>/delete/',api_blog_delete_view,name="delete"),
    path('create/',api_blog_create_view,name="create"),
    path('registration-user/',registration_api_view,name="registration"),
    path('login/',obtain_auth_token,name='login'),
    path('profile-property/',profile_property_view,name='profile-property'),
    path('profile-update/',profile_update_view,name='profile-update'),
    path('list-with-pagination/',PaginationListView.as_view(),name='list-with-pagination'),
   
]
