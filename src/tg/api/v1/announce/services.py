# -*- coding: utf-8 -*-
import ast
from contextlib import closing
from collections import OrderedDict
from django.conf import settings
from django.db import connection
from base.utils.sqlpaginator import SqlPaginator
from base.utils.db import dictfetchall, dictfetchone

PER_PAGE = settings.PAGINATE_BY


def all_announse(request, form, to, region_id, user_id=None):
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
            f"""SELECT count(1) as cnt from tg_announce  inner join geo_region gr ON gr.id = {region_id} 
    where {form} <= (price->>'from')::int and {to} >= (price->>'to')::int""")
        row = dictfetchone(cursor)

    if row:
        count_records = row['cnt']
    else:
        count_records = 0

    paginator = SqlPaginator(request, page=1, per_page=PER_PAGE, count=count_records)
    pagging = paginator.get_paginated_response()

    return OrderedDict([
        ('item', result),
        ('meta', pagging)
    ])


def get_all_user(request,  user_id=None):
    try:
        page = int(request.GET.get('page', 1))
    except:
        page = 1
    offset = (page - 1) * PER_PAGE

    extra_sql = f"""
   select ann.id, fullname, phone_number, coalesce(price->>'from', '') || '-' ||coalesce(price->>'to', '') as price, 
   description, geo."name"->>'uz' as region_name_uz, geo."name"->>'ru' as region_name_ru,
    cat."name"->>'uz' as category_name_uz, cat."name"->>'ru' as category_name_ru
    from tg_announce ann
    left join geo_region geo on ann.region_id = geo.id
    left join tg_announcecategories acat on ann.id = acat.resume_id 
    left join tg_category cat on acat.category_id = cat.id 
    where ann.user_id = %s and ann.is_active = True
    order by ann.id desc
    limit %s offset %s
"""
    with closing(connection.cursor()) as cursor:
        cursor.execute(extra_sql, [user_id, PER_PAGE, offset])
        data = dictfetchone(cursor)
        if data:
            result = _format(data)
        else:
            result = None
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            "SELECT count(1) as cnt from tg_announce where user_id = %s and is_active = True", [user_id])
        row = dictfetchone(cursor)

    if row:
        count_records = row['cnt']
    else:
        count_records = 0

    paginator = SqlPaginator(request, page=page, per_page=PER_PAGE, count=count_records)
    pagging = paginator.get_paginated_response()

    return OrderedDict([
        ('item', result),
        ('meta', pagging)
    ])


def one_product(request, id):
    extra_sql = f"""
        select ann.id, fullname, phone_number, coalesce(price->>'from', '') || '-' ||coalesce(price->>'to', '') as price,
         description, geo."name"->>'uz' as region_name_uz, geo."name"->>'ru' as region_name_ru, 
         cat."name"->>'uz' as category_name_uz, cat."name"->>'ru' as category_name_ru
    from tg_announce ann
    left join geo_region geo on ann.region_id = geo.id
    left join tg_announcecategories acat on ann.id = acat.resume_id 
    left join tg_category cat on acat.category_id = cat.id 
    where ann.id = %s and ann.is_active = True
    """

    with closing(connection.cursor()) as cursor:
        cursor.execute(extra_sql, [id])
        data = dictfetchone(cursor)
        if data:
            result = _format(data)
        else:
            result = None

    return OrderedDict([
        ('item', result)
    ])


def _format_(data):
    return OrderedDict([
        ('id', data['id']),
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
        ('id', data['id']),
        ('fullname', data['fullname']),
        ('description', data['description']),
        ('price', data['price']),
        ('phone_number', data['phone_number']),
        ('region_uz', data['region_name_uz']),
        ('region_ru', data['region_name_ru']),
        ('category_uz', data['category_name_uz']),
        ('category_ru', data['category_name_ru'])

    ])
