from logger import log_settings
from sqlalchemy.sql import text
from drivers.mysql import session, Base, ENGINE
import math
import logging
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

        result['search_result'].append(vehicle_list)
        result['total_search_count'] = get_total_search_count(binds, **kwargs)
        result['paging'] = get_paging(limit, result['total_search_count'])

    except Exception as e:
        raise e

    logger.info("end get_vehicle_list")

    return result


# 強行距離別 廃車買取取得 グラフ取得
def get_vehicle_graph(car_id):
    result = []
    binds = {'car_id': car_id}
    logger.info("start get_vehicle_graph")

    try:
        graph_result = get_graph_result(binds)
    except Exception as e:
        raise e

    logger.info("end get_vehicle_graph")

    return graph_result


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


def get_graph_result(binds):
    graph_data = []

    # グラフ用データ(走行距離別、1万km単位で集計、平均値)
    # 走行距離別の廃車買取価格グラフ
    # 	距離：1万キロ単位で、割ってグループバイ
    # 		平均値を計算して返す。

    search_query = text(
        'SELECT price,mileage  FROM vehicle_list WHERE car_id = :car_id')

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


def has_not_data(array):
    return len(array) == 0


def has_kwarg(data):
    return data is not None


def main():
    Base.metadata.create_all(bind=ENGINE)


if __name__ == "__main__":
    main()
