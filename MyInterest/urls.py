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
    url(r'^fetch-person/', views.fetch_person),
    url(r'^fetch-users/', views.fetch_users),
    url(r'^fetch-friends/', views.fetch_friends),
    url(r'^fetch-pending-friends/', views.fetch_pending_friends),
    url(r'^register-user/', views.register_user),
    url(r'^register-categories/', views.register_categories),
    url(r'^login/', views.login),
    url(r'^fetch-items/', views.fetch_items),
    url(r'^fetch-user-posts/', views.fetch_user_posts),
    url(r'^fetch-posts/', views.fetch_posts),
    url(r'^store-post/', views.store_post),
    url(r'^store-comment/', views.store_comment),
    url(r'^store-like/', views.store_like),
    url(r'^request-friend/', views.request_friend),
    url(r'^accept-friend/', views.accept_friend),
    url(r'^cancel-friend/', views.cancel_friend),
    url(r'^delete-friend/', views.delete_friend)
]
