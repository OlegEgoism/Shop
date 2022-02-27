from .cart import Cart
from django.template import RequestContext

def cart(request):
    # print(request.session._get_session())
    return {'cart': Cart(request)}

