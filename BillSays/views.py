from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from rest_framework.viewsets import ModelViewSet
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import response, schemas

from BillSays.models import  Check
from BillSays.serializers import CheckSerializer


@api_view()
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='Bill Says API')
    return response.Response(generator.get_schema(request=request))


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class CheckViewSet(ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Check.objects.all()
    serializer_class = CheckSerializer
