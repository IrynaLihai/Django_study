from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("blog", views.index, name='main'),
    path("blog/post<str:title>", views.post, name='post'),
    path("about", views.about, name='about'),
    path("services", views.services, name='services'),
    path("contact", views.contact, name='contact'),
    path("blog/category/<str:name>", views.category, name='category'),
    path('create_comment/', views.create_comment, name='comment_create'),
    path('blog/search/', views.search, name='search'),
    path('blog/create/', views.create, name='create'),
    path('blog/tag/<str:name>/', views.tag_posts, name='tag_posts'),
    path('blog/login', LoginView.as_view(), name='blog_login'),
    path('blog/logout', views.custom_logout, name='blog_logout'),
    path('blog/profile', views.profile, name='profile'),
    path("blog/uploads/", views.upload, name='upload'),
    path("blog/registration/", views.registration, name='registration'),
    path("blog/my_posts/", views.my_posts, name='my_posts'),
    path('delete_post/<post_id>/', views.delete_post, name='delete_post'),



]



