# Django core imports
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.utils.http import urlencode
from django.views.decorators.http import require_POST

# Local imports
from .models import Task, Category
from .forms import TaskForm

def filter_tasks(tasks, category_id, priority, completed, search_query):
    """タスクのクエリセットをフィルタリングする

    Args:
        tasks (QuerySet): フィルタリング前のタスククエリセット
        category_id (str): フィルタリングするカテゴリID
        priority (str): フィルタリングする優先度
        completed (str): フィルタリングする完了状態
        search_query (str): 検索クエリ

    Returns:
        QuerySet: フィルタリング後のタスククエリセット
    """
    if category_id:
        tasks = tasks.filter(category_id=category_id)
    if priority:
        tasks = tasks.filter(priority=priority)
    if completed:
        tasks = tasks.filter(completed=completed == 'True')
    if search_query:
        tasks = tasks.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))
    return tasks

def sort_tasks(tasks, sort_param):
    """タスクのクエリセットをソートする

    Args:
        tasks (QuerySet): ソート前のタスククエリセット
        sort_param (str): ソートのパラメータ

    Returns:
        QuerySet: ソート後のタスククエリセット
    """
    sort_mapping = {
        'due_date': 'due_date',
        '-due_date': '-due_date',
        'priority': '-priority',
        '-priority': 'priority',
        'created_date': 'created_date',
        '-created_date': '-created_date'
    }
    return tasks.order_by(sort_mapping.get(sort_param, '-created_date'))

@login_required
def task_list(request):
    """ログインユーザーのタスク一覧を表示する

    フィルタリング、ソート、検索、ページネーション機能を提供

    Args:
        request (HttpRequest): HTTPリクエストオブジェクト

    Returns:
        HttpResponse: レンダリングされたタスク一覧ページ
    """
    tasks = Task.objects.filter(user=request.user)
    categories = Category.objects.all()

    # フィルタリングとソートのパラメータを取得
    category_id = request.GET.get('category')
    priority = request.GET.get('priority')
    completed = request.GET.get('completed')
    search_query = request.GET.get('search', '')
    sort = request.GET.get('sort', '-created_date')

    # タスクのフィルタリングとソート
    tasks = filter_tasks(tasks, category_id, priority, completed, search_query)
    tasks = sort_tasks(tasks, sort)

    # ページネーション
    paginator = Paginator(tasks, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 現在のGETパラメータを取得し、'page'と'sort'を除去
    query_params = request.GET.copy()
    query_params.pop('page', None)
    query_params.pop('sort', None)

    context = {
        'page_obj': page_obj,
        'tasks': page_obj,
        'categories': categories,
        'current_category': category_id,
        'current_priority': priority,
        'current_completed': completed,
        'current_sort': sort,
        'search_query': search_query,
        'query_params': urlencode(query_params),
    }
    return render(request, 'todo/task_list.html', context)

@login_required
def task_detail(request, pk):
    """タスクの詳細を表示する

    Args:
        request (HttpRequest): HTTPリクエストオブジェクト
        pk (int): タスクのプライマリーキー

    Returns:
        HttpResponse: レンダリングされたタスク詳細ページ

    Raises:
        Http404: 指定されたタスクが存在しない場合
    """
    task = get_object_or_404(Task, pk=pk, user=request.user)
    return render(request, 'todo/task_detail.html', {'task': task})

@login_required
def task_create(request):
    """新しいタスクを作成する

    Args:
        request (HttpRequest): HTTPリクエストオブジェクト

    Returns:
        HttpResponse: 成功時はタスク一覧ページへのリダイレクト
                      失敗時は新規作成フォームを表示
    """
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'タスクが正常に作成されました')
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'todo/task_form.html', {'form': form})

@login_required
def task_update(request, pk):
    """既存のタスクを更新する

    Args:
        request (HttpRequest): HTTPリクエストオブジェクト
        pk (int): 更新するタスクのプライマリーキー

    Returns:
        HttpResponse: 成功時はタスク一覧ページへのリダイレクト
                      失敗時は編集フォームを再表示

    Raises:
        Http404: 指定されたタスクが存在しない場合
    """
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'タスクが正常に更新されました')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'todo/task_form.html', {'form': form})

@login_required
def task_delete(request, pk):
    """タスクを削除する

    Args:
        request (HttpRequest): HTTPリクエストオブジェクト
        pk (int): 削除するタスクのプライマリーキー

    Returns:
        HttpResponse: 成功時はタスク一覧ページへのリダイレクト
                      確認時は削除確認ページを表示

    Raises:
        Http404: 指定されたタスクが存在しない場合
    """
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'タスクが正常に削除されました')
        return redirect('task_list')
    return render(request, 'todo/task_confirm_delete.html', {'task': task})

@require_POST
@login_required
def task_toggle_complete(request, pk):
    """タスクの完了状態を切り替える

    Args:
        request (HttpRequest): HTTPリクエストオブジェクト
        pk (int): 切り替えるタスクのプライマリーキー

    Returns:
        JsonResponse: タスクの新しい状態を含むJSON応答

    Raises:
        Http404: 指定されたタスクが存在しない場合
    """
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.completed = not task.completed
    task.save()
    return JsonResponse({
        'status': 'success',
        'completed': task.completed
    })

def register(request):
    """新規ユーザーを登録する

    Args:
        request (HttpRequest): HTTPリクエストオブジェクト

    Returns:
        HttpResponse: 成功時はタスク一覧ページへのリダイレクト
                      失敗時は登録フォームを再表示
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '正常に登録されました')
            return redirect('task_list')
    else:
        form = UserCreationForm()
    return render(request, 'todo/register.html', {'form': form})