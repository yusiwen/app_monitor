import hashlib
import json
import logging

from elasticsearch import Elasticsearch
from elasticsearch import NotFoundError

from app_monitor import settings


def _init_elasticsearch():
    es = Elasticsearch(
        settings.ES_HOSTS,
        http_auth=(settings.ES_USERNAME,
                   settings.ES_PASSWORD),
        use_ssl=settings.ES_USE_SSL,
        port=settings.ES_PORT)
    return es


def _genid(app_id, category):
    s = app_id + category
    return hashlib.sha1(s.encode()).hexdigest()


def get(app_id, category):
    id = _genid(app_id, category)
    # check index if it exists
    es = _init_elasticsearch()
    if not es.indices.exists(index=settings.ES_INDEX):
        return None

    try:
        # get document by _id
        doc = es.get(index=settings.ES_INDEX,
                     doc_type=settings.ES_TYPE,
                     id=id)
        return doc
    except NotFoundError:
        return None
    finally:
        es.close()


def _get_data(item):
    o = json.loads(json.dumps(item.__dict__))
    return json.dumps(o['_values'])


def add(item):
    es = _init_elasticsearch()
    try:
        result = es.index(
            index=settings.ES_INDEX,
            doc_type=settings.ES_TYPE,
            id=_genid(item['id'], item['category']),
            body=_get_data(item))
        if not result:
            logging.error('ERROR: Elasticsearch add document error')
    finally:
        es.close()


def update(item):
    es = _init_elasticsearch()
    try:
        result = es.update(
            index=settings.ES_INDEX,
            id=_genid(item['id'], item['category']),
            body='{"doc":' + _get_data(item) + '}')
        if not result:
            logging.error('ERROR: Elasticsearch update document error')
    finally:
        es.close()
