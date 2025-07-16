from django.urls import path
from .views import DashboardHomeView, UserListView, UserDetailView, UserEditView

urlpatterns = [
    path('', DashboardHomeView.as_view(), name='dashboard-home'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('users/<int:pk>/edit/', UserEditView.as_view(), name='user-edit'),
]
