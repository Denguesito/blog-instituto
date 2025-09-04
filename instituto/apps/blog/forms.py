from django import forms
from .models import Articulo, ImagenArticulo
from django.core.exceptions import ValidationError


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

    def clean_imagenes(self):
        """Validación de las imágenes subidas"""
        imagenes = self.files.getlist('imagenes')
        max_size = 5 * 1024 * 1024  # 5MB

        for img in imagenes:
            # Validar extensión
            if not img.content_type in ['image/jpeg', 'image/png', 'image/gif', 'image/webp']:
                raise ValidationError(f"El archivo {img.name} no es un tipo de imagen válido.")

            # Validar tamaño
            if img.size > max_size:
                raise ValidationError(f"El archivo {img.name} supera el tamaño máximo de 5MB.")

        return imagenes
