from django import forms
from .models import Categoria, Transaccion
from django.utils import timezone

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'tipo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Sueldo, Comida, Arriendo'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'nombre': 'Nombre de la Categoría',
            'tipo': 'Tipo de Categoría',
        }

class TransaccionForm(forms.ModelForm):
    fecha = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
        initial=timezone.now().date(), # Establece la fecha actual por defecto
        label='Fecha de la Transacción'
    )

    class Meta:
        model = Transaccion
        fields = ['descripcion', 'monto', 'fecha', 'categoria', 'notas']
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Compra supermercado, Pago de cuenta luz'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Ej: 25000.50'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Detalles adicionales (opcional)'}),
        }
        labels = {
            'descripcion': 'Descripción',
            'monto': 'Monto ($)',
            'categoria': 'Categoría',
            'notas': 'Notas Adicionales',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].queryset = Categoria.objects.all().order_by('nombre')
        self.fields['categoria'].empty_label = "Seleccione una categoría"