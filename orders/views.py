from symbol import test

from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm, AllFrom, AFrom, HomeForm
from cart.cart import Cart
# from .tasks import add
from .new_celery import add


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


def celeryhome(request):
    form = HomeForm()
    if request.method == 'POST':
        form = HomeForm(request.POST)
        if form.is_valid():
            num = form.cleaned_data
            # print(num.get('number'))

            # result = add.delay(num.get('number'))
            result = test.delay(num.get('number'))
            print(len(result.id))
            # print(num.get('number'))

            context = {'form': form,
                       'task_id': result.id,
                       }
            return render(request, 'orders/order/home.html', context=context)
    context = {'form': form
               }
    return render(request, 'orders/order/home.html', context=context)


def getcelery(request):
    if request.method == "POST":
        task = add.delay(4)
        context = {'Work': 'задача'}
        return render(request, 'orders/order/getcelery.html', context=context)

    return render(request, 'orders/order/getcelery.html')