from flask import Flask, render_template, request
from search import elasticSearch
import jsonify
import json
from params import host_address, port, index_type
from params import index_name_default,index_name_f1,index_name_f2


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('search.html')

@app.route("/search", methods=['GET', 'POST'])
def get_es():
    if request.method == "POST":
        func_query = "1"# default index
        if "index_func" in request.form:
            func_query = request.form['index_func']
        comments_query = request.form['keyword']
        rating_query = request.form['rating']
        title_query = request.form['only_title']
        index_name = convert_to_index(func_query)

        es = elasticSearch(index_name=index_name,
                           index_type=index_type)
        data = es.search(comments_query, rating_query, title_query)
        result_data = data['hits']['hits']
        result_list = []
        for item in result_data:
            result_list.append(item["_source"])
        address_len = len(result_list)
        return render_template('search_result.html',
                               search_result=result_list,
                               search_nums=address_len,
                               keyword=comments_query,
                               rating_choice=rating_query,
                               only_title=title_query)
    return render_template('search.html')

def convert_to_index(num):
    if num == "2":
        return index_name_f1 # Modified index 1
    elif num == "3":
        return index_name_f2 # Modified index 2
    else:
        return index_name_default # Default index

if __name__ == '__main__':
    app.run(host=host_address,
            port=port,
            debug=True)
