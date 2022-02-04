from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    # routes for creating a user
    path('create/', views.CreateUserView.as_view(), name='create'),
    # routes for validating, authenticating, & returning a users' token
    path('token/', views.CreateTokenView.as_view(), name='token'),

    path('manage/', views.ManageUserView.as_view(), name='manage_user'),

]
