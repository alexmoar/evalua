from rest_framework import serializers

# Serializers define the API representation.
from authentication.models import UserInformation


class UserInformationSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="authentication:userinformation-detail")

    class Meta:
        model = UserInformation
        fields = ['url', 'identification', 'role', 'show_intro', 'biography']
