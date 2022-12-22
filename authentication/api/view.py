# ViewSets define the view behavior.
from rest_framework import viewsets, status
from rest_framework.response import Response

from authentication.api.serializers import UserInformationSerializer
from authentication.models import User, UserInformation


class UserInformationViewSet(viewsets.ModelViewSet):
    queryset = UserInformation.objects.all()
    serializer_class = UserInformationSerializer

    def update(self, request, *args, **kwargs):
        user = UserInformation.objects.filter(id=kwargs['pk'], user=request.user).first()
        if user:
            data = request.data
            print(data['show_intro'])
            if data['show_intro'] is not None and user.show_intro != data['show_intro']:
                print('Pasoooooooo')
                user.show_intro = data['show_intro']
            user.save()
            serializer = UserInformationSerializer(user, context={'request': request})
            data = {
                'message': "Usuario actualizado",
                'user': serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
