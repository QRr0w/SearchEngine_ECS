# Introduction

Search engine design and implement by Group C

# How to use

First generate index by index.py

Skip if already has index

```python
# Build ElasticSearch index
# Must running ElasticSearch before!!!!
insert_data_to_es()
```

Start flask service in app.py

```python
host = "127.0.0.1"
port = 5000
app.run(host=host,port=port,debug=True)
```

Enter homepage

Eg: http://127.0.0.1:5000/

# Needs to do

- [ ] BM25
- [ ] Relevance analysis (needs generate labels first)