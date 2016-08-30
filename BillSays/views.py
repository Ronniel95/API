import time

import datetime
from allauth.socialaccount.providers.vk.views import VKOAuth2Adapter
from django.contrib.auth.models import User
from django.http import Http404
from rest_framework.generics import CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from rest_framework.viewsets import ModelViewSet
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import response, schemas

# from BillSays.models import  Check
# from BillSays.serializers import CheckSerializer

from BillSays.models import Friend
from BillSays.serializers import FriendSerializer


@api_view()
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='Bill Says API')
    return response.Response(generator.get_schema(request=request))


class FacebookLogin(SocialLoginView):
    # permission_classes = (IsAuthenticated,)
    adapter_class = FacebookOAuth2Adapter


class VKLogin(SocialLoginView):
    adapter_class = VKOAuth2Adapter


class FriendAPIView(APIView):
    """
    Retrieve, update or delete a snippet instance.

    """
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Friend.objects.get(pk=pk)
        except Friend.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = FriendSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = FriendSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()

        return Response()


class FriendAPIListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):


        items = Friend.objects.all()\
                              .filter(fk_user_friend=request.user)\
                              .filter(fk_user_owner=request.user)
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = FriendSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = FriendSerializer(data=request.data)

        if serializer.is_valid():
            serializer.validated_data['fk_user_owner'] = request.user

            # check if user trying add self to friends
            if serializer.data['fk_user_friend'] == serializer.data['fk_user_owner']:
                return Response("You cant add self as friend", status=400)

            # check if exist same record
            if (Friend.objects.filter(fk_user_friend=(serializer.data['fk_user_friend']),
                                      fk_user_owner=(serializer.data['fk_user_owner'])).count() != 0):
                return Response("Record already exist", status=400)

            serializer.save()

            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
