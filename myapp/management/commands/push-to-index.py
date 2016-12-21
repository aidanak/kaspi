# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from myapp.models import venues
from elasticsearch.client import IndicesClient
from django.conf import settings
from myapp.es_mappings import model_es_indices, es_mappings
from elasticsearch.helpers import bulk
from django.contrib.gis import geos
import json

class Command(BaseCommand):
    es_index_name = 'restaurant'
    es_ind_settings = {
        "settings": {
            "analysis": {
                "analyzer": {
                    "my_analyzer": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": ["lowercase", "my_stopwords", "standard"]
                    }
                },
                "filter": {
                    "my_stopwords": {
                        "type": "stop",
                        "stopwords": "кафе,ресторан,гастобар,бар"
                    }
                }
            }
        }
    }


    def handle(self, *args, **options):
        self.recreate_index()
        self.push_db_to_index()

    def push_db_to_index(self):
        data = [
            self.convert_for_bulk(s, 'create') for s in venues.objects.all()[:1000]
            ]
        bulk(client=settings.ES_CLIENT, actions=data, stats_only=True)

    def convert_for_bulk(self, django_object, action=None):
        data = django_object.es_repr()
        metadata = {
            '_op_type': action,
            "_index": model_es_indices[django_object.__class__.__name__]['index_name'],
            "_type": model_es_indices[django_object.__class__.__name__]['type'],
        }
        data.update(**metadata)
        return data

    def recreate_index(self):
        indices_client = IndicesClient(client=settings.ES_CLIENT)
        index_name = self.es_index_name
        if indices_client.exists(index_name):
            indices_client.delete(index=index_name)
        indices_client.create(index=index_name, body = self.es_ind_settings)

        ## create mapping for one model only for now
        model_name = 'venues'
        indices_client.put_mapping(
            doc_type=model_es_indices[model_name]['type'],
            body=es_mappings[model_name],
            index=index_name
        )
