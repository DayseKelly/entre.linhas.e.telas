from django.urls import path
from . import views 

urlpatterns = [
    path('', views.listar_usuario_obras, name='listar_usuario_obras'),
    path('meus-favoritos/', views.meus_favoritos, name='meus_favoritos'),
    path('favoritar/<int:obra_id>/', views.alternar_favorito, name='alternar_favorito'),
    path('criar/', views.criar_usuario_obra, name='criar_usuario_obra'),
    path('<int:id>/', views.detalhe_usuario_obra, name='detalhe_usuario_obra'),
    path('<int:id>/editar/', views.editar_usuario_obra, name='editar_usuario_obra'),
    path('<int:id>/excluir/', views.excluir_usuario_obra, name='excluir_usuario_obra'),
]