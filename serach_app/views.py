from django.shortcuts import render
from elasticsearch import Elasticsearch
# Create your views here.
def score_view(request): #urls에 만들었던 함수
    return render(request,'throw.html')


def search_result(request):
    es = Elasticsearch()
        # 검색어
    search_word = request.GET.get('search_text')
    docs = es.search(index='npr',
                     doc_type='np_data',
                     body={
                         "query": {
                             "multi_match": {
                                 "query": search_word,
                                 "fields": ["title", "article_body"]
                             }
                         }
                     })
    data_list =""
    for i in docs['hits']['hits']:
        res = ",".join(("{}={}".format(*j) for j in i['_source'].items()))
        data_list=data_list+str(i['_score'])+" "+res+"\n"
    return render(request,'catch.html',{'data_list':data_list,'gil':len(search_word)})
