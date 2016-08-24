from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import response, schemas

from BillSays.models import Person
from BillSays.serializers import PersonSerializer


@api_view()
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='Bill Says API')
    return response.Response(generator.get_schema(request=request))


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class PersonAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = Person.objects.get(pk=id)
            serializer = PersonSerializer(item)
            return Response(serializer.data)
        except Person.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = Person.objects.get(pk=id)
        except Person.DoesNotExist:
            return Response(status=404)
        serializer = PersonSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = Person.objects.get(pk=id)
        except Person.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class PersonAPIListView(APIView):

    def get(self, request, format=None):
        items = Person.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = PersonSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)