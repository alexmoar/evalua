# Routers provide an easy way of automatically determining the URL conf.
from rest_framework import routers

from authentication.api.view import UserInformationViewSet

router = routers.DefaultRouter()
router.register(r'user', UserInformationViewSet)
