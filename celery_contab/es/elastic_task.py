import time

from celery_contab.celery import cel
from celery_contab.es.utils.elastic import Elastic
from celery_contab.es.utils.rtz_db import DbCorporation


def create_index_struct(es):
    index_body = {
        "settings": {
            "index.analysis.analyzer.default.type": "ik_smart",
            "number_of_replicas": "0"  # 在本地没有备份
        },
        "mappings": {
            "properties": {
                "title": {
                    "type": "text",
                    "analyzer": "ik_smart",
                    "search_analyzer": "ik_smart",
                    "fields": {
                        "raw": {
                            "type": "keyword"
                        }
                    }
                },
                "family": {
                    "type": "text",
                    "analyzer": "ik_smart",
                    "search_analyzer": "ik_smart",
                    "fields": {
                        "raw": {
                            "type": "keyword"
                        }
                    }
                },
                "tags": {
                    "type": "text",
                    "analyzer": "ik_smart",
                    "search_analyzer": "ik_smart",
                    "fields": {
                        "raw": {
                            "type": "keyword"
                        }
                    }
                },
                "doc_id": {
                    "type": "keyword",
                    "index": False
                },
                "marks": {
                    "type": "integer",
                    "index": False
                }
            }
        }
    }
    es.create_index('rtz', index_body)


def get_data_from_db(db, i):
    return db.get_data_from_db('select * from fs_rtz order by id limit %s,%s' % (i * 100, 100))


def get_data_counts_from_db(db, table_name):
    return db.get_num_from_db(table_name)


def insert_data_to_es(es, data_list):
    insert_data_list = []
    for data in data_list:
        insert_data_list.append(
            {
                "title": data[2],
                "tags": data[5],
                "family": data[3],
                "doc_id": data[1],
                "marks": data[8]
            }
        )
    es.bulk_index_data('rtz', insert_data_list)


@cel.task
def create_index():
    start_time = int(time.time())
    es = Elastic()
    # 删除索引
    res = es.delete_index('rtz')
    print(res)

    # 创建索引
    create_index_struct(es)

    db = DbCorporation()
    num = get_data_counts_from_db(db, 'fs_rtz')[0]
    max_val = int(num / 100)
    if max_val * 100 < num:
        max_val += 1

    for i in range(max_val):
        print('进度： %.4f \n' % float(i / max_val) * 100)
        data_list = get_data_from_db(db, i)
        insert_data_to_es(es, data_list)

    print('耗时： %.2f' % ((int(time.time()) - start_time) / 60.0))


if __name__ == '__main__':
    create_index()
