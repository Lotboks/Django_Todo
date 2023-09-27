from django.views import View
from base.models import Task, TaskContainer
from django.shortcuts import render, redirect, get_object_or_404
from base.forms import TaskForm, TaskFileForm, RegistrationForm, CustomAuthenticationForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.utils import timezone

class ContainerListView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        containers = TaskContainer.objects.filter(user=request.user)
        return render(request, 'base/container_list.html', {'containers': containers}) 


class ContainerCreateView(LoginRequiredMixin, View):
    login_url = '/login/'
    def post(self, request):
        form = TaskFileForm(request.POST)
        if form.is_valid():
            container = form.save(commit=False)
            container.user = request.user
            container.save()
            return redirect('container_list')
        
        return render(request, 'base/create_container.html', {'form': form})

    def get(self, request):
        # if not request.user.is_authenticated:
        #     return redirect('login')
        form = TaskFileForm()
        return render(request, 'base/create_container.html', {'form': form})

class ContainerDetailView(View):
    def get(self, request, container_id):
        container = get_object_or_404(TaskContainer, pk=container_id)
        if container.user.id != request.user.id:
            return HttpResponse(status=403)

        search_input = request.GET.get('search-area', '')

        tasks = Task.objects.filter(container=container, user=request.user)
        if search_input:
            tasks = tasks.filter(title__icontains=search_input)

        tasks = tasks.order_by('completed', 'due')
        now = timezone.now()

        for task in tasks:
            if task.due and task.due < now and not task.completed:
                task.completed = True
                task.completed_at = now
        Task.objects.bulk_update(tasks, ['completed', 'completed_at'])

        context = {
            'container': container,
            'tasks': tasks,
            'search_input': search_input,
        }
        return render(request, 'base/container_detail.html', context)
    

class TaskCreateView(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request, container_id):
        container = get_object_or_404(TaskContainer, pk=container_id, user=request.user)
        form = TaskForm(request.POST)
        context = {'form': form, 'container': container}

        if form.is_valid():
            task = form.save(commit=False)
            task.container = container
            task.user = request.user
            task.save()
            return redirect('container_detail', container_id=container_id)

        return render(request, 'base/create_task.html', context)

    def get(self, request, container_id):
        container = get_object_or_404(TaskContainer, pk=container_id, user=request.user)
        form = TaskForm()
        context = {'form': form, 'container': container}
        return render(request, 'base/create_task.html', context)

class TaskUpdateView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        form = TaskForm(instance=task)
        context = {'form': form, 'task': task}
        return render(request, 'base/update_task.html', context)

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        form = TaskForm(request.POST, instance=task)
        context = {'form': form, 'task': task}
        if form.is_valid():
            if form.cleaned_data['completed']:
                task.completed_at = timezone.now()
            else:
                task.completed_at = None
            form.save()
            container_id = task.container.id
            return redirect('container_detail', container_id=container_id)
        return render(request, 'base/update_task.html', context)

class TaskDeleteView(View):
    def get(self, request, pk):
        if not request.user.is_authenticated:
            return redirect('login')

        task = get_object_or_404(Task, pk=pk)
        return render(request, 'base/task_confirm_delete.html', {'task': task})
    
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        if 'confirm' in request.POST:
            task.delete()
            container_id = task.container.id
            return redirect('container_detail', container_id=container_id)

        return redirect('delete_task', pk=pk)


class ContainerDeleteView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, container_id):
        container = get_object_or_404(TaskContainer, pk=container_id)
        return render(request, 'base/container_confirm_delete.html', {'container': container})

    def post(self, request, container_id):
        container = get_object_or_404(TaskContainer, pk=container_id)
        if 'confirm' in request.POST:
            container.delete()
            return redirect('container_list')

        return redirect('delete_container', container_id=container_id)


class CustomLoginView(View):
    template_name = 'base/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('container_list')
        
        form = CustomAuthenticationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('container_list')
        
        form = CustomAuthenticationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('container_list')
            else:
                form.add_error(None, 'Invalid username or password!')

        return render(request, self.template_name, {'form': form})


class CustomRegisterView(View):
    template_name = 'base/register.html'

    def get(self, request):
        if self.request.user.is_authenticated:
            return redirect('container_list')
        return render(request, self.template_name, {'form': RegistrationForm()})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            confirm_password = form.cleaned_data.get('confirm_password')

            # Check if the password and confirm_password fields match
            if password == confirm_password:
                user = form.save()
                login(request, user)
                return redirect('container_list')
            else:
                # Passwords don't match, add an error to the form
                form.add_error('confirm_password', 'Passwords do not match')
        return render(request, self.template_name, {'form': form})
    

# class CustomRegisterView(View):
#     template_name = 'base/register.html'

#     def get(self, request):
#         if self.request.user.is_authenticated:
#             return redirect('container_list')
#         return render(request, self.template_name, {'form': RegistrationForm()})

#     def post(self, request):
#         try:
#             form = RegistrationForm(request.POST)
#             if form.is_valid():
#                 user = form.save()
#                 login(request, user)
#                 return redirect('container_list')
#         except Exception as e:
#             # Handle the exception here, e.g., log it or display an error message
#             return render(request, self.template_name, {'form': form, 'error_message': str(e)})

#         # If no exception occurred, render the template with the form
#         return render(request, self.template_name, {'form': form})

