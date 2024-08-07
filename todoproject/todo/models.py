from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """カテゴリモデル

    タスクを分類するためのカテゴリ

    Attributes:
        name: カテゴリ名
        color: カテゴリを表す色のHEXコード
    """
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default='#007bff')

    def __str__(self):
        return self.name


class Task(models.Model):
    """タスクモデル

    ユーザーのToDoタスク

    Attributes:
        title: タスクのタイトル
        description: タスクの詳細説明
        created_date: タスクの作成日時
        due_date: タスクの期限
        completed: タスクの完了状態
        category: タスクのカテゴリ
        priority: タスクの優先度
        user: タスクの所有者
    """
    PRIORITY_CHOICES = [
        ('low', '低'),
        ('medium', '中'),
        ('high', '高'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} （期限: {self.due_date}）'