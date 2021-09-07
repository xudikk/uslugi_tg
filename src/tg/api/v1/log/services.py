# -*- coding: utf-8 -*-
import ast
from contextlib import closing
from collections import OrderedDict

from django.db import connection
from django.conf import settings

from base.utils.db import dictfetchall, dictfetchone
from base.utils.sqlpaginator import SqlPaginator


def one_product(request, tg_id):
    extra_sql = f"""
    select user_id, messages
    from tg_log
    where user_id = {tg_id}
    """

    with closing(connection.cursor()) as cursor:
        cursor.execute(extra_sql, [tg_id])
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
        ('messages', ast.literal_eval(data['messages'])),
    ])
