from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'category', 'priority']
        labels = {
            'title': 'タイトル',
            'description': '説明',
            'due_date': '期限',
            'category': 'カテゴリ',
            'priority': '優先度',
        }
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }