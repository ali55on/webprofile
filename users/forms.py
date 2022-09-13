from datetime import datetime
from django import forms
from tempus_dominus.widgets import DatePicker
from webprofile.models import Post
from users.models import FormUser


class LoginForms(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = FormUser
        fields = ['username', 'password']
        labels = {
            'username': 'Nome de usuário',
            'password': 'Senha',
        }
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean(self):
        fields = {
            'username': self.cleaned_data.get('username'),
            'password': self.cleaned_data.get('password')}

        errors = {}

        for key, value in fields.items():
            if not value.strip():
                errors[key] = 'Preencha este campo'

        if not fields['username'].isalpha():
            errors['name'] = 'Só é permitido letras neste campo'

        if errors:
            for erro in errors:
                error_message = errors[erro]
                self.add_error(erro, error_message)
        return self.cleaned_data


class SignUpForms(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = FormUser
        fields = '__all__'
        labels = {
            'name': 'Nome',
            'username': 'Nome de usuário (Letras)',
            'email': 'Email',
            'password': 'Senha (Mínimo 8 Letras e números)',
            'password_confirm': 'Senha novamente',
        }
        widgets = {
            'password': forms.PasswordInput(),
            'password_confirm': forms.PasswordInput(),
        }

    def clean(self):
        fields = {
            'name': self.cleaned_data.get('name'),
            'username': self.cleaned_data.get('username'),
            'email': self.cleaned_data.get('email'),
            'password': self.cleaned_data.get('password'),
            'password_confirm': self.cleaned_data.get('password_confirm')}

        errors = {}

        for key, value in fields.items():
            if not value.strip():
                errors[key] = 'Preencha este campo'

        if not fields['username'].isalpha():
            errors['name'] = 'Só é permitido letras neste campo'

        if errors:
            for erro in errors:
                error_message = errors[erro]
                self.add_error(erro, error_message)
        return self.cleaned_data


class PostForms(forms.ModelForm):
    publication_date = forms.DateTimeField(
        initial=datetime.now,
        label='Data de publicação',
        disabled=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Post
        fields = '__all__'
        labels = {
            'user': 'Usuário',
            'title': 'Título',
            'image': 'Imagem',
            'summary': 'Resumo',
            'content': 'Conteúdo',
            'category': 'Categoria',
            'post_is_published': 'Marcar como publicado',
        }

        widgets = {
            'publication_date': DatePicker(),
        }
