from django.urls import path
from . import views

urlpatterns = [
    path ('', views.listar_usuarios, name='listar_usuarios'),
    path('minha-area/', views.minha_area, name='minha_area'),
    path ('novo/', views.criar_usuario, name='criar_usuario'),  
    path('<int:id>/', views.detalhe_usuario, name='detalhe_usuario'),
    path('<int:id>/editar/', views.editar_usuario, name='editar_usuario'),
    path('<int:id>/excluir/', views.excluir_usuario, name='excluir_usuario'),
    path('login/', views.fazer_login, name='login'),
    path('cadastro/', views.cadastrar, name='cadastro'),
    path('escolas/buscar/', views.buscar_escolas, name='buscar_escolas'),
    path('logout/', views.fazer_logout, name='logout'),

]
