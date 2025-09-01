from django import forms
from .models import Articulo, ImagenArticulo

# Widget custom para permitir múltiples archivos
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class ArticuloForm(forms.ModelForm):
    # Campo extra para subir varias imágenes
    imagenes = forms.FileField(
        widget=MultipleFileInput(attrs={'multiple': True}),
        required=False,
        label="Imágenes"
    )

    class Meta:
        model = Articulo
        fields = ['titulo', 'contenido', 'categoria', 'destacado']
        widgets = {
            'contenido': forms.Textarea(attrs={
                'class': 'textarea_custom1',
                'rows': 10,
                'cols': 80,
            }),
        }

