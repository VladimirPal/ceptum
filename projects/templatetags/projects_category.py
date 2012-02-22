from django import template
from projects.models import Category

register = template.Library()

@register.inclusion_tag("projects/tags/categories.html")
def category(request):
    categories = Category.objects.all()
    return {
        'categories': categories,
        'request_path': request.path,
        }