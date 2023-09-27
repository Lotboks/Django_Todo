from django.urls import path
from base.views import (
    TaskCreateView,
    TaskDeleteView,
    TaskUpdateView, 
    CustomLoginView, 
    CustomRegisterView, 
    ContainerCreateView, 
    ContainerListView, 
    ContainerDetailView,
    ContainerDeleteView
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', CustomRegisterView.as_view(), name='register'),

    path('', ContainerListView.as_view(), name='container_list'),
    path('create_container/', ContainerCreateView.as_view(), name='create_container'),
    path('delete/<int:pk>/', TaskDeleteView.as_view(), name='delete_task'),
    path('update/<int:pk>/', TaskUpdateView.as_view(), name='update_task'),
    path('container/<int:container_id>/', ContainerDetailView.as_view(), name='container_detail'),
    path('container/<int:container_id>/create_task/', TaskCreateView.as_view(), name='create_task'),
    path('container/<int:container_id>/delete/', ContainerDeleteView.as_view(), name='delete_container'),
]