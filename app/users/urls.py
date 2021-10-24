from django.urls import path

from users.views import CreateTokenView, CreateUserView, RetrieveUpdateUserView

app_name = "users"

urlpatterns = [
    path("token/", CreateTokenView.as_view(), name="token"),
    path("create/", CreateUserView.as_view(), name="create"),
    path("me/", RetrieveUpdateUserView.as_view(), name="me"),
]

