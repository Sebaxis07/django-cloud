from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from .models import Categoria, Transaccion
from .forms import CategoriaForm, TransaccionForm
from django.utils import timezone
from decimal import Decimal
import datetime
from django.db.models import ProtectedError

from tracker import models

# Vistas para Categoría
def categoria_list_view(request):
    categorias = Categoria.objects.all().order_by('nombre')
    ingreso_count = categorias.filter(tipo='INGRESO').count()
    egreso_count = categorias.filter(tipo='EGRESO').count()

    context = {
        'categorias': categorias,
        'ingreso_count': ingreso_count,
        'egreso_count': egreso_count,
        'current_year': datetime.date.today().year,
    }
    return render(request, 'categoria_list.html', context)


def categoria_create_view(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada exitosamente.')
            return redirect('tracker:categoria_list')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = CategoriaForm()
    context = {
        'form': form,
        'current_year': datetime.date.today().year,
        'form_title': 'Nueva Categoría',
        'submit_button_text': 'Crear Categoría'
    }
    return render(request, 'categoria_form.html', context)

def categoria_update_view(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría actualizada exitosamente.')
            return redirect('tracker:categoria_list')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = CategoriaForm(instance=categoria)
    context = {
        'form': form,
        'categoria': categoria,
        'current_year': datetime.date.today().year,
        'form_title': f'Editar Categoría: {categoria.nombre}',
        'submit_button_text': 'Actualizar Categoría'
    }
    return render(request, 'categoria_form.html', context)

def categoria_delete_view(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        try:
            categoria.delete()
            messages.success(request, 'Categoría eliminada exitosamente.')
            return redirect('tracker:categoria_list')
        except models.ProtectedError:
            messages.error(request, 'No se puede eliminar esta categoría porque tiene transacciones asociadas.')
            return redirect('tracker:categoria_list')
    context = {
        'categoria': categoria,
        'current_year': datetime.date.today().year,
    }
    return render(request, 'categoria_confirm_delete.html', context)


# Vistas para Transacción
def transaccion_list_view(request):
    today = timezone.now().date()
    selected_month = request.GET.get('month', str(today.month))
    selected_year = request.GET.get('year', str(today.year))

    try:
        selected_month = int(selected_month)
        selected_year = int(selected_year)
    except ValueError:
        selected_month = today.month
        selected_year = today.year

    transacciones = Transaccion.objects.filter(
        fecha__year=selected_year,
        fecha__month=selected_month
    ).order_by('-fecha', '-id')

    total_ingresos = sum(t.monto for t in transacciones if t.categoria.tipo == 'INGRESO')
    total_egresos = sum(t.monto for t in transacciones if t.categoria.tipo == 'EGRESO')
    balance = total_ingresos - total_egresos

    # Para los selectores de mes y año
    years = range(datetime.date.today().year - 5, datetime.date.today().year + 2)
    months = [(i, datetime.date(selected_year, i, 1).strftime('%B')) for i in range(1, 13)]


    context = {
        'transacciones': transacciones,
        'total_ingresos': total_ingresos,
        'total_egresos': total_egresos,
        'balance': balance,
        'selected_month': selected_month,
        'selected_year': selected_year,
        'months': months,
        'years': years,
        'current_year_template': datetime.date.today().year, # Para el footer
    }
    return render(request, 'transaccion_list.html', context)


def transaccion_create_view(request):
    if request.method == 'POST':
        form = TransaccionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transacción creada exitosamente.')
            return redirect('tracker:transaccion_list')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = TransaccionForm()
    context = {
        'form': form,
        'current_year': datetime.date.today().year,
        'form_title': 'Nueva Transacción',
        'submit_button_text': 'Crear Transacción'
    }
    return render(request, 'transaccion_form.html', context)

def transaccion_update_view(request, pk):
    transaccion = get_object_or_404(Transaccion, pk=pk)
    if request.method == 'POST':
        form = TransaccionForm(request.POST, instance=transaccion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transacción actualizada exitosamente.')
            return redirect('tracker:transaccion_list')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = TransaccionForm(instance=transaccion)
    context = {
        'form': form,
        'transaccion': transaccion,
        'current_year': datetime.date.today().year,
        'form_title': f'Editar Transacción: {transaccion.descripcion[:30]}...',
        'submit_button_text': 'Actualizar Transacción'
    }
    return render(request, 'transaccion_form.html', context)

def transaccion_delete_view(request, pk):
    transaccion = get_object_or_404(Transaccion, pk=pk)
    if request.method == 'POST':
        transaccion.delete()
        messages.success(request, 'Transacción eliminada exitosamente.')
        return redirect('tracker:transaccion_list')
    context = {
        'transaccion': transaccion,
        'current_year': datetime.date.today().year,
    }
    return render(request, 'transaccion_confirm_delete.html', context)