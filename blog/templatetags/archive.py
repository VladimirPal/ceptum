from django import template
from datetime import date
from blog.models import Entry, Category

register = template.Library()

def spanning_months(start, end):
    assert start <= end
    current = start.year * 12 + start.month - 1
    end = end.year * 12 + end.month - 1
    while current <= end:
        yield date(current // 12, current % 12 + 1, 1)
        current += 1

@register.inclusion_tag("blog/tags/archive.html")
def archive():
    latest_entry = Entry.objects.all().latest('id').date
    first_entry = Entry.objects.order_by()[0].date
    dates = spanning_months(first_entry, latest_entry)

    return {
        'dates': dates,
        }

@register.inclusion_tag("blog/tags/categories.html")
def categories():
    categories = Category.objects.all()
    return {
        'categories': categories,
        }
