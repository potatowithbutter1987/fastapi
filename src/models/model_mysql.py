from logger import log_settings
from sqlalchemy.sql import text
from drivers.mysql import session, Base, ENGINE
import math
import logging
import sys
sys.path.append('../')
logger = logging.getLogger(__name__)


# 車両一覧取得
def get_vehicle_list(**kwargs):
    limit = kwargs.get('limit')
    offset = kwargs.get('offset')
    binds = {'limit': limit, 'offset': offset}
    vehicle_list = []
    result = {'search_result': [], 'paging': 0, 'total_search_count': 0}

    logger.info("start get_vehicle_list")

    try:
        vehicle_list = get_search_result(binds, **kwargs)

        if has_not_data(vehicle_list):
            return []

        result['search_result'] = vehicle_list
        result['total_search_count'] = get_total_search_count(binds, **kwargs)
        result['paging'] = get_paging(limit, result['total_search_count'])

    except Exception as e:
        raise e

    logger.info("end get_vehicle_list")

    return result


# 強行距離別 廃車買取取得 グラフ取得
def get_vehicle_graph(**kwargs):
    binds = {}
    result = {'search_result': []}
    logger.info("start get_vehicle_graph")

    try:
        graph_result = get_graph_result(binds, **kwargs)
    except Exception as e:
        raise e

    result['search_result'] = graph_result

    logger.info("end get_vehicle_graph")

    return result


# 車両一覧 検索結果取得
def get_search_result(binds, **kwargs):
    vehicle_list = []

    query_where = create_query_where(binds, **kwargs)

    search_query = text('SELECT * FROM vehicle_list ' +
                        query_where +
                        'LIMIT :limit OFFSET :offset')

    for row in session.execute(search_query, binds):
        vehicle_list.append(row)

    return vehicle_list


def get_graph_result(binds, **kwargs):
    graph_data = []

    query_select_price = "IFNULL(FORMAT(avg((price / (mileage / 10000))) / 1000, 1), 0) as 'price'"
    query_where = create_query_where_for_graph(binds, **kwargs)

    search_query = text(
        "SELECT '32' as 'mileage',  " + query_select_price +
        "FROM vehicle_list" + query_where + " 280000 <= mileage\
            UNION\
        SELECT '28' as 'mileage',  " + query_select_price +
        "FROM vehicle_list" + query_where + " 280000 > mileage AND 240000 <= mileage\
            UNION\
        SELECT '24' as 'mileage',  " + query_select_price +
        "FROM vehicle_list" + query_where + " 240000 > mileage AND 200000 <= mileage\
            UNION\
        SELECT '20' as 'mileage',  " + query_select_price +
        "FROM vehicle_list" + query_where + " 200000 > mileage AND 160000 <= mileage\
            UNION\
        SELECT '16' as 'mileage',  " + query_select_price +
        "FROM vehicle_list" + query_where + " 160000 > mileage AND 120000 <= mileage\
            UNION\
        SELECT '12' as 'mileage',  " + query_select_price +
        "FROM vehicle_list" + query_where + " 120000 > mileage AND 80000 <= mileage\
            UNION\
        SELECT '8' as 'mileage', " + query_select_price +
        "FROM vehicle_list" + query_where + " 80000 > mileage AND 40000 <= mileage\
            UNION\
        SELECT '4' as 'mileage',  " + query_select_price +
        "FROM vehicle_list" + query_where + " 40000 > mileage")

    for row in session.execute(search_query, binds):
        graph_data.append(row)

    return graph_data


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


def create_query_where_for_graph(binds, **kwargs):
    query_where = ""

    for key, value in kwargs.items():
        if has_kwarg(kwargs.get(key)):
            if not query_where == "":
                query_where += 'and '
                query_where += key + ' = :' + key + ' '
            else:
                query_where += key + ' = :' + key + ' '
            binds.update({key: kwargs.get(key)})

    if not query_where == "":
        query_where = ' WHERE ' + query_where + ' AND '
    else:
        query_where = ' WHERE '

    return query_where


def has_not_data(array):
    return len(array) == 0


def has_kwarg(data):
    return data is not None


def main():
    Base.metadata.create_all(bind=ENGINE)


if __name__ == "__main__":
    main()
