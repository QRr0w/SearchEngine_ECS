from elasticsearch import Elasticsearch
import numpy as np

def insert_data_to_es():
    es = Elasticsearch()
    path = 'dataset\\test.ft.txt'
    dataset = load_data(path)
    try:
        for index in range(len(dataset[0])):
            es.index(index="version1.0",
                     doc_type="test-type",
                     body={
                         'id': index,
                         'title': dataset[1][index],
                         'rating': dataset[0][index],
                         'comments': dataset[2][index]
                     })
    except:
        print("Error: unable to fecth data")

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

if __name__ == '__main__':
    insert_data_to_es()

    # dataset = load_data(path)
    # print(dataset)

