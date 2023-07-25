from home.views import index,people,login,PersonAPI,PeopleViewSet,RegisterAPI,LoginAPI
from rest_framework.routers import DefaultRouter
from django.urls import path,include

router = DefaultRouter()
router.register(r'people', PeopleViewSet, basename='people')
urlpatterns = router.urls
urlpatterns = [
    path("",include(router.urls)),
    path('index/', index),
    path('person/',people),
    path('login/',login),
    path('person-api-class/',PersonAPI.as_view()),
    path("register/",RegisterAPI.as_view()),
    path('signin/',LoginAPI.as_view())
]
