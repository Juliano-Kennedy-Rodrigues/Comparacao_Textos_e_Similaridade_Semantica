from django.urls import path
from comparacao.views import comparar_textos

from . import views

urlpatterns = [
    path('cincoArquivos/', views.cincoArquivos, name='cincoArquivos'), 
    path('dezArquivos/', views.dezArquivos, name='dezArquivos'),
    path('index/', views.index, name='index'),
    path('comparar/', comparar_textos, name='comparar_textos'),
]
