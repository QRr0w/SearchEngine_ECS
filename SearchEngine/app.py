from flask import Flask, render_template, request
from search import elasticSearch
import jsonify
import json

app = Flask(__name__)
index_name = "version2.0"
index_type = "_doc"

@app.route('/')
def index():
    return render_template('search.html')

@app.route("/search", methods=['GET', 'POST'])
def get_es():
    if request.method == "POST":
        es = elasticSearch(index_name=index_name,
                           index_type=index_type)
        query = request.form['keyword']
        data = es.search(query)
        result_data = data['hits']['hits']
        result_list = []
        for item in result_data:
            result_list.append(item["_source"])
        address_len = len(result_list)
        return render_template('search_result.html',
                               search_result=result_list,
                               search_nums=address_len,
                               keyword=query)
    return render_template('search.html')

        # new_data = json.dumps(result_list)
        # return app.response_class(new_data, content_type='application/json')

if __name__ == '__main__':
    app.run(host='127.0.0.1',
            port=5000,
            debug=True)
