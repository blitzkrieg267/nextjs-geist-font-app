from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import TemplateView, ListView, DetailView, UpdateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Count
from .forms import UserEditForm

class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class DashboardHomeView(AdminRequiredMixin, TemplateView):
    template_name = "dashboard/dashboard_home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_count'] = User.objects.count()
        context['staff_count'] = User.objects.filter(is_staff=True).count()
        context['active_users'] = User.objects.filter(is_active=True).count()
        context['recent_users'] = User.objects.order_by('-date_joined')[:5]
        return context

class UserListView(AdminRequiredMixin, ListView):
    model = User
    template_name = "dashboard/user_list.html"
    context_object_name = 'users'
    paginate_by = 20
    
    def get_queryset(self):
        return User.objects.all().order_by('-date_joined')

class UserDetailView(AdminRequiredMixin, DetailView):
    model = User
    template_name = "dashboard/user_detail.html"
    context_object_name = 'user_obj'

class UserEditView(AdminRequiredMixin, UpdateView):
    model = User
    form_class = UserEditForm
    template_name = "dashboard/user_edit.html"
    context_object_name = 'user_obj'
    
    def get_success_url(self):
        messages.success(self.request, f'User {self.object.username} updated successfully.')
        return reverse_lazy('user-detail', kwargs={'pk': self.object.pk})
    
    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)
