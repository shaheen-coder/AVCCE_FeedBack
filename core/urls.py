from django.urls import path 
from core import views
from core.api import api
urlpatterns = [
    path('',views.Home.as_view(),name='home'),
    path('team',views.Team.as_view(),name='team'),
    path('login/',views.Login.as_view(),name='login'),
    path('feed/<str:code>/',views.FeedForm.as_view(),name='feed-form'),
    path('choose/course/',views.CourseChocie.as_view(),name='course'), # choose which course 
    path('courses/<int:cid>/',views.CourseList.as_view(),name='course-list'), # list selectd course subject 
    # api urls 
    path('api/',api.urls),
]