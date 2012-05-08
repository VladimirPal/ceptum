          # -*- coding: utf-8 -*-

def valid_client_form(postdata):
    errors = {}
    name = postdata.get('name','')
    contacts = postdata.get('contacts','')
    status = postdata.get('status','')
    manager = postdata.get('manager','')
    if not name:
        errors['name'] = 'Введите название'
    if not contacts:
        errors['contacts'] = 'Введите контактное лицо'
    if not status:
        errors['status'] = 'Укажите статус'
    if not manager:
        errors['manager'] = 'Укажите исполнителя'
    return errors
