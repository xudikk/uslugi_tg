# -*- coding: utf-8 -*-
import ast
from contextlib import closing
from collections import OrderedDict

from django.db import connection

from base.utils.db import dictfetchall, dictfetchone


def one_product(request, id):
    extra_sql = f"""
        select id, fullname, region_id, phone_number, description, price, user_id
        from tg_announce 
        where id = {id}
    """

    with closing(connection.cursor()) as cursor:
        cursor.execute(extra_sql, [id])
        data = dictfetchone(cursor)
        if data:
            result = _format(data)
        else:
            result = None
    return OrderedDict([
        ('item', result),
    ])


def _format(data):
    return OrderedDict([
        ('id', data['id']),
        ('fullname', data['fullname']),
        ('region_id', data['region_id']),
        ('phone_number', data['phone_number']),
        ('description', data['description']),
        ('price', data['price']),
        ('user', data['user_id']),

    ])
