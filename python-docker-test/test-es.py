#!/usr/bin/python

from elasticsearch import Elasticsearch
import requests
import json


es = Elasticsearch([{'host': 'ec2-35-180-158-38.eu-west-3.compute.amazonaws.com', 'port': 9200}])
req = requests.get('http://ec2-35-180-158-38.eu-west-3.compute.amazonaws.com:9200')

i = 1

while req.status_code == 200:
    r = requests.get('http://swapi.co/api/people/' + str(i))
    es.index(index='sw', doc_type='people', id=i, body=json.loads(r.content))
    i=i+1
