from django.urls import path 
from drfapi import views

urlpatterns = [
    path('feed/submit/',views.FeedBackApi.as_view(),name='feed-submit'),
]