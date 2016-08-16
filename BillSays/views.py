from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from BillSays.serializers import AchievementSerializer, CheckelementSerializer, ChecksSerializer, DebtelementSerializer, DictachievementSerializer, DjangoMigrationsSerializer, FriendSerializer, UsercheckelementSerializer, UsersSerializer
from BillSays.models import Achievement, Checkelement, Checks, Debtelement, Dictachievement, DjangoMigrations, Friend, Usercheckelement, Users


class AchievementAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = Achievement.objects.get(pk=id)
            serializer = AchievementSerializer(item)
            return Response(serializer.data)
        except Achievement.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = Achievement.objects.get(pk=id)
        except Achievement.DoesNotExist:
            return Response(status=404)
        serializer = AchievementSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = Achievement.objects.get(pk=id)
        except Achievement.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class AchievementAPIListView(APIView):

    def get(self, request, format=None):
        items = Achievement.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = AchievementSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = AchievementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class CheckelementAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = Checkelement.objects.get(pk=id)
            serializer = CheckelementSerializer(item)
            return Response(serializer.data)
        except Checkelement.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = Checkelement.objects.get(pk=id)
        except Checkelement.DoesNotExist:
            return Response(status=404)
        serializer = CheckelementSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = Checkelement.objects.get(pk=id)
        except Checkelement.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class CheckelementAPIListView(APIView):

    def get(self, request, format=None):
        items = Checkelement.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = CheckelementSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = CheckelementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ChecksAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = Checks.objects.get(pk=id)
            serializer = ChecksSerializer(item)
            return Response(serializer.data)
        except Checks.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = Checks.objects.get(pk=id)
        except Checks.DoesNotExist:
            return Response(status=404)
        serializer = ChecksSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = Checks.objects.get(pk=id)
        except Checks.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class ChecksAPIListView(APIView):

    def get(self, request, format=None):
        items = Checks.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = ChecksSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = ChecksSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class DebtelementAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = Debtelement.objects.get(pk=id)
            serializer = DebtelementSerializer(item)
            return Response(serializer.data)
        except Debtelement.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = Debtelement.objects.get(pk=id)
        except Debtelement.DoesNotExist:
            return Response(status=404)
        serializer = DebtelementSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = Debtelement.objects.get(pk=id)
        except Debtelement.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class DebtelementAPIListView(APIView):

    def get(self, request, format=None):
        items = Debtelement.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = DebtelementSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = DebtelementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class DictachievementAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = Dictachievement.objects.get(pk=id)
            serializer = DictachievementSerializer(item)
            return Response(serializer.data)
        except Dictachievement.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = Dictachievement.objects.get(pk=id)
        except Dictachievement.DoesNotExist:
            return Response(status=404)
        serializer = DictachievementSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = Dictachievement.objects.get(pk=id)
        except Dictachievement.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class DictachievementAPIListView(APIView):

    def get(self, request, format=None):
        items = Dictachievement.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = DictachievementSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = DictachievementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)




class DjangoMigrationsAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = DjangoMigrations.objects.get(pk=id)
            serializer = DjangoMigrationsSerializer(item)
            return Response(serializer.data)
        except DjangoMigrations.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = DjangoMigrations.objects.get(pk=id)
        except DjangoMigrations.DoesNotExist:
            return Response(status=404)
        serializer = DjangoMigrationsSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = DjangoMigrations.objects.get(pk=id)
        except DjangoMigrations.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class DjangoMigrationsAPIListView(APIView):

    def get(self, request, format=None):
        items = DjangoMigrations.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = DjangoMigrationsSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = DjangoMigrationsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class FriendAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = Friend.objects.get(pk=id)
            serializer = FriendSerializer(item)
            return Response(serializer.data)
        except Friend.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = Friend.objects.get(pk=id)
        except Friend.DoesNotExist:
            return Response(status=404)
        serializer = FriendSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = Friend.objects.get(pk=id)
        except Friend.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class FriendAPIListView(APIView):

    def get(self, request, format=None):
        items = Friend.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = FriendSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = FriendSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class UsercheckelementAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = Usercheckelement.objects.get(pk=id)
            serializer = UsercheckelementSerializer(item)
            return Response(serializer.data)
        except Usercheckelement.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = Usercheckelement.objects.get(pk=id)
        except Usercheckelement.DoesNotExist:
            return Response(status=404)
        serializer = UsercheckelementSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = Usercheckelement.objects.get(pk=id)
        except Usercheckelement.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class UsercheckelementAPIListView(APIView):

    def get(self, request, format=None):
        items = Usercheckelement.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = UsercheckelementSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = UsercheckelementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class UsersAPIView(APIView):

    def get(self, request, id, format=None):
        try:
            item = Users.objects.get(pk=id)
            serializer = UsersSerializer(item)
            return Response(serializer.data)
        except Users.DoesNotExist:
            return Response(status=404)

    def put(self, request, id, format=None):
        try:
            item = Users.objects.get(pk=id)
        except Users.DoesNotExist:
            return Response(status=404)
        serializer = UsersSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        try:
            item = Users.objects.get(pk=id)
        except Users.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204)


class UsersAPIListView(APIView):

    def get(self, request, format=None):
        items = Users.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(items, request)
        serializer = UsersSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import response, schemas

@api_view()
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='Pastebin API')
    return response.Response(generator.get_schema(request=request))

