# -*- coding: utf-8 -*-
import ast
from contextlib import closing
from collections import OrderedDict

from django.db import connection

from base.utils.db import dictfetchall, dictfetchone


def one_product(request, id):
    extra_sql = f"""
    
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
        ('user_id', data['user_id']),
        ('first_name', data['first_name']),
        ('last_name', data['last_name']),
        ('user_name', data['user_name']),
        ('lang', data['lang']),
        ('menu_log', data['menu_log']),

    ])
