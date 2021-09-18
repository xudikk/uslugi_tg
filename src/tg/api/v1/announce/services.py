# -*- coding: utf-8 -*-
import ast
from contextlib import closing
from collections import OrderedDict
from django.conf import settings
from django.db import connection
from base.utils.sqlpaginator import SqlPaginator
from base.utils.db import dictfetchall, dictfetchone
PER_PAGE = settings.PAGINATE_BY

def all_announse(request, form, to, region_id):
    try:
        page = int(request.GET.get('page', 1))
    except:
        page = 1
    offset = (page - 1) * PER_PAGE

    extra_sql = f"""
    select fullname , phone_number , (price->>'from')::int as price_from, (price->>'to')::int as price_to, description, is_active,
    region_id, user_id, gr."name"->>'uz' as name_uz, gr."name"->>'ru' as name_ru
    from tg_announce ta 
    inner join geo_region gr ON gr.id = {region_id} 
    where {form} <= (price->>'from')::int and {to} >= (price->>'to')::int
"""
    with closing(connection.cursor()) as cursor:
        cursor.execute(extra_sql, [PER_PAGE, offset])
        items = dictfetchall(cursor)
        result = []
        for data in items:
            result.append(_format_(data))

    with closing(connection.cursor()) as cursor:
        cursor.execute(
            "SELECT count(1) as cnt from tg_announce")
        row = dictfetchone(cursor)

    if row:
        count_records = row['cnt']
    else:
        count_records = 0

    paginator = SqlPaginator(request, page=1, per_page=PER_PAGE, count=count_records)
    pagging = paginator.get_paginated_response()

    return OrderedDict([
        ('items', result),
        ('meta', pagging)
    ])

def one_product(request, id):
    extra_sql = f"""
    select fullname , phone_number , price->>'from' as price_from, price->>'to' as price_to, description, is_active, region_id, user_id
    from tg_announce ta 
    where id = %s
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



def _format_(data):
    return OrderedDict([
        ('fullname', data['fullname']),
        ('phone_number', data['phone_number']),
        ('price_from', data['price_from']),
        ('price_to', data['price_to']),
        ('description', data['description']),
        ('is_active', data['is_active']),
        ('region_id', data['region_id']),
        ('user_id', data['user_id']),
        ('region_name_uz', data['name_uz']),
        ('region_name_ru', data['name_ru']),

    ])


def _format(data):
    return OrderedDict([
        ('fullanme', data['fullname']),
        ('price_from', data['price_from']),
        ('price_to', data['price_to']),
        ('description', data['description']),
        ('is_active', data['is_active']),
        ('region_id', data['region_id']),
        ('user_id', data['user_id']),

    ])
