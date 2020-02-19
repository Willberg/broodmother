import json

import requests

from celery_task.celery_tasks import app


def test_req(req_data):
    # 请求rtz接口
    headers = {
        'service': 'rtz_0001',
        'secret': 'bd3273c7a37b5ab33ed3e996d14f744d'
    }
    res = requests.put('http://127.0.0.1:10002/api/fs/v1/rtz/save', headers=headers, data=req_data).content
    if not res:
        print('error')
        return None

    res_json = json.loads(res)
    if not res_json['status']:
        print('error')
        return None

    return res_json['data']


@app.task
def insert_to_db():
    # 从rabbit取数据
    req_data = {
        'family': 'test',
        'tags': '1, 2',
        'title': '213',
        'doc_id': '1'
    }
    return test_req(req_data)
