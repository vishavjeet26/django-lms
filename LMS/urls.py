"""LMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from signup_crud.views import home_view

from rest_framework import routers
#from lms_api.views import index,category,book
#from lms_api import views
from django.contrib.auth import views as auth_views

# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'categories', views.CategoryViewSet)
# router.register(r'publishers', views.PublisherViewSet)
# router.register(r'authors', views.AuthorViewSet)
# router.register(r'books', views.BookViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('singup_crud/', include('signup_crud.urls')),
    path('', home_view),
    path('library/', include('library.urls')),
   # Resfull API for LMS
    # path('category/(?P<category_id>\d+)', category, name="category"),
    # path('book/(?P<book_id>\d+)', book, name="book"),
    # path('', index, name="index" ), 
    # path('', include(router.urls)),
    path('accounts/login/', auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
