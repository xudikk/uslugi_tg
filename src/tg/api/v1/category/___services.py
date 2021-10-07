# -*- coding: utf-8 -*-
import json
from contextlib import closing
from collections import OrderedDict
from django.db import connection
from django.conf import settings

from base.utils.db import dictfetchall, dictfetchone
from base.utils.sqlpaginator import SqlPaginator

PER_PAGE = settings.PAGINATE_BY


def get_list_category(request, parent=None):
    try:
        page = int(request.query_params.get('page', 1))
    except:
        page = 1

    if "main" in request.query_params:
        try:
            filter_query = "where parent_id is null and is_active is true"
        except:
            filter_query = "where is_active is true"
    else:
        filter_query = "where is_active is true"
    print(filter_query)
    count_records = _count_list_category(filter_query)

    rows = _get_all_category(page, filter_query)
    nodes = {}
    for data in rows:
        nodes[data['id']] = _format_one(data)

    result = []
    if parent:
        for data in rows:
            result.append(nodes[data['id']])

    else:
        for data in rows:
            id = data['id']
            parent_id = data['parent_id']
            node = nodes[id]
            if parent_id is None:
                result.append(node)
            else:
                if parent_id in nodes:
                    parent = nodes[parent_id]
                    children = parent['children']
                    children.append(node)
                else:
                    result.append(node)
    paginator = SqlPaginator(request, page=1, per_page=PER_PAGE, count=count_records)
    pagging = paginator.get_paginated_response()
    return OrderedDict([
        ('items', result),
        ('meta', pagging)
    ])


def _get_all_category(page, filter_query):
    extra_sql = f"""select id, name->>'uz' as name_uz, name->>'ru' as name_ru, tg_category.slug, parent_id as parent_id, sort_order,
    is_main, is_active
    from
    (
        SELECT  node.slug 
        FROM tg_category AS node,
            tg_category AS parent
        WHERE node.lft BETWEEN parent.lft AND parent.rght
        GROUP BY node.slug
    ) t
    inner join tg_category on t.slug = tg_category.slug
    {filter_query}
    ORDER BY tree_id, lft
    limit 50
            """
    with closing(connection.cursor()) as cursor:
        cursor.execute(extra_sql)
        rows = dictfetchall(cursor)
    return rows


def get_one_category(request, slug):
    category = _format_one(_get_one_category(slug))

    if category:
        child_items = []
        childs = _get_category_childs(category["id"])
        for data in childs:
            child_items.append(_format_one(data))
        category['children'] = child_items

    result = OrderedDict([
        ('item', category)
    ])
    return result


def _get_one_category(name):
    extra_sql = """
    select id, name->>'uz' as name_uz, name->>'ru' as name_ru, slug, parent_id as parent_id, sort_order,
    is_main, is_active
    from tg_category
    where (name->>'uz' = %s or name->>'ru' = %s)  and is_active is true
    """
    with closing(connection.cursor()) as cursor:
        cursor.execute(extra_sql, [name, name])
        rows = dictfetchone(cursor)
    return rows


def ctg_by_name(name, parent_id=None):
    if parent_id:
        parent = f'and parent_id={parent_id}'
    else:
        parent = 'and parent_id is null'
    with closing(connection.cursor()) as cursor:
        print("parent", parent)
        sql = """select id, parent_id, name->>'uz' as name_1, name->>'ru' as name_2 
        from tg_category 
        where (name->>'uz' = %s or name->>'ru' = %s) {parent}""".format(parent=parent)
        cursor.execute(sql, [name, name])
        category = dictfetchone(cursor)
        category = _format_one(_get_one_category(category.get("id", 0)))
        if category:
            child_items = []
            childs = _get_category_childs(id)
            for data in childs:
                child_items.append(_format_one(data))
            category['children'] = child_items

        result = OrderedDict([
            ('item', category)
        ])
        return result


def _get_category_childs(parent_id):
    extra_sql = f"""select id, name->>'uz' as name_uz, name->>'ru' as name_ru, slug, parent_id as parent_id, sort_order,is_main, is_active
FROM tg_category
where parent_id = {parent_id} and is_active is true
ORDER BY lft
LIMIT 30
        """
    with closing(connection.cursor()) as cursor:
        cursor.execute(extra_sql)
        rows = dictfetchall(cursor)
    return rows


def _count_list_category(filter_query):
    with closing(connection.cursor()) as cursor:
        cursor.execute(f"""select count(1) as cnt from tg_category {filter_query} and parent_id is null """)
        row = dictfetchone(cursor)
    if row:
        result = row['cnt']
    else:
        result = 0

    return result


def deactivate_children(parent_id, deactivate=False):
    if deactivate:
        activation = "false"
    else:
        activation = "true"

    extra_sql = f"""
    UPDATE tg_category
    SET is_active = {activation}
    where parent_id = {parent_id}
    """
    with closing(connection.cursor()) as cursor:
        cursor.execute(extra_sql, [parent_id])
    return {"result": "All child ctgs was deleted"}


def _format_one(data):
    items = OrderedDict([
        ('id', data['id']),
        ('slug', data['slug']),
        ('parent_id', data['parent_id']),
        ('name_1', data['name_uz']),
        ('name_2', data['name_ru']),
        ('is_active', data['is_active']),
        ('is_main', data['is_main']),
        ('sort_order', data['sort_order']),
        ('children', []),
    ])
    return items
