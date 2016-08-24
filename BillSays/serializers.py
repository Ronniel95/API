from rest_framework.serializers import ModelSerializer
from BillSays.models import Person


class PersonSerializer(ModelSerializer):

    class Meta:
        model = Person
