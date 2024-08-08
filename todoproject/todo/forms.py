from django import forms
from .models import Task, Category

class TaskForm(forms.ModelForm):
    """タスク作成・編集用のフォーム

    タスクモデルに基づいて、ユーザーがタスクを作成・編集するためのフォームを提供する
    """
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="カテゴリを選択",
        required=False,
        label='カテゴリ'
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'category', 'priority']
        labels = {
            'title': 'タイトル',
            'description': '説明',
            'due_date': '期限',
            'priority': '優先度',
        }
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }