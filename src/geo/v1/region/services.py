# -*- coding: utf-8 -*-
import ast
from contextlib import closing
from collections import OrderedDict
from django.db import connection
from django.conf import settings

from base.utils.db import dictfetchone, dictfetchall
from base.utils.sqlpaginator import SqlPaginator

PER_PAGE = settings.PAGINATE_BY


def list_region(request):
    try:
        page = int(request.GET.get('page', 1))
    except:
        page = 1
    offset = (page - 1) * PER_PAGE

    extra_sql = f"""
    select id, name->>'uz' as name_uz, name->>'ru' as name_ru, sort_order  
    from geo_region
    order by sort_order asc
"""
    with closing(connection.cursor()) as cursor:
        cursor.execute(extra_sql, [PER_PAGE, offset])
        items = dictfetchall(cursor)
        result = []
        for data in items:
            result.append(_format(data))

    with closing(connection.cursor()) as cursor:
        cursor.execute(
            "SELECT count(1) as cnt from geo_region")
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


def one_region(request, pk):
    extra_sql = f"""
    select id, name->>'uz' as name_uz, name->>'ru' as name_ru, sort_order
    from geo_region
    where name->>'uz' = %s or name->>'ru' = %s
    """

    with closing(connection.cursor()) as cursor:
        cursor.execute(extra_sql, [pk])
        data = dictfetchone(cursor)
        if data:
            result = _format(data)
        else:
            result = None
    return OrderedDict([
        ('item', result),
    ])


def one_region_by_name(request, name):
    extra_sql = f"""
    select id, name->>'uz' as name_uz, name->>'ru' as name_ru, sort_order
    from geo_region
    where name->>'uz' ILIKE %s or name->>'ru' ILIKE %s
    """

    with closing(connection.cursor()) as cursor:
        cursor.execute(extra_sql, [name, name])
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
        ('name_1', data['name_uz']),
        ('name_2', data['name_ru']),
        ('sort_order', data['sort_order']),
    ])
