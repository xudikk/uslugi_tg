# -*- coding: utf-8 -*-
import ast
from contextlib import closing
from collections import OrderedDict
from django.db import connection
from django.conf import settings

from base.utils.db import dictfetchall, dictfetchone
from base.utils.sqlpaginator import SqlPaginator

PER_PAGE = settings.PAGINATE_BY


def list_model(request):
    try:
        page = int(request.GET.get('page', 1))
    except:
        page = 1
    try:
        region = int(request.GET.get('region', 0))
    except:
        region = 0
    offset = (page - 1) * PER_PAGE
    if region:
        where = f"where geo_district.region_id={region}"
    else:
        where = ""

    extra_sql = f"""
    select geo_district.id, geo_district.name->>'uz' as name_uz, geo_district.name->>'ru' as name_ru, geo_district.sort_order,
    geo_region.id as region_id, geo_region.name->>'uz' as region_name_uz, geo_region.name->>'ru' as region_name_ru, geo_region.sort_order as region_sort_order
    from geo_district
    inner join geo_region on geo_district.region_id=geo_region.id {where}
    order by geo_district.sort_order asc
    limit %s OFFSET %s
"""
    with closing(connection.cursor()) as cursor:
        cursor.execute(extra_sql, [PER_PAGE, offset])
        items = dictfetchall(cursor)
        result = []
        for data in items:
            result.append(_format(data))

    with closing(connection.cursor()) as cursor:
        cursor.execute(
            "SELECT count(1) as cnt from geo_district")
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


def one_model(request, pk):
    extra_sql = f"""
    select geo_district.id, geo_district.name->>'uz' as name_uz, geo_district.name->>'ru' as name_ru, geo_district.sort_order,
    geo_region.id as region_id, geo_region.name->>'uz' as region_name_uz, geo_region.name->>'ru' as region_name_ru, geo_region.sort_order as region_sort_order
    from geo_district
    inner join geo_region on geo_district.region_id=geo_region.id
    where geo_district.id = %s
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


def _format(data):
    return OrderedDict([
        ('id', data['id']),
        ('name_1', data['name_uz']),
        ('name_2', data['name_ru']),
        ('sort_order', data['sort_order']),
        ('region', OrderedDict([
                ('id', data['region_id']),
                ('name_1', data['region_name_uz']),
                ('name_2', data['region_name_ru']),
                ('sort_order', data['region_sort_order'])
            ]))
    ])
