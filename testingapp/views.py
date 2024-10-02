from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.views.generic import TemplateView,View,ListView,DetailView,CreateView
from django.contrib.auth import authenticate , login as authlogin
from testingapp.models import Task
from testingapp.mixins import PrintUsernameMixin


# Create your views here.

class Register(TemplateView):
    template_name="register.html"
    def post(self,request):
        username=request.POST.get('username')
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
        if password != confirm_password:
            messages.error(request,"password doesnot match")
            return redirect('register')
        if User.objects.filter(username=username).exists():
            messages.error(request,"user already exist")
            return redirect('register')
        try:
            User.objects.create_user(username=username,password=password)
            return redirect('login')
        except Exception as e:
            messages.error(request,str(e))

class Login(TemplateView):
    template_name="login.html"
    def post(self,request):
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(User,username=username,password=password)
        if user is not None:
            authlogin(request,user)
            return redirect('task_view')
        else:
            messages.error(request,"enter correct user and password")
            return redirect('login')
        
# class TaskView(LoginRequiredMixin, View):
#     def get(self,request):
#         filter_option=request.GET.get('filter',all)
#         search_text=request.GET.get('search','')
#         task = Task.objects.filter(user=request.user)
#         if filter_option == "Completed":
#             task = task.filter(completed=True)
#         elif filter_option == "Incomplete":
#             task = task.filter(completed=False)
#         if search_text:
#             task = task.filter(title__icontains=search_text)
#         return render(request,"task_view.html",{'task':task})

class TaskView(LoginRequiredMixin,PrintUsernameMixin,ListView): 
    model = Task
    template_name = "task_view.html"
    context_object_name = "task"

    def get_queryset(self,*args,**kwargs):
        queryset = super().get_queryset(*args,**kwargs)
        queryset = queryset.filter(user=self.request.user)
        filter_option = self.request.GET.get('filter',all)
        search_text = self.request.GET.get('search','')
        if filter_option == "Completed":
            queryset = queryset.filter(completed=True)
        elif filter_option == "Incomplete":
            queryset = queryset.filter(completed=False)
        if search_text:
            queryset = queryset.filter(title__icontains=search_text)
        return queryset
    
    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['username'] = self.request.user.username
        return context


# class TaskCreateView(LoginRequiredMixin ,PrintUsernameMixin,TemplateView):
#         template_name="create_task.html"
#         def post(self,request):
#             title = request.POST.get('title')
#             description = request.POST.get('description')
#             self.execute_view()        
#             if not title and not description:
#                 messages.error(request, 'Title and description are required.') 
#                 return redirect('task_view')
                
#             if Task.objects.filter(title=title).exists():
#                 messages.error(request,"task already exist") 
#                 return redirect('task_view') 
#             try:
#                 Task.objects.create(title=title, description=description, user=request.user)
#                 messages.success(request, 'Task created successfully.')
#             except Exception as e:
#                 messages.success(request, str(e))
            
#             return redirect('task_view') 

class TaskCreateView(LoginRequiredMixin, PrintUsernameMixin, CreateView):
    model = Task
    template_name = "create_task.html"
    fields = ['title', 'description']
    success_url = reverse_lazy('task_view')

    def form_valid(self, form):
        title = form.cleaned_data['title']
        
        if Task.objects.filter(title=title).exists():
            messages.error(self.request, "Task already exists.")
            return self.form_invalid(form)
        form.instance.user = self.request.user  
        messages.success(self.request, 'Task created successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Title and description are required.')
        return super().form_invalid(form)
        
class TaskUpdateView(LoginRequiredMixin,PrintUsernameMixin,DetailView):
    model = Task
    template_name = "task_update.html"
    context_object_name = 'task'

    def post(self,request,pk):
        task=Task.objects.get(pk=pk,user=request.user)
        title=request.POST.get('title')
        description=request.POST.get('description')
        if Task.objects.filter(title=title).exclude(id=task.id).exists():
            messages.error(request,"title already exist")
            return redirect('task_update',pk=pk)
        if title and description is not None:
            task.title=title
            task.description=description
            task.save()
            return redirect('task_view')
        else:
            messages.error(request,"enter title and description")
            return redirect('task_update',pk=pk)
    
# class TaskUpdateView(LoginRequiredMixin,View):
#     def get(self,request,pk):
#         task=Task.objects.get(pk=pk,user=request.user)
#         return render(request,"task_update.html",{'task':task})
#     def post(self,request,pk):
#         task=Task.objects.get(pk=pk,user=request.user)
#         title=request.POST.get('title')
#         description=request.POST.get('description')
#         if Task.objects.filter(title=title).exclude(id=task.id).exists():
#             messages.error(request,"title already exist")
#             return redirect('task_update',pk=pk)
#         if title and description is not None:
#             task.title=title
#             task.description=description
#             task.save()
#             return redirect('task_view')
#         else:
#             messages.error(request,"enter title and description")
#             return redirect('task_update',pk=pk)
        
class TaskDeleteView(LoginRequiredMixin,View):
        def get(self,request,pk):
            task=Task.objects.get(pk=pk,user=request.user)
            task.delete()
            return redirect('task_view')
        
class TaskComplete(LoginRequiredMixin,View):
    def post(self,request,pk):
        task= Task.objects.get(pk=pk,user=request.user)
        task.completed =True
        task.save()
        return redirect('task_view')





