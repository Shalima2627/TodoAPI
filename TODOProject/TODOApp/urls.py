from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api',views.TodoListAPIView.as_view()),
    path('api/<int:todo_id>',views.DetailTodoAPIView.as_view()),
]