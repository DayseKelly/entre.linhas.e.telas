from django.shortcuts import get_object_or_404, render, redirect
from .models import Obra, Tema
from .forms import ObraForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages


@login_required
def listar_obras(request):
    temas = Tema.objects.all()
    obras = Obra.objects.prefetch_related('temas').order_by('titulo')
    tema_id = request.GET.get('tema', '')
    if tema_id.isdigit():
        obras = obras.filter(temas__id=tema_id)
    return render(request, 'obras/lista_obras.html', {
        'obras': obras,
        'temas': temas,
        'tema_selecionado': tema_id,
    })

@login_required
@permission_required('obras.add_obra', raise_exception=True)
def criar_obra(request):
    if request.method == 'POST':
        form = ObraForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Obra cadastrada com sucesso.')
            return redirect('listar_obras')
    else:
        form = ObraForm()

    return render(request, 'obras/form_obra.html', {
        'form': form,
        'titulo_pagina': 'Cadastrar obra',
    })


  
@login_required
def detalhe_obra(request, id):
    obra = get_object_or_404(Obra, id=id)
    from avaliacoes.forms import ComentarioForm
    from avaliacoes.models import Avaliacao
    from usuario_obra.models import UsuarioObra
    from django.db.models import Avg

    minha_avaliacao = Avaliacao.objects.filter(obra=obra, usuario=request.user).first()
    if request.method == 'POST':
        form = ComentarioForm(request.POST, instance=minha_avaliacao)
        if form.is_valid():
            avaliacao = form.save(commit=False)
            avaliacao.obra = obra
            avaliacao.usuario = request.user
            avaliacao.save()
            messages.success(request, 'Sua avaliação foi publicada.')
            return redirect('detalhe_obra', id=obra.id)
    else:
        form = ComentarioForm(instance=minha_avaliacao)

    avaliacoes = obra.avaliacoes.select_related('usuario').order_by('-id')
    resumo_avaliacoes = avaliacoes.aggregate(media=Avg('nota'))
    favorito = UsuarioObra.objects.filter(
        usuario=request.user,
        obra=obra,
        favorito=True,
    ).exists()
    return render(request, 'obras/detalhe_obra.html', {
        'obra': obra,
        'avaliacao_form': form,
        'minha_avaliacao': minha_avaliacao,
        'avaliacoes': avaliacoes,
        'media_avaliacoes': resumo_avaliacoes['media'],
        'favorito': favorito,
    })

@login_required
@permission_required('obras.change_obra', raise_exception=True)
def editar_obra(request, id):
    obra = get_object_or_404(Obra, id=id)

    if request.method == 'POST':
        form = ObraForm(request.POST, request.FILES, instance=obra)

        if form.is_valid():
            form.save()
            messages.success(request, 'Obra editada com sucesso.')
            return redirect('detalhe_obra', id=obra.id)
    else:
        form = ObraForm(instance=obra)

    return render(request, 'obras/form_obra.html', {
        'form': form,
         'titulo_pagina': 'Editar obra',
        'obra': obra,
    })
@login_required
@permission_required('obras.delete_obra', raise_exception=True)
def excluir_obra(request, id):
    obra = get_object_or_404(Obra, id=id)

    if request.method == 'POST':
        obra.delete()
        messages.success(request, 'Obra excluída com sucesso.')
        return redirect('listar_obras')

    return render(request, 'obras/excluir.html', {
        'obra': obra,
    })
