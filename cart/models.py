          # -*- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import smart_unicode
from datetime import date
from catalog.models import Product

class CartProduct(models.Model):
    cartitem = models.ForeignKey('CartItem')
    product = models.ForeignKey(Product, verbose_name='Товар')
    quantity = models.IntegerField(default=1, verbose_name='Количество')

    def delete(self, using=None):
        for f in self._meta.fields:
            if f.name == 'cartitem':
                try:
                    client = Client.objects.get(cart=self.cartitem)
                    client.change_log += u"%s - %s удалил %s(%s шт)<br>\r" % (date.today(), client.last_user, self.product, self.quantity)
                    client.save()
                except :
                    pass
        super(CartProduct, self).delete() # Call the "real" save() method.


    def save(self, force_insert=False, force_update=False, using=None):
        not_new = self.pk
        if not_new:
            old = CartProduct.objects.get(pk=self.pk)
            try:
                client = Client.objects.get(cart=old.cartitem.pk)
                for f in self._meta.fields:
                    if f.value_from_object(old) != f.value_from_object(self):
                        if f.name == 'quantity':
                            if old.product == self.product:
                                client.change_log += u"%s - %s изменил %s с %s шт на %s шт<br>\r" % (date.today() ,client.last_user, self.product, f.value_from_object(old), f.value_from_object(self))
                                client.save()
                        elif f.name == 'product':
                            old_product = Product.objects.get(pk=f.value_from_object(old))
                            new_product = Product.objects.get(pk=f.value_from_object(self))
                            client.change_log += u"%s - %s изменил %s(%s шт) на %s(%s шт)<br>\r" % (date.today(), client.last_user, old_product, old.quantity, new_product, self.quantity)
                            client.save()
            except:
                pass
        super(CartProduct, self).save() # Call the "real" save() method.
        if not self.pk == not_new:
            try:
                client = Client.objects.get(cart=self.cartitem)
                if not "добавил клиента" in client.change_log.split('\r')[len(client.change_log.split('\r')) - 2].encode('utf-8'):
                    for f in self._meta.fields:
                        if f.name == 'cartitem':
                            client.change_log += u"%s - %s добавил %s(%s шт)<br>\r" % (date.today(), client.last_user, self.product, self.quantity )
                            client.save()
            except:
                pass

class CartItem(models.Model):
    cart_id = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)
    product = models.ManyToManyField(Product, through=CartProduct)

    class Meta:
        db_table = 'cart_item'

DELIVERY_CHOICES = (
    ('EMS', 'EMS'),
    ('COURIER', 'Курьер'),
)

STATUS_CHOICES = (
    ('PROCESS', 'Обработать'),
    ('POSTSEND', 'Отправить почтой'),
    ('COURIER_SEND', 'Отправить курьером'),
    ('BACK', 'Обмен/Возврат'),
    ('CONTACT_AT', 'Связаться'),
    ('COURIER_TAKE', 'Передано курьеру'),
    ('BUYER_TAKE', 'Передано покупателю'),
    ('WAYT_PRODUCT', 'Ожидание поступления товара'),
    ('POSTSENDED', 'Отправлено почтой'),
    ('CASH_IN', 'Деньги внесены'),
    ('REFUSED', 'Снятие заявки клиентом'),
)

class Client(models.Model):
    surname = models.CharField(max_length=50, null=True, blank=True, verbose_name="Фамилия")
    name = models.CharField(max_length=50, verbose_name="Имя")
    patronymic = models.CharField(max_length=50, null=True, blank=True, verbose_name="Отчество")
    city = models.CharField(max_length=50, null=True, blank=True, verbose_name="Город")
    postcode = models.IntegerField(null=True, blank=True, verbose_name="Индекс")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    address = models.CharField(max_length=500, null=True, blank=True, verbose_name="Адрес")
    email = models.EmailField(null=True, blank=True)
    cart = models.ForeignKey(CartItem)
    ordered_at = models.DateTimeField(auto_now_add=True )
    subtotal = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2, verbose_name="Сумма")
    discount = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2, verbose_name="Скидка")
    tracking_number = models.CharField(max_length=20, null=True, blank=True)
    tracking_status = models.CharField(max_length=500, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name="Статус", default='PROCESS')
    sms_status = models.NullBooleanField()
    referrer = models.URLField(verify_exists=False, max_length=500)
    comment = models.TextField(null=True, blank=True, verbose_name='Комментарий')
    execute_at = models.DateTimeField(editable=True,null=True, blank=True, verbose_name='Время исполнения')
    delivery = models.CharField(max_length=20, choices=DELIVERY_CHOICES, null=True, blank=True, verbose_name='Способ доставки')
    last_user = models.CharField(max_length=200, null=True, blank=True)
    change_log = models.TextField(null=True, blank=True)

    def get_order(self):
        cart_items = CartProduct.objects.filter(cartitem = self.cart.id)
        products = ""
        for item in cart_items:
            products += u"<a href=\"%s\" target=\"_blank\">%s</a> - %sшт<br> " % (item.product.get_absolute_url(), item.product.slug, item.quantity )
        return products

    class Meta:
        ordering = ['-ordered_at']

    def __unicode__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None):
        not_new = self.pk
        if not self.last_user:
            user = u"Сайт"
        else:
            user = self.last_user
        if not_new:
            old = Client.objects.get(pk=self.pk)
            for f in self._meta.fields:
                if f.value_from_object(old) != f.value_from_object(self):
                    if not f.name == 'subtotal':
                        if not f.name == 'discount':
                            if not f.name == 'change_log':
                                if not f.name == 'last_user':
                                    if not f.name == 'tracking_status':
                                        if f.name == 'status':
                                            if f.value_from_object(old):
                                                self.change_log += u"%s - %s изменил %s с %s на %s<br>\r" %\
                                                  (date.today(), user, smart_unicode(Client._meta.get_field(f.name).verbose_name),
                                                   old.get_status_display(), self.get_status_display())
                                            else:
                                                self.change_log += u"%s - %s добавил %s %s<br>\r" %\
                                                             (date.today(), user, smart_unicode(Client._meta.get_field(f.name).verbose_name),
                                                              self.get_status_display())
                                        elif f.name == 'delivery':
                                            if f.value_from_object(old):
                                                self.change_log += u"%s - %s изменил %s с %s на %s<br>\r" %\
                                                  (date.today(), user, smart_unicode(Client._meta.get_field(f.name).verbose_name),
                                                   old.get_delivery_display(), self.get_delivery_display())
                                            else:
                                                self.change_log += u"%s - %s добавил %s %s<br>\r" %\
                                                             (date.today(), user, smart_unicode(Client._meta.get_field(f.name).verbose_name),
                                                              self.get_delivery_display())
                                        else:
                                            if f.value_from_object(old):
                                                self.change_log += u"%s - %s изменил %s с %s на %s<br>\r" %\
                                                  (date.today(), user, smart_unicode(Client._meta.get_field(f.name).verbose_name),
                                                   f.value_from_object(old), f.value_from_object(self))
                                            else:
                                                self.change_log += u"%s - %s добавил %s %s<br>\r" %\
                                                             (date.today(), user, smart_unicode(Client._meta.get_field(f.name).verbose_name),
                                                              f.value_from_object(self))
        super(Client, self).save() # Call the "real" save() method.
        if not not_new == self.pk:
            client = Client.objects.get(pk=self.pk)
            client.change_log = u"%s - %s добавил клиента<br>\r" % (date.today(), user)
            client.save()
