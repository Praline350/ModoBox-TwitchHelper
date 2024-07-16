from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required

from authentication.serializers import *


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_token(request):
    user = request.user
    serializer = UserSerializer(user)

    return Response(serializer.data)