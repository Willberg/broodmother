from elasticsearch import Elasticsearch
from elasticsearch.helpers import parallel_bulk


class Elastic:
    def __init__(self, ip='192.168.0.105'):
        self.es = Elasticsearch([ip], port=9200, http_auth=('elastic', '123456'), timeout=3600)

    # 创建索引
    def create_index(self, index_name, body=None):
        if self.es.indices.exists(index=index_name):
            return True

        if not body:
            return False

        res = self.es.indices.create(index=index_name, body=body)
        return res['acknowledged']

    # 删除索引
    def delete_index(self, index_name):
        if not self.es.indices.exists(index=index_name):
            return True
        res = self.es.indices.delete(index=index_name)
        return res['acknowledged']

    # 删除数据
    def delete_index_data(self, index_name, data_id):
        if not self.es.exists(index=index_name, id=data_id):
            return True
        res = self.es.delete(index=index_name, id=data_id)
        if res['result'] == 'deleted':
            return True
        return False

    # 搜索数据
    def search_index_data(self, index_name, body):
        _searched_data = self.es.search(index=index_name, body=body)

        ret = []
        for hit in _searched_data['hits']['hits']:
            ret.append(hit['_source'])
        return ret

    # 批量插入数据
    def bulk_index_data(self, index_name, data_list):
        actions = []
        for data in data_list:
            action = {
                '_index': index_name,
                '_source': data
            }
            actions.append(action)

        return parallel_bulk(self.es, actions=actions)

    # 解析词
    def analyze_token(self, text, analyzer='ik_smart'):
        body = {
            "analyzer": analyzer,
            "text": text
        }
        return self.es.indices.analyze(body)


if __name__ == '__main__':
    es = Elastic()

    un_analyze_word = '我是中国人，在中央人民政府工作'
    print(es.analyze_token(un_analyze_word))

    index_body = {
        "settings": {
            "index.analysis.analyzer.default.type": "ik_smart"
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

    # 删除索引
    res = es.delete_index('rtz')
    print(res)

    res = es.create_index('rtz', body=index_body)
    print(res)

    insert_data_list = [
        {
            "title": "我是中国人，在中央人民政府工作",
            "tags": "中国，中央人民，工作",
            "family": "测试",
            "doc_id": "5e4e3bc91867a5e184d32a76",
            "marks": 1
        },
        {
            "title": "随便一些字",
            "tags": "字",
            "family": "测试",
            "doc_id": "5e4e3bd21867a5e184d32a7a",
            "marks": 2
        },
        {
            "title": "搞事情",
            "tags": "事情",
            "family": "测试",
            "doc_id": "5e4e3bd21867a5e184d32a7a",
            "marks": 3
        },
    ]
    data_corporation = es.bulk_index_data('rtz', insert_data_list)
    for data in data_corporation:
        print(data)

    search_data = {
        "query": {
            "term": {
                "family": "测试"
            }
        },
        "sort": {
            "marks": "desc"
        },
    }
    res = es.search_index_data('rtz', search_data)
    print(res)

    # res = es.delete_index_data('rtz', 'LUYwcnAB4gNzbB9u8kqT')
    # print(res)
