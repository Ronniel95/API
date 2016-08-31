from allauth.socialaccount.providers.vk.views import VKOAuth2Adapter
from django.http import Http404

from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import response, schemas
from rest_framework import filters

from BillSays.models import Friend, Check
from BillSays.serializers import FriendSerializer, CheckSerializer
from rest_framework import viewsets

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
    Retrieve, update friend instance.

    """
    permission_classes = (IsAuthenticated,)

    def get_object(self, id):
        try:
            return Friend.objects.get(id=id)
        except Friend.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        snippet = self.get_object(id)
        serializer = FriendSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        snippet = self.get_object(id)
        serializer = FriendSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class FriendAPIListView(APIView):
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('fk_user_friend', 'fk_user_owner',)

    def get(self, request, format=None):

        from itertools import chain
        items = list(chain(Friend.objects.all().filter(fk_user_friend=request.user),
                           Friend.objects.all().filter(fk_user_owner=request.user)))

        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = FriendSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = FriendSerializer(data=request.data)

        if serializer.is_valid():
            serializer.validated_data['fk_user_owner'] = request.user

            # check if user trying add self to friends
            if serializer.validated_data['fk_user_friend'] == serializer.validated_data['fk_user_owner']:
                return Response("You cant add self as friend", status=400)

            # check if exist same record
            if (Friend.objects.filter(fk_user_friend=(serializer.validated_data['fk_user_friend']),
                                      fk_user_owner=(serializer.validated_data['fk_user_owner'])).count() != 0):
                return Response("Record already exist", status=400)

            serializer.save()

            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class CheckAPIListView(APIView):
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.DjangoFilterBackend,)
    parser_classes = (FileUploadParser,)

    def get(self, request, format=None):
        from itertools import chain
        items = Check.objects.all()

        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = CheckSerializer(data=request.DATA, files=request.FILES)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = CheckSerializer(data=request.DATA, files=request.FILES)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)




class CheckViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Check.objects.all()
    serializer_class = CheckSerializer
