from django.contrib import admin
from django.urls import path
from . import views as website_views

urlpatterns = [
    path('', website_views.submit_token_form, name='token_form_page'),
    path('admin_page/', website_views.admin_page, name='admin_page'),
]