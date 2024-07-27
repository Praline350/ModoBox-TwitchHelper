from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from chat.models import *
from API.serializers import *


class MultipleSerializerMixin:

    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy'] and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()
    

class ChatMesssageViewset(MultipleSerializerMixin, ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatMessageSerializer

    def get_queryset(self):
        return ChatMessage.objects.all()


class UserChatSettingsDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            settings = user.userchatsettings
        except UserChatSettings.DoesNotExist:
            settings = UserChatSettings(user=user)
            settings.save()

        serializer = UserChatSettingSerializer(settings)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        try:
            settings = user.userchatsettings
        except UserChatSettings.DoesNotExist:
            settings = UserChatSettings(user=user)

        serializer = UserChatSettingSerializer(settings, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class GetTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            print("User is authenticated:", user)
        else:
            print("User is not authenticated")
        serializer = UserSerializer(user)
        return Response(serializer.data)