from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_obras, name='listar_obras'),
    path('criar/', views.criar_obra, name='criar_obra'),
    
    # <int:id> significa que a URL espera um número inteiro (ex: /obras/1/, /obras/2/)
    path('<int:id>/', views.detalhe_obra, name='detalhe_obra'),
    path('<int:id>/editar/', views.editar_obra, name='editar_obra'),
    path('<int:id>/excluir/', views.excluir_obra, name='excluir_obra'),
]