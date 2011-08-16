from django.conf.urls.defaults import *

urlpatterns = patterns('',
                       url(r'^$', 'cart.views.show_cart', name="show_cart"),
)
