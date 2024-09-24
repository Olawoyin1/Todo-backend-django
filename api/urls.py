from django.urls import path
from . import views


urlpatterns = [
    path("", views.TodoList.as_view(), name="todo"),
    path("<str:pk>/", views.TodoActions.as_view(), name="todoactions"),
]
