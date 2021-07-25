from logger import log_settings
from sqlalchemy.sql import text
from drivers.mysql import session, Base, ENGINE
import math
import logging
logger = logging.getLogger(__name__)


def get_vehicle_list(**kwargs):
    limit = kwargs.get('limit')
    offset = kwargs.get('offset')
    binds = {'limit': limit, 'offset': offset}
    vehicle_list = []
    result = {'search_result': [], 'paging': 0, 'total_search_count': 0}

    try:
        vehicle_list = get_search_result(binds, **kwargs)

        if has_not_data(vehicle_list):
            return []

        result['search_result'].append(vehicle_list)
        result['total_search_count'] = get_total_search_count(binds, **kwargs)
        result['paging'] = get_paging(limit, result['total_search_count'])

    except Exception as e:
        raise e

    return result


# 車両一覧取得
def get_search_result(binds, **kwargs):
    vehicle_list = []

    query_where = create_query_where(binds, **kwargs)

    search_query = text('SELECT * FROM vehicle_list ' +
                        query_where +
                        'LIMIT :limit OFFSET :offset')

    for row in session.execute(search_query, binds):
        vehicle_list.append(row)

    return vehicle_list


# トータルカウント取得
def get_total_search_count(binds, **kwargs):
    total_search_count = 0

    query_where = create_query_where(binds, **kwargs)

    search_count_query = text(
        'SELECT count(id) as count FROM vehicle_list ' + query_where)

    for row in session.execute(search_count_query, binds):
        total_search_count = row['count']

    return total_search_count


# 全体ページ数取得
def get_paging(limit, total_count):
    return math.ceil(total_count / limit)


def create_query_where(binds, **kwargs):
    query_where = ""

    for key, value in kwargs.items():
        if key == 'limit' or key == 'offset':
            continue

        if has_kwarg(kwargs.get(key)):
            if not query_where == "":
                query_where += 'and '
                query_where += key + ' = :' + key + ' '
            else:
                query_where += key + ' = :' + key + ' '
            binds.update({key: kwargs.get(key)})

    if not query_where == "":
        query_where = 'WHERE ' + query_where

    return query_where


def has_not_data(array):
    return len(array) == 0


def has_kwarg(data):
    return data is not None


# def main():
#     Base.metadata.create_all(bind=ENGINE)


# if __name__ == "__main__":
#     main()
