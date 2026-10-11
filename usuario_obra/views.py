from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import UsuarioObra
from .forms import UsuarioObraForm
from django.contrib.auth.decorators import login_required, permission_required
from obras.models import Obra


@login_required
@permission_required('usuario_obra.view_usuarioobra', raise_exception=True)
def listar_usuario_obras(request):
    registros = UsuarioObra.objects.all()
    return render(request, 'lista_usuario_obra.html', {'usuario_obras': registros})


@login_required
@permission_required('usuario_obra.add_usuarioobra', raise_exception=True)
def criar_usuario_obra(request):
    if request.method == 'POST':
        form = UsuarioObraForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Relação usuário-obra cadastrada com sucesso.')
            return redirect('listar_usuario_obras')
    else:
        form = UsuarioObraForm()
    return render(request, 'form_usuario_obra.html', {'form': form})


@login_required
@permission_required('usuario_obra.view_usuarioobra', raise_exception=True)
def detalhe_usuario_obra(request, id):
    registro = get_object_or_404(UsuarioObra, id=id)
    return render(request, 'detalhe_usuario_obra.html', {'registro': registro})


@login_required
@permission_required('usuario_obra.change_usuarioobra', raise_exception=True)
def editar_usuario_obra(request, id):
    registro = get_object_or_404(UsuarioObra, id=id)

    if request.method == 'POST':
        form = UsuarioObraForm(request.POST, instance=registro)
        if form.is_valid():
            form.save()
            messages.success(request, 'Relação usuário-obra editada com sucesso.')
            return redirect('detalhe_usuario_obra', id=registro.id)
    else:
        form = UsuarioObraForm(instance=registro)

    return render(request, 'form_usuario_obra.html', {
        'form': form,
        'titulo_pagina': 'Editar relação usuário-obra',
    })


@login_required
@permission_required('usuario_obra.delete_usuarioobra', raise_exception=True)
def excluir_usuario_obra(request, id):
    registro = get_object_or_404(UsuarioObra, id=id)

    if request.method == 'POST':
        registro.delete()
        messages.success(request, 'Relação usuário-obra excluída com sucesso.')
        return redirect('listar_usuario_obras')

    return render(request, 'excluir_usuario_obra.html', {'registro': registro})


@login_required
def meus_favoritos(request):
    favoritos = UsuarioObra.objects.filter(
        usuario=request.user,
        favorito=True,
    ).select_related('obra').prefetch_related('obra__temas').order_by('obra__titulo')
    return render(request, 'meus_favoritos.html', {
        'favoritos': favoritos,
        'active_tab': 'favoritos',
    })


@login_required
@require_POST
def alternar_favorito(request, obra_id):
    obra = get_object_or_404(Obra, id=obra_id)
    registro, _ = UsuarioObra.objects.get_or_create(usuario=request.user, obra=obra)
    registro.favorito = not registro.favorito
    registro.save(update_fields=['favorito'])
    if registro.favorito:
        messages.success(request, 'Repertório adicionado aos seus favoritos.')
    else:
        messages.success(request, 'Repertório removido dos seus favoritos.')
    return redirect('detalhe_obra', id=obra.id)