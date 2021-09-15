# -*- coding: utf-8 -*-
import ast
from contextlib import closing
from collections import OrderedDict

from django.db import connection

from base.utils.db import dictfetchall, dictfetchone


def one_product(request, id):
    extra_sql = f"""
        select resume_id, category_id
        from tg_announcecategories 
        where resume_id = {id}
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
        ('resume', data['resume_id']),
        ('category', data['category_id']),
    ])
