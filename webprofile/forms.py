from django import forms
from webprofile.models import Post
from django_quill.forms import QuillFormField


class PostForms(forms.ModelForm):

    content = QuillFormField(
        label=('<h5>Conteúdo</h5><small class="text-muted">'
               'Matéria da postagem</small>'))

    is_published = forms.BooleanField(
        label='<h5>Marcar como publicado</h5>',
        initial=True, required=False)

    is_for_main_page = forms.BooleanField(
        label='<h5>Publicar na página inicial</h5>',
        initial=False, required=False)

    is_locked_for_review = forms.BooleanField(
        label='<h5>Bloqueado para revisão</h5>',
        initial=False, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if (visible.name != 'is_published'
                    and visible.name != 'is_for_main_page'
                    and visible.name != 'is_locked_for_review'):
                visible.field.widget.attrs['class'] = 'form-control'

            if visible.name == 'publication_date':
                # visible.field.widget = forms.HiddenInput()
                visible.field.widget.attrs['readonly'] = 'readonly'

    class Meta:
        model = Post
        exclude = ['user', 'publication_date', 'url_title', 'is_for_main_page']

        labels = {
            'title': '<h5>Título</h5>',
            'image': (
                '<h5>Imagem</h5>'
                '<small class="text-muted">Capa do card</small>'),
            'summary': (
                '<h5>Resumo</h5><small class="text-muted">'
                'Apresentação resumida do card</small>'),
            'category': (
                '<h5>Categoria</h5><small class="text-muted">'
                'Separe por vírgula</small>'),
            'review_reason': (
                '<h5>Mensagem da revisão</h5><small class="text-muted">'
                'Motivo do bloqueio. '
                'Se for excluir, avise quando e porque</small>'),
        }

        widgets = {
            'summary': forms.Textarea(attrs={'rows': 2}),  # 'cols': 15
            'review_reason': forms.Textarea(attrs={'rows': 2}),
            # 'content': forms.Textarea(attrs={'rows': 10}),
        }

    def clean(self):
        errors = {}

        # wayfinder_map_form.cleaned_data['media_file']
        if not self.cleaned_data.get('image'):
            errors['image'] = 'Cadê a imagem pô?!'

        if errors:
            for erro in errors:
                error_message = errors[erro]
                self.add_error(erro, error_message)
        return self.cleaned_data
