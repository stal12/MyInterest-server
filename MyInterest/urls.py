"""MyInterest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView

from server import views
from rest_framework_jwt.views import verify_jwt_token

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^admin/', admin.site.urls),
    url(r'^api-token-auth/', views.my_obtain_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),
    url(r'^prova/', views.prova),
    # url(r'^personal/', views.personal),
    url(r'^facebook-login/', views.facebook_login),
    url(r'^facebook-register/', views.facebook_register),
    url(r'^fetch-user/', views.fetch_user),
    url(r'^register-user/', views.register_user),
    url(r'^register-categories/', views.register_categories),
    url(r'^login/', views.login)
]
