from django.http import Http404

from rest_framework import exceptions
from rest_framework.permissions import AllowAny
from rest_framework.renderers import CoreJSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework_swagger import renderers

from autoapi.generators import SchemaGenerator
from autoapi.utils import get_model


class AutoModelSerializer(object):

    @property
    def model(self):
        if not hasattr(self, '_model'):
            app_name = self.kwargs.get('app_name')
            model_name = self.kwargs.get('model_name')
            model = get_model(app_name, model_name)
            if not model:
                raise Http404
            self._model = model
        return self._model

    def get_serializer_class(self, *args, **kwargs):
        meta_attrs = {
            'model': self.model,
            'fields': '__all__'
        }
        meta = type('Meta', (), meta_attrs)
        class_name = self.model.__name__ + 'Serializer'
        attrs = {
            'Meta': meta
        }
        serializer_class = type(ModelSerializer)(
            class_name, (ModelSerializer, ), attrs)
        return serializer_class

    def get_queryset(self):
        return self.model._default_manager.all()


class ListCreateAutoView(AutoModelSerializer, ListCreateAPIView):

    pass


class RetrieveUpdateDestroyAutoView(
        AutoModelSerializer, RetrieveUpdateDestroyAPIView):

    pass


def get_swagger_view(title=None, url=None, patterns=None, urlconf=None):
    """
    Returns schema view which renders Swagger/OpenAPI.
    """
    class SwaggerSchemaView(APIView):
        _ignore_model_permissions = True
        exclude_from_schema = True
        permission_classes = [AllowAny]
        renderer_classes = [
            CoreJSONRenderer,
            renderers.OpenAPIRenderer,
            renderers.SwaggerUIRenderer
        ]

        def get(self, request):
            generator = SchemaGenerator(
                title=title,
                url=url,
                patterns=patterns,
                urlconf=urlconf
            )
            schema = generator.get_schema(request=request)

            if not schema:
                raise exceptions.ValidationError(
                    'The schema generator did not return a schema Document'
                )

            return Response(schema)

    return SwaggerSchemaView.as_view()
