from django.urls import path
from rest_framework.routers import SimpleRouter
from core import views

router = SimpleRouter()
router.register(r'groups/(?P<group>\d+)/settings', views.TestGroupSettingsViewSet, basename='modules')
router.register(r'groups/(?P<group>\d+)/topics/(?P<topic>\d+)/questions',
                views.QuestionViewSet, basename='topics')
router.register(r'groups/(?P<group>\d+)/topics', views.TopicViewSet, basename='topics')
router.register(r'groups', views.TestGroupsViewSet, basename='groups')

urlpatterns = [
    path('login/', views.LoginView.as_view()),
]

urlpatterns += router.urls
