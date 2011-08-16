from django import template
from cart import cart

register = template.Library()

@register.inclusion_tag("cart/cart_box.html")
def cart_box(request):
    box_count = cart.cart_count(request)
    return {
        'box_count': box_count,
}
