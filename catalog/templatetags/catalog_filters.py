from django import template
from catalog.models import Section
from cart import cart

register = template.Library()

@register.inclusion_tag("tags/sidebar.html")
def category_list(request):
    active_sections = Section.objects.filter(is_active=True)
    return {
        'request_path': request.path,
        'sections': active_sections,
        'request': request,
}

@register.inclusion_tag("cart/cart_box.html")
def cart_box(request):
    box_count = cart.cart_count(request)
    return {
        'box_count': box_count,
}

@register.filter
def div(value, arg):
    return value % arg
