from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.serializers import ModelSerializer

from django.db.models import Model, QuerySet


class ManyToManyApiView(APIView):
    changeable_model: Model
    serializer: ModelSerializer
    many_to_many_field: str
    main_id_query_name: str = 'main_id'
    optional_id_query_name: str = 'optional_id'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.relationship_object_class = None
        self.many_to_many_relationship = None
        self.changeable_model_object = None

    def __serialize(self, data):
        if isinstance(data, QuerySet):
            return self.__class__.serializer(data, many=True)
        return self.__class__.serializer(data, many=False)

    def __get_data(self, main_id, optional_id):
        if optional_id:
            data = self.many_to_many_relationship.get(pk=optional_id)
        else:
            data = self.many_to_many_relationship.all()
        return data

    def __get_changeable_model(self, main_id):
        return self.__class__.changeable_model.objects.get(pk=main_id)

    def __get_many_to_many_relationship(self, changeable_model_object):
        return getattr(changeable_model_object, self.__class__.many_to_many_field)

    def get(self, request, main_id, optional_id=None):
        data = self.__get_data(main_id, optional_id)
        serialized_data = self.__serialize(data)

        return Response(data=serialized_data.data, status=status.HTTP_200_OK)

    def post(self, request, main_id, optional_id):
        self.many_to_many_relationship.add(self.relationship_object_class.objects.get(pk=optional_id))
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, main_id, optional_id):
        self.many_to_many_relationship.remove(self.relationship_object_class.objects.get(pk=optional_id))
        return Response(status=status.HTTP_204_NO_CONTENT)

    def dispatch(self, request, *args, **kwargs):
        self.changeable_model_object = self.__get_changeable_model(kwargs[self.__class__.main_id_query_name])
        self.many_to_many_relationship = getattr(self.changeable_model_object, self.__class__.many_to_many_field)
        self.relationship_object_class = self.many_to_many_relationship.model
        return super().dispatch(request, *args, **kwargs)


