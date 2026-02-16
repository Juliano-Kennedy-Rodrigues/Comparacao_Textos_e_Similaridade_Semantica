from django.urls import path

from . import views

urlpatterns = [
    path('helloworld/', views.helloWorld),
    path("", views.comparacao, name="comparacao"),
    path('yourname/<str:name>', views.yourName, name='your-name'),
]
