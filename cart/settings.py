SEND_SMS = True
SEND_ADMIN_EMAIL = True
SEND_CLIENT_EMAIL = True
DISCOUNT = True
DISCOUNT_PERCENT = 10
COUNT_FOR_DISCOUNT = 2

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'info@my-spy.ru'
EMAIL_HOST_PASSWORD = 'kjaH71baHGas'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

try:
    from local_settings import *
except ImportError:
    pass