from elasticsearch import Elasticsearch
from params import ES_address

class elasticSearch():
    def __init__(self, index_type: str, index_name: str, ip="127.0.0.1"):
        self.es = Elasticsearch(ES_address)
        self.index_type = index_type
        self.index_name = index_name

    def create_index(self):
        if self.es.indices.exists(index=self.index_name) is True:
            self.es.indices.delete(index=self.index_name)
        self.es.indices.create(index=self.index_name, ignore=400)

    def delete_index(self):
        try:
            self.es.indices.delete(index=self.index_name)
        except:
            pass

    def get_doc(self, uid):
        return self.es.get(index=self.index_name, id=uid)

    def insert_one(self, doc:dict):
        self.es.index(index=self.index_name,
                      doc_type=self.index_type,
                      body=doc)
    def insert_array(self,docs:list):
        for doc in docs:
            self.es.index(index=self.index_name,
                          doc_type=self.index_type,
                          body=doc)

    def search(self, query, count:int = 30):
        dsl = {
            "query": {
                "bool": {
                    "must": [{
                        "match": {
                            "comments": query
                        }
                    }],
                    "must_not": [],
                    "should": []
                }
            },
            "from": 0,
            "size": 10,
            "sort": [],
            "aggs": {}
        }
        match_data = self.es.search(index=self.index_name,
                                    body=dsl,
                                    size=count)
        return match_data
