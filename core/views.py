from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework import views, permissions, response, status
from rest_framework.mixins import RetrieveModelMixin, \
    ListModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.authentication import TokenAuthentication


from core import serializers
from core import models
from core.permissions import IsGroupOwner, IsGroupMember


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):  # auth
        serializer = serializers.LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return response.Response({'error': serializer.errors}, status=status.HTTP_401_UNAUTHORIZED)
        user = serializer.validated_data['user']
        token = Token.objects.get_or_create(user=user)
        return response.Response({'token': token[0].key})

    def put(self, request):  # registration
        serializer = serializers.RegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            return response.Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.save()
        token = Token.objects.get_or_create(user=user)
        return response.Response({'token': token[0].key})


class TestGroupsViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    model = models.TestGroup
    serializer_class = serializers.TestGroupSerializer

    def get_queryset(self):
        return models.TestGroup.objects.filter(test_groups__user=self.request.user.id)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context


class TestGroupSettingsViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsGroupOwner]
    model = models.TestUserForGroup
    serializer_class = serializers.TestUserForGroupSerializer

    def get_queryset(self):
        return models.TestUserForGroup.objects.filter(
            group__id=self.kwargs.get('group', '-1')
        )


class TopicViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsGroupMember]
    model = models.Topic
    serializer_class = serializers.TopicSerializer

    def get_queryset(self):
        return models.Topic.objects.filter(group__id=self.kwargs.get('group', '-1'))

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['group'] = self.kwargs.get('group', '-1')
        return context


class QuestionViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsGroupMember]
    model = models.Topic
    serializer_class = serializers.QuestionSerializer

    def get_queryset(self):
        return models.Question.objects.filter(topic__id=self.kwargs.get('topic', '-1'))

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['group'] = self.kwargs.get('group', '-1')
        context['topic'] = self.kwargs.get('topic', '-1')
        return context
