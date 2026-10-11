from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_escolas, name='listar_escolas'),
    path('nova/', views.criar_escola, name='criar_escola'),
    path('<int:id>/', views.detalhe_escola, name='detalhe_escola'),
    path('<int:id>/editar/', views.editar_escola, name='editar_escola'),
    path('<int:id>/excluir/', views.excluir_escola, name='excluir_escola'),
]