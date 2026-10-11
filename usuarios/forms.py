from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.html import format_html, format_html_join
from escolas.constants import CAMPI_IF_BAIANO
from escolas.models import Escola
from .models import Usuario

User = get_user_model()


def _senha_validacao_ajuda_pt_br():
    mensagens = [
        'A senha não pode ser muito parecida com suas outras informações pessoais.',
        'Pelo menos 8 caracteres.',
        'A senha não pode ser tão comum.',
        'A senha não pode conter apenas números.',
    ]
    itens = format_html_join('', '<li>{}</li>', ((mensagem,) for mensagem in mensagens))
    return format_html('<ul>{}</ul>', itens)


def _traduzir_erro_senha(mensagem):
    traducao = {
        'This password is too similar to the username.': 'A senha é muito parecida com o nome de usuário.',
        'This password is too similar to your other personal information.': 'A senha é muito parecida com suas outras informações pessoais.',
        'This password is too short. It must contain at least 8 characters.': 'A senha é muito curta. Ela deve conter pelo menos 8 caracteres.',
        'This password is too common.': 'A senha é muito comum.',
        'A senha é muito comum.': 'A senha é muito comum.',
        'This password is entirely numeric.': 'A senha não pode conter apenas números.',
        'A senha é muito curta. Ela deve conter pelo menos 8 caracteres.': 'A senha é muito curta. Ela deve conter pelo menos 8 caracteres.',
    }
    return traducao.get(mensagem, mensagem)


def _configurar_busca_escola(form):
    campo = form.fields['escola']
    campo.queryset = campo.queryset.filter(nome__in=CAMPI_IF_BAIANO)
    campo.widget = forms.HiddenInput()
    escola_id = form.data.get('escola') if form.is_bound else form.initial.get('escola')
    if not escola_id and form.instance.pk:
        escola_id = form.instance.escola_id
    try:
        escola = campo.queryset.filter(pk=escola_id).first() if escola_id else None
    except (TypeError, ValueError):
        escola = None
    if escola:
        campo.widget.attrs['data-selected-label'] = str(escola)


class UsuarioForm(forms.ModelForm):
    username = forms.CharField(max_length=150, label='Nome de usuário')
    password = forms.CharField(label='Senha', widget=forms.PasswordInput, strip=False)

    class Meta:
        model = Usuario
        fields = ['data_nasc', 'rg', 'cpf', 'escola']
        labels = {
            'data_nasc': 'Data de nascimento',
            'rg': 'RG',
            'cpf': 'CPF',
            'escola': 'Escola',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['username'].initial = self.instance.user.username
            self.fields.pop('password')
        else:
            self.fields['password'].required = True
        _configurar_busca_escola(self)

    def clean_username(self):
        username = self.cleaned_data['username']
        users = User.objects.filter(username=username)
        if self.instance.pk:
            users = users.exclude(pk=self.instance.user_id)
        if users.exists():
            raise forms.ValidationError('Este nome de usuário já está em uso.')
        return username


class CadastroPublicoForm(forms.ModelForm):
    username = forms.CharField(max_length=150, label='Nome de usuário')
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=_senha_validacao_ajuda_pt_br(),
    )
    password_confirmation = forms.CharField(
        label='Confirme a senha',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
    )
    escola = forms.ModelChoiceField(
        queryset=Escola.objects.filter(nome__in=CAMPI_IF_BAIANO),
        label='Escola',
        widget=forms.HiddenInput(),
    )

    class Meta:
        model = Usuario
        fields = ['data_nasc', 'rg', 'cpf', 'escola']
        labels = {
            'data_nasc': 'Data de nascimento',
            'rg': 'RG',
            'cpf': 'CPF',
            'escola': 'Escola',
        }
        widgets = {'data_nasc': forms.DateInput(attrs={'type': 'date'})}

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Este nome de usuário já está em uso.')
        return username

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _configurar_busca_escola(self)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirmation = cleaned_data.get('password_confirmation')

        if password and confirmation and password != confirmation:
            self.add_error('password_confirmation', 'As senhas não coincidem.')
        elif password:
            user = User(username=cleaned_data.get('username', ''))
            try:
                validate_password(password, user)
            except ValidationError as error:
                for mensagem in error.messages:
                    self.add_error('password', _traduzir_erro_senha(mensagem))

        return cleaned_data

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
        )
        perfil = super().save(commit=False)
        perfil.user = user
        perfil.save()
        return perfil
