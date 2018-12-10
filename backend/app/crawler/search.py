from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch_dsl import Document, Search, Text, analyzer
from elasticsearch_dsl.connections import connections

from app.crawler import models

connections.create_connection(hosts=['elasticsearch:9200'])

my_analyzer = analyzer('my_analyzer',
                       tokenizer="standard",
                       filter=["standard", "lowercase", "stop", "snowball"],
                       )


class PageIndex(Document):
    text = Text(analyzer=my_analyzer, )

    class Index:
        name = 'page-index'


def bulk_indexing():
    PageIndex.init()
    es = Elasticsearch()
    bulk(client=es, actions=(b.indexing() for b in models.page.Page.objects.all().iterator()))


def search(text):
    s = Search().query('match', text=text)
    response = s.execute()
    return response
