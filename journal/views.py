from django.shortcuts import render,redirect
from .models import Item,Transaction
from .forms import itemForm,TransactionFormSet
from django.contrib import messages

# Create your views here.

def journalMain(request):
    """
        Carga pagina principal de partidas
    """
    ItemsShow = Item.objects.all().order_by('date')
    transaccionShow = Transaction.objects.all()


    objects = {
        "items":ItemsShow,
        "transaccion":transaccionShow
    }
    return render(request,'journalMain.html',objects)


def formItem(request):
    """
    Vista para agregar un nuevo Item junto con sus transacciones.
    """
    item = None
    title = "Agregar Partida"

    if request.method == 'POST':
        formItem = itemForm(request.POST)
        formTrans = TransactionFormSet(request.POST, instance=item)

        if formItem.is_valid() and formTrans.is_valid():
            item = formItem.save()
            formTrans.instance = item
            formTrans.save()

            messages.success(request, "La partida y sus transacciones se han guardado exitosamente.")
            return redirect('journalMain')
        else:
            if not formItem.is_valid():
                messages.error(request, "Error en el formulario de la partida.")
            if not formTrans.is_valid():
                messages.error(request, "El debe y el haber deben de estar balanceado.")
    else:
        formItem = itemForm()
        formTrans = TransactionFormSet(instance=item)

    objects = {
        "itemForm": formItem,
        "transForm": formTrans,
        "title": title
    }

    return render(request, 'formItem.html', objects)


def editItem(request, pk):
    """
    Editar una partida existente junto con sus transacciones.
    """
    item = Item.objects.get(pk=pk)
    title = "Editar Partida"

    if request.method == 'POST':
        # Crear el formulario con los datos de POST
        formItem = itemForm(request.POST, instance=item)
        formTrans = TransactionFormSet(request.POST, instance=item)

        # Actualizar manualmente la fecha del item desde el campo oculto si es necesario
        if 'date' in request.POST:
            item.date = request.POST['date']

        if formItem.is_valid() and formTrans.is_valid():
            formItem.save()
            formTrans.save()

            messages.success(request, "La partida y sus transacciones se han actualizado correctamente.")
            return redirect('journalMain')
        else:
            messages.error(request, "Ocurrió un error al actualizar la partida. Por favor, revisa los datos.")
    else:
        formItem = itemForm(instance=item)
        formTrans = TransactionFormSet(instance=item)

    objects = {
        "itemForm": formItem,
        "transForm": formTrans,
        "title": title,
        "is_edit": True,
        "item_date": item.date.strftime('%Y-%m-%d')  # Formatear fecha para mostrarla
    }
    return render(request, 'formItem.html', objects)







def deleteItem(request, pk):
    """
    Confirmar y eliminar una partida.
    """
    item = Item.objects.get(pk=pk)

    if request.method == 'POST':
        item.delete()
        messages.success(request, "La partida se eliminó correctamente.")
        return redirect('journalMain')

    return render(request, 'delete_confirmation.html', {'item': item})
