from rest_framework import serializers
from core import models
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError('Incorrect username or password.')
        if not user.is_active:
            raise serializers.ValidationError('User is disabled.')
        user.testuser = models.TestUser.objects.get_or_create(user=user)[0]
        return {'user': user}


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])
        test_user = models.TestUser.objects.get_or_create(user=user)[0]
        user.testuser = test_user
        user.save()
        return user

    def validate(self, attrs):
        is_user_exists = User.objects.filter(username=attrs["username"]).exists()
        if is_user_exists:
            raise serializers.ValidationError('User already exists.')
        return attrs


class TestUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = models.TestUser
        fields = '__all__'


class TestGroupSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = self.context['user']
        created_group = super().create(validated_data)
        test_user_for_group = models.TestUserForGroup(user=user.testuser,
                                                      group=created_group,
                                                      user_role=models.TestUserForGroup.UserRoles.ADMINISTRATOR)
        test_user_for_group.save()
        return created_group

    def update(self, instance, validated_data):
        user = self.context['user']
        is_current_user_administrator = models.TestUserForGroup.objects.filter(
            user=user.testuser,
            group=instance,
            user_role=models.TestUserForGroup.UserRoles.ADMINISTRATOR).exists()
        if not is_current_user_administrator:
            raise serializers.ValidationError('Can not update group due permissions')
        return super().update(instance, validated_data)

    class Meta:
        model = models.TestGroup
        fields = '__all__'


class TestUserForGroupSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user_data = TestUserSerializer(instance.user)
        data['user'] = user_data.data
        return data

    class Meta:
        model = models.TestUserForGroup
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = models.Answer
        fields = '__all__'


class TopicSerializer(serializers.ModelSerializer):
    group = serializers.PrimaryKeyRelatedField(read_only=True)

    def create(self, validated_data):
        validated_data['group'] = models.TestGroup.objects.get(id=self.context['group'])
        topic = super().create(validated_data)
        return topic

    class Meta:
        model = models.Topic
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    topic = serializers.PrimaryKeyRelatedField(read_only=True)
    answers = AnswerSerializer(many=True, required=False)

    def create(self, validated_data):
        validated_data['topic'] = models.Topic.objects.get(id=self.context['topic'])
        answers = validated_data.pop('answers', [])
        question = super().create(validated_data)
        self.add_answers(answers, question)
        return question

    def update(self, instance, validated_data):
        models.Answer.objects.filter(question=instance).delete()
        answers = validated_data.pop('answers', [])
        question = super().update(instance, validated_data)
        self.add_answers(answers, question)
        return question

    def add_answers(self, answers, question):
        answer_objects = []
        for i in range(len(answers)):
            answers[i]['question'] = question
            answer_objects.append(models.Answer(**answers[i]))
        models.Answer.objects.bulk_create(answer_objects)

    class Meta:
        model = models.Question
        fields = '__all__'


class AnswerForUserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnswerForUserData
        fields = '__all__'


class QuestionForUserDataSerializer(serializers.ModelSerializer):
    answers_data = AnswerForUserDataSerializer(many=True, read_only=True)

    class Meta:
        model = models.QuestionForUserData
        fields = '__all__'


class TopicForUserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TopicForUserData
        fields = '__all__'
