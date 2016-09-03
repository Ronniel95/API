import random


from django.contrib.auth.models import User
from django.db.models import Q
from django.http import Http404

from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import response, schemas
from rest_framework import filters
from rest_framework import viewsets

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.vk.views import VKOAuth2Adapter

from rest_auth.registration.views import SocialLoginView

from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer

from BillSays.models import Friend, Check, Mention, Location, Waitress, CheckElement, UserCheckElement
from BillSays.serializers import FriendSerializer, CheckSerializer, MentionSerializer, RecognizedCheckSerializer, \
    UserCheckElementSerializer, UserSerializerPublic, UserDetailsSerializerNew


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


class CheckViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Check.objects.all()
    serializer_class = CheckSerializer
    permission_classes = (IsAuthenticated,)
    def create(self, request, *args, **kwargs):
        serializer = CheckSerializer(data=request.data)
        if serializer.is_valid():
            test = serializer.save()
            self.generate_check(test)
            self.generate_dishes(test)
            return Response(RecognizedCheckSerializer(instance=test).data)
        else:
            return Response(serializer.errors, status=400)

    def generate_check(self, check):
        check.total_cost = random.randrange(1000)

        id_location = 0
        id_waitress = 0

        restaurant_name = 'restaurant_' + str(random.randrange(5))
        waitress_name = 'waitress_' + str(random.randrange(5))

        if Location.objects.filter(name=restaurant_name).count() == 0:
            location = Location(name=restaurant_name)
            location.save()
            id_location = location
        else:
            id_location = Location.objects.get(name=restaurant_name)

        if Waitress.objects.filter(name=waitress_name, fk_location=id_location).count() == 0:
            waitress = Waitress(name=waitress_name, fk_location=id_location)
            waitress.save()
            id_waitress = waitress
        else:
            id_waitress = Waitress.objects.get(name=waitress_name, fk_location=id_location)

        check.fk_waitress = id_waitress
        check.save()

    def generate_dishes(self, check):
        for i in range(1, 6):
            CheckElement.objects.create(fk_check=check,
                                        name='dish' + str(random.randrange(100)),
                                        cost=random.randrange(1000),
                                        quantity=random.randrange(10)
                                        )


class MentionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Mention.objects.all()
    serializer_class = MentionSerializer

    def create(self, request, *args, **kwargs):
        serializer = MentionSerializer(data=request.data)
        if serializer.is_valid():

            if (Check.objects.filter(id=serializer.validated_data['id']).count() == 0):
                return Response("Given check doesnt exist", status=400)
            test = serializer.save()

            return Response(test.id)
        else:
            return Response(serializer.errors, status=400)


class BookViewSet(viewsets.mixins.CreateModelMixin, viewsets.mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    ViewSet create and list books

    Usage single : POST
    {
        "name":"Killing Floor: A Jack Reacher Novel",
        "author":"Lee Child"
    }

    Usage array : POST
    [{
        "name":"Mr. Mercedes: A Novel (The Bill Hodges Trilogy)",
        "author":"Stephen King"
    },{
        "name":"Killing Floor: A Jack Reacher Novel",
        "author":"Lee Child"
    }]
    """
    queryset = UserCheckElement.objects.all()
    serializer_class = UserCheckElementSerializer


    def create(self, request, *args, **kwargs):
        """
        #checks if post request data is an array initializes serializer with many=True
        else executes default CreateModelMixin.create function
        """
        is_many = isinstance(request.data, list)
        if not is_many:
            return super(BookViewSet, self).create(request, *args, **kwargs)
        else:
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=201, headers=headers)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed
    """
    queryset = User.objects.all()
    serializer_class = UserSerializerPublic

    def get_queryset(self):
        return super(UserViewSet, self).get_queryset().filter(Q(username__contains=self.kwargs['name'])|
                                                              Q(email__contains=self.kwargs['name']))


