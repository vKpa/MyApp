from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Category

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    categories = Category.objects.all()

    # フィルタリング
    category_id = request.GET.get('category')
    priority = request.GET.get('priority')
    completed = request.GET.get('completed')
    search_query = request.GET.get('search', '')

    if category_id:
        tasks = tasks.filter(category_id=category_id)
    if priority:
        tasks = tasks.filter(priority=priority)
    if completed:
        tasks = tasks.filter(completed=completed == 'True')
    if search_query:
        tasks = tasks.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))

    # ソート
    sort = request.GET.get('sort', 'created_date')  # デフォルトは作成日順
    if sort == 'due_date':
        tasks = tasks.order_by('due_date')
    elif sort == '-due_date':
        tasks = tasks.order_by('-due_date')
    elif sort == 'priority':
        tasks = tasks.order_by('-priority')  # 優先度高い順
    else:
        tasks = tasks.order_by('-created_date')

    # ページネーション
    paginator = Paginator(tasks, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'tasks': page_obj,
        'categories': categories,
        'current_category': category_id,
        'current_priority': priority,
        'current_completed': completed,
        'current_sort': sort,
        'search_query': search_query,
    }
    return render(request, 'todo/task_list.html', context)

@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    return render(request, 'todo/task_detail.html', {'task': task})

@login_required
@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'タスクが正常に作成されました。')
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'todo/task_form.html', {'form': form})

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'todo/task_form.html', {'form': form})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'todo/task_confirm_delete.html', {'task': task})

@require_POST
@login_required
def task_toggle_complete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.completed = not task.completed
    task.save()
    return JsonResponse({
        'status': 'success',
        'completed': task.completed
    })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')  # タスク一覧ページにリダイレクト
    else:
        form = UserCreationForm()
    return render(request, 'todo/register.html', {'form': form})