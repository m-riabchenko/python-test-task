from django.urls import path

from python_test_task.magic_auth import views

urlpatterns = [
    path("", views.enter_email, name="enter_email"),
    path("auth/<str:magic_token>", views.auth, name="auth"),
]
