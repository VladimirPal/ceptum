from django.conf.urls.defaults import *

urlpatterns = patterns('',
                      url(r'^$', 'catalog.views.index', name="main-page"),
                      url(r'^video-solutions$', 'catalog.views.video_solutions', name="video-solutions-page"),
                      url(r'^office$', 'catalog.views.office', name="office-page"),
                      url(r'^store$', 'catalog.views.store', name="store-page"),
                      url(r'^house$', 'catalog.views.house', name="house-page"),
                      url(r'^podezd$', 'catalog.views.podezd', name="podezd-page"),
                      url(r'^autoservice$', 'catalog.views.autoservice', name="autoservice-page"),
                      url(r'^autostore$', 'catalog.views.autostore', name="autostore-page"),
                      url(r'^otel$', 'catalog.views.hotel', name="hotel-page"),
                      url(r'^cats/all-goods/$', 'catalog.views.all_goods', name="all-goods"),
                      url(r'^cats/(?P<category_slug>[-\w]+)/$', 'catalog.views.show_category', name="catalog-page"),
                      url(r'^section/(?P<section_slug>[-\w]+)/$', 'catalog.views.show_section', name="section-page"),
                      url(r'^products/(?P<product_slug>[-\w]+)/$', 'catalog.views.show_product', name="product-page"),
                      url(r'^about$', 'catalog.views.about', name="about-page"),
                      url(r'^install$', 'catalog.views.install', name="install-page"),
                      url(r'^service$', 'catalog.views.service', name="service-page"),
                      url(r'^take_form$', 'catalog.views.take_call_form', name="call-form"),
                      url(r'^take_vk_comment$', 'catalog.views.take_vk_comment', name="vk-comment"),
)

