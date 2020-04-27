from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token
from . import views

session_endpoint = [
  path('', views.HomeView.as_view(), name='HomeView'),
]

app_name = "jaded.api"
urlpatterns = [
  path('sessions/', include(session_endpoint)),
  path('token_auth/', obtain_jwt_token),
  path('token_verify/', verify_jwt_token),
  path('current_user/', views.current_user.as_view()),
]
