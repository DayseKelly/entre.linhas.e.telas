from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import Escola
from .forms import EscolaForm
from django.contrib.auth.decorators import login_required, permission_required


@login_required
@permission_required('escolas.view_escola', raise_exception=True)
def listar_escolas(request):
    escolas = Escola.objects.all()
    return render(request, 'lista_escolas.html', {'escolas': escolas})


@login_required
@permission_required('escolas.add_escola', raise_exception=True)
def criar_escola(request):
    if request.method == 'POST':
        form = EscolaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Escola cadastrada com sucesso.')
            return redirect('listar_escolas')
    else:
        form = EscolaForm()
    return render(request, 'form_escolas.html', {'form': form})

@login_required
@permission_required('escolas.view_escola', raise_exception=True)
def detalhe_escola(request, id):
    escola = get_object_or_404(Escola, id=id)
    return render(request, 'detalhe_escola.html', {'escola': escola})

@login_required
@permission_required('escolas.change_escola', raise_exception=True)
def editar_escola(request, id):
    escola = get_object_or_404(Escola, id=id)

    if request.method == 'POST':
        form = EscolaForm(request.POST, instance=escola)
        if form.is_valid():
            form.save()
            messages.success(request, 'Escola editada com sucesso.')
            return redirect('detalhe_escola', id=escola.id)
    else:
        form = EscolaForm(instance=escola)

    return render(request, 'form_escolas.html', {
        'form': form,
        'titulo_pagina': 'Editar escola',
    })

@login_required
@permission_required('escolas.delete_escola', raise_exception=True)
def excluir_escola(request, id):
    escola = get_object_or_404(Escola, id=id)

    if request.method == 'POST':
        escola.delete()
        messages.success(request, 'Escola excluída com sucesso.')
        return redirect('listar_escolas')

    return render(request, 'excluir_escola.html', {'escola': escola})

# Create your views here.
