from flask import Flask
from search import elasticSearch
import jsonify
import json

app = Flask(__name__)
index_name = "version2.0"
index_type = "_doc"

@app.route('/')
def index():
    return 'Hello World, this is my first flask web app!'

@app.route("/getEs/<query>")
def get_es(query):
    es = elasticSearch(index_name=index_name,
                       index_type=index_type)
    data = es.search(query)
    address_data = data['hits']['hits']
    address_list = []
    for item in address_data:
        address_list.append(item["_source"])
    new_data = json.dumps(address_list)
    return app.response_class(new_data, content_type='application/json')

if __name__ == '__main__':
    app.run(host='127.0.0.1',
            port=5000,
            debug=True)
