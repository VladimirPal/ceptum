SEND_SMS = True

EMS = 300
COURIER = 400

try:
    from local_settings import *
except ImportError:
    pass
