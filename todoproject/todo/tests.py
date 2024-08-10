from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Task, Category
from datetime import datetime, timedelta


class TodoTestCase(TestCase):
    def setUp(self):
        # テスト用のユーザーを作成
        self.user = User.objects.create_user(username='testuser', password='12345')

        # テスト用のカテゴリを作成
        self.category = Category.objects.create(name='Test Category', display_name='Test Category')

        # テスト用のタスクを作成
        self.task = Task.objects.create(
            title='Test Task',
            description='This is a test task',
            due_date=timezone.now() + timedelta(days=1),
            user=self.user,
            category=self.category,
            priority='medium'
        )

        # クライアントを設定
        self.client = Client()

    def test_task_list_view(self):
        # ログインする
        self.client.login(username='testuser', password='12345')

        # タスク一覧ページにアクセス
        response = self.client.get(reverse('task_list'))

        # レスポンスのステータスコードを確認
        self.assertEqual(response.status_code, 200)

        # テンプレートが正しいか確認
        self.assertTemplateUsed(response, 'todo/task_list.html')

        # コンテキストにタスクが含まれているか確認
        self.assertContains(response, 'Test Task')

    def test_task_create_view(self):
        # ログインする
        self.client.login(username='testuser', password='12345')

        # タスク作成ページにアクセス
        response = self.client.get(reverse('task_create'))
        self.assertEqual(response.status_code, 200)

        # 新しいタスクを作成
        new_task_data = {
            'title': 'New Test Task',
            'description': 'This is a new test task',
            'due_date': (timezone.now() + timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S'),
            'category': self.category.id,
            'priority': 'high'
        }
        response = self.client.post(reverse('task_create'), new_task_data)

        # リダイレクトされたか確認
        self.assertEqual(response.status_code, 302)

        # 新しいタスクがデータベースに追加されたか確認
        self.assertTrue(Task.objects.filter(title='New Test Task').exists())

    def test_task_update_view(self):
        # ログインする
        self.client.login(username='testuser', password='12345')

        # タスク更新ページにアクセス
        response = self.client.get(reverse('task_update', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)

        # タスクを更新
        updated_task_data = {
            'title': 'Updated Test Task',
            'description': 'This is an updated test task',
            'due_date': (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d %H:%M:%S'),
            'category': self.category.id,
            'priority': 'low'
        }
        response = self.client.post(reverse('task_update', args=[self.task.id]), updated_task_data)

        # リダイレクトされたか確認
        self.assertEqual(response.status_code, 302)

        # タスクが更新されたか確認
        updated_task = Task.objects.get(id=self.task.id)
        self.assertEqual(updated_task.title, 'Updated Test Task')

    def test_task_delete_view(self):
        # ログインする
        self.client.login(username='testuser', password='12345')

        # タスク削除を実行
        response = self.client.post(reverse('task_delete', args=[self.task.id]))

        # リダイレクトされたか確認
        self.assertEqual(response.status_code, 302)

        # タスクが削除されたか確認
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_task_toggle_complete(self):
        # ログインする
        self.client.login(username='testuser', password='12345')

        # タスクの完了状態を切り替え
        response = self.client.post(reverse('task_toggle_complete', args=[self.task.id]))

        # JSONレスポンスを確認
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'status': 'success', 'completed': True})

        # データベース上でタスクの状態が更新されたか確認
        updated_task = Task.objects.get(id=self.task.id)
        self.assertTrue(updated_task.completed)
