from functools import reduce
from operator import or_
from typing import Final

from django.db import models
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.serializers import ModelSerializer

from django.db.models import Model, QuerySet, Q

from .validation import validate_query_data


QUERY_IDS_PARAM: Final = 'ids'


class ManyToManyApiView(APIView):
    changeable_model: Model
    serializer: ModelSerializer
    many_to_many_field: str
    main_id_query_name: str = 'main_id'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.query_data = None
        self.relationship_object_class = None
        self.many_to_many_relationship = None
        self.changeable_model_object = None

    def __serialize(self, data):
        if isinstance(data, QuerySet):
            return self.__class__.serializer(data, many=True)
        return self.__class__.serializer(data, many=False)

    def __get_data(self):
        all_fields = self.relationship_object_class._meta.get_fields()
        search_fields = [f.name for f in all_fields if isinstance(
            f, (models.CharField, models.IntegerField, models.IntegerField))
        ]
        filter_condition = reduce(or_, [Q(**{'{}__contains'.format(f): self.request.GET['search']}) for f in search_fields], Q())
        return self.many_to_many_relationship.filter(filter_condition)

    def __get_changeable_model(self, main_id):
        return self.__class__.changeable_model.objects.get(pk=main_id)

    def __get_many_to_many_relationship(self, changeable_model_object):
        return getattr(changeable_model_object, self.__class__.many_to_many_field)

    def get(self, request, main_id):
        data = self.__get_data()

        serialized_data = self.__serialize(data)
        result = dict(
            count=len(serialized_data.data),
            results=serialized_data.data
        )
        return Response(data=result, status=status.HTTP_200_OK)

    def post(self, request, main_id):
        self.query_data = validate_query_data(self.query_data)
        for id in self.query_data:
            self.many_to_many_relationship.add(self.relationship_object_class.objects.get(pk=id))
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, main_id):
        self.query_data = validate_query_data(self.query_data)
        for id in self.query_data:
            self.many_to_many_relationship.remove(self.relationship_object_class.objects.get(pk=id))
        return Response(status=status.HTTP_204_NO_CONTENT)

    def dispatch(self, request, *args, **kwargs):
        if QUERY_IDS_PARAM in request.GET:
             self.query_data = request.GET[QUERY_IDS_PARAM]
        self.changeable_model_object = self.__get_changeable_model(kwargs[self.__class__.main_id_query_name])
        self.many_to_many_relationship = self.__get_many_to_many_relationship(self.changeable_model_object)
        self.relationship_object_class = self.many_to_many_relationship.model
        return super().dispatch(request, *args, **kwargs)



