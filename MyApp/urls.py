from django.urls import path
from MyApp import views
urlpatterns=[
    path('upload/',views.index,name='upload_file'),
     path('summary/', views.summary, name='summary'),
     path('',views.home,name='home')
     
]