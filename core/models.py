from django.db import models
from django.contrib.auth.models import User


class TestUser(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.deletion.CASCADE)


class TestGroup(models.Model):
    group_name = models.CharField(max_length=255)


class TestUserForGroup(models.Model):
    class UserRoles(models.TextChoices):
        ADMINISTRATOR = 'administrator', 'administrator'
        MEMBER = 'member', 'member'

    user = models.ForeignKey(to=TestUser, on_delete=models.deletion.CASCADE, related_name='test_users')
    group = models.ForeignKey(to=TestGroup, on_delete=models.deletion.CASCADE, related_name='test_groups')
    user_role = models.CharField(max_length=255, choices=UserRoles.choices)

    class Meta:
        unique_together = ('user', 'group',)


class Topic(models.Model):
    name = models.CharField(max_length=500)
    group = models.ForeignKey(to=TestGroup, on_delete=models.deletion.CASCADE, related_name='topics')


class Question(models.Model):
    class QuestionTypes(models.TextChoices):
        TEXT = 'text', 'text'
        SINGLE_ANSWER = 'single', 'single'
        MULTIPLE_ANSWER = 'multiple', 'multiple'
    text = models.TextField()
    type = models.CharField(max_length=30, choices=QuestionTypes.choices)
    topic = models.ForeignKey(to=Topic, on_delete=models.deletion.CASCADE, related_name='questions')


class Answer(models.Model):
    right = models.BooleanField(default=False)
    text = models.TextField()
    question = models.ForeignKey(to=Question, on_delete=models.deletion.CASCADE, related_name='answers')


class TopicForUserData(models.Model):
    topic = models.ForeignKey(to=Topic, on_delete=models.deletion.CASCADE, related_name='user_data')
    user = models.ForeignKey(to=TestUser, on_delete=models.deletion.CASCADE, related_name='topic_data')
    last_answered_question = models.ForeignKey(to=Question, on_delete=models.deletion.CASCADE)
    date_started = models.DateTimeField(auto_now_add=True)


class QuestionForUserData(models.Model):
    question_number = models.IntegerField()
    topic_data = models.ForeignKey(to=TopicForUserData,
                                   on_delete=models.deletion.CASCADE, related_name='questions_data')
    question = models.ForeignKey(to=Question, on_delete=models.deletion.CASCADE)
    is_answered = models.BooleanField(default=False)
    is_right = models.BooleanField(default=False)


class AnswerForUserData(models.Model):
    question_data = models.ForeignKey(to=QuestionForUserData,
                                      on_delete=models.deletion.CASCADE, related_name='answers_data')
    answer = models.ForeignKey(to=Answer, on_delete=models.deletion.CASCADE)
