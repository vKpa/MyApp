from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Task, Category
from datetime import timedelta
from .views import filter_tasks, sort_tasks

class TodoTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.category = Category.objects.create(name='TestCategory', display_name='Test Category')
        self.task = Task.objects.create(
            title='Test Task',
            description='This is a test task',
            due_date=timezone.now() + timedelta(days=1),
            user=self.user,
            category=self.category,
            priority='medium',
            completed=False
        )

    def test_task_list_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/task_list.html')
        # タスクが実際にデータベースに存在するか確認
        self.assertTrue(Task.objects.filter(title='Test Task').exists())
        self.assertContains(response, 'Test Task')

    def test_task_create_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('task_create'))
        self.assertEqual(response.status_code, 200)

        new_task_data = {
            'title': 'New Test Task',
            'description': 'This is a new test task',
            'due_date': (timezone.now() + timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S'),
            'category': self.category.id,
            'priority': 'high'
        }
        response = self.client.post(reverse('task_create'), new_task_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(title='New Test Task').exists())

    def test_task_update_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('task_update', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)

        updated_task_data = {
            'title': 'Updated Test Task',
            'description': 'This is an updated test task',
            'due_date': (timezone.now() + timedelta(days=3)).strftime('%Y-%m-%d %H:%M:%S'),
            'category': self.category.id,
            'priority': 'low'
        }
        response = self.client.post(reverse('task_update', args=[self.task.id]), updated_task_data)
        self.assertEqual(response.status_code, 302)
        updated_task = Task.objects.get(id=self.task.id)
        self.assertEqual(updated_task.title, 'Updated Test Task')

    def test_task_delete_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('task_delete', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_task_toggle_complete(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('task_toggle_complete', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'status': 'success', 'completed': True})
        self.task.refresh_from_db()
        self.assertTrue(self.task.completed)

    def test_filter_tasks(self):
        tasks = Task.objects.all()

        # 各フィルター条件でのテスト
        test_cases = [
            (str(self.category.id), self.task.priority, str(self.task.completed), 'Test', 1),
            (str(self.category.id), 'medium', 'False', 'Test', 1),
            (str(self.category.id), None, None, None, 1),
            (None, 'medium', None, None, 1),
            (None, None, 'False', None, 1),
            (None, None, None, 'Test', 1),
            (None, None, None, 'NonExistent', 0),
        ]

        for category_id, priority, completed, search_query, expected_count in test_cases:
            filtered_tasks = filter_tasks(tasks, category_id, priority, completed, search_query)
            self.assertEqual(filtered_tasks.count(), expected_count)

        # エッジケースのテスト
        edge_cases = [
            ('999', 'high', 'True', 'Nonexistent', 0),  # 存在しないカテゴリ
            (str(self.category.id), 'invalid', 'False', 'Test', 0),  # 無効な優先度
            (str(self.category.id), 'medium', 'invalid', 'Test', 0),  # 無効な完了状態
        ]

        for category_id, priority, completed, search_query, expected_count in edge_cases:
            filtered_tasks = filter_tasks(tasks, category_id, priority, completed, search_query)
            self.assertEqual(filtered_tasks.count(), expected_count,
                                f"Failed for: category_id={category_id}, priority={priority}, "
                                f"completed={completed}, search_query={search_query}")

    def test_sort_tasks(self):
        Task.objects.create(
            title='Another Task',
            description='Another Description',
            due_date=timezone.now() + timedelta(days=2),
            user=self.user,
            category=self.category
        )
        tasks = Task.objects.all()
        sorted_tasks = sort_tasks(tasks, 'due_date')
        self.assertEqual(sorted_tasks.first(), self.task)

    def test_register_success(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_failure(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'testpassword123',
            'password2': 'differentpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='newuser').exists())

    def test_task_create_view_invalid_data(self):
        self.client.login(username='testuser', password='12345')
        invalid_task_data = {
            'title': '',  # タイトルを空にして無効なデータをテスト
            'description': 'This is an invalid task',
            'due_date': (timezone.now() + timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S'),
            'category': self.category.id,
            'priority': 'high'
        }
        response = self.client.post(reverse('task_create'), invalid_task_data)
        self.assertEqual(response.status_code, 200)  # フォームが再表示されることを確認
        self.assertFalse(Task.objects.filter(description='This is an invalid task').exists())
