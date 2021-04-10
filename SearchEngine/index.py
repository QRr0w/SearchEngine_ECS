import elasticsearch
from elasticsearch import Elasticsearch
import numpy as np


def insert_data_to_es():
    es = Elasticsearch()
    path = 'dataset\\test.ft.txt'
    index_name = "version2.0"
    setting = {
        "settings": {
            "analysis": {
                "filter": {
                    "english_stop": {
                        "type": "stop",
                        "stopwords": "_english_"
                    },
                    "english_keywords": {
                        "type": "keyword_marker",
                        "keywords": ["example"]
                    },
                    "english_stemmer": {
                        "type": "stemmer",
                        "language": "english"
                    },
                    "english_possessive_stemmer": {
                        "type": "stemmer",
                        "language": "possessive_english"
                    }
                },
                "analyzer": {
                    "english": {
                        "tokenizer": "standard",
                        "filter": [
                            "english_possessive_stemmer",
                            "lowercase",
                            "english_stop",
                            "english_keywords",
                            "english_stemmer"
                        ]
                    }
                }
            }
        }
    }
    mapping = {
        "properties": {
            "comments": {
                "type": "text",
                "analyzer": "english",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            },
            "id": {
                "type": "long"
            },
            "rating": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            },
            "title": {
                "type": "text",
                "analyzer": "english",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            }
        }
    }
    dataset = load_data(path)
    try:
        es.indices.create(index=index_name,
                          body=setting)
        es.indices.put_mapping(body=mapping, index=index_name)

        for index in range(len(dataset[0])):
            es.index(index=index_name,
                     body={
                         'id': index,
                         'title': dataset[1][index],
                         'rating': dataset[0][index],
                         'comments': dataset[2][index]
                     })
    except:
        print("Error: unable to fetch data")


def load_data(path):
    # dataset = np.loadtxt(path, encoding='utf-8', dtype=str)
    # return dataset
    with open(path, "r", encoding='utf-8') as f:
        data = f.readlines()
        label_list = []
        title_list = []
        txt_list = []
        for index in range(len(data)):
            label_list.append(data[index][:10])
            title = data[index][11:-1].split(":")[0]
            title_list.append(title)
            txt_list.append(data[index][11:-1].replace(title + ': ', ""))

    return np.array([label_list, title_list, txt_list])

def rating_convert(str):
    if str=="__label__1":
        return "Great Comments!"
    else:
        return "Bad Comments!"

if __name__ == '__main__':
    insert_data_to_es()

    # dataset = load_data(path)
    # print(dataset)
