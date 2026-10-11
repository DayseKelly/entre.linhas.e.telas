from django.urls import path
from . import views 
urlpatterns = [
    path('', views.listar_avaliacoes, name='listar_avaliacoes'),
    path('minhas/', views.minhas_avaliacoes, name='minhas_avaliacoes'),
    path('criar/', views.criar_avaliacao, name='criar_avaliacao'),
    path('<int:id>/', views.detalhe_avaliacao, name='detalhe_avaliacao'),
    path('<int:id>/editar/', views.editar_avaliacao, name='editar_avaliacao'),
    path('<int:id>/excluir/', views.excluir_avaliacao, name='excluir_avaliacao'),
]