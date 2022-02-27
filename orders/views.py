from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm, AllFrom, AFrom
from cart.cart import Cart
from .tasks import add

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # очистка корзины
            cart.clear()
            return render(request, 'orders/order/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm
    return render(request, 'orders/order/create.html',
                  {'cart': cart, 'form': form})


def getform(request):
    form = AFrom()
    if request.method == 'POST':
        form = AFrom(request.POST)
        if form.is_valid():
            form.save()
            a = AllFrom.objects.all()
            v = form.cleaned_data.get('number')
            res = add.delay(v)

            print(res)
            context = {
                'form': form,
                'a': a,
                'v': v
            }
            return render(request, 'orders/order/form.html', context=context)
    return render(request, 'orders/order/form.html', {'form': form})
