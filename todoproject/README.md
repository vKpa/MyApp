# Todoリストアプリケーション

このプロジェクトは、Django を使用して開発された簡単な Todo リストアプリケーションです。ユーザーはタスクの作成、編集、削除、および完了状態の管理ができます。

## 機能

- ユーザー認証（登録、ログイン、ログアウト）
- タスクの作成、編集、削除
- タスクの完了状態の切り替え
- タスクのカテゴリ分け
- タスクの優先度設定
- タスクのフィルタリングと並び替え

## 必要条件

- Python 3.8以上
- Django 4.2以上

## インストール

1. リポジトリをクローン：
   ```
   git clone git@github.com:vKpa/MyApp1.git
   ```

2. `.env` ファイルをプロジェクトのルートディレクトリに作成し、以下の変数を設定する：
   ```
   SECRET_KEY=your_secret_key_here
   DATABASE_URL=sqlite:///db.sqlite3
   ```

3. 仮想環境を作成し、アクティベート：

   ```
   python -m venv venv
   source venv/bin/activate  # Windowsの場合: venv\Scripts\activate
   ```


4. データベースの移行：

   ```
   python manage.py migrate
   ```

5. 管理者ユーザーを作成：

   ```
   python manage.py createsuperuser
   ```

## 使用方法

1. 開発サーバーを起動：
   ```
   python manage.py runserver
   ```

2. ブラウザで http://127.0.0.1:8000 にアクセス。

3. 新規ユーザーとして登録するか、作成した管理者アカウントでログイン。

4. タスクの追加、編集、削除、完了状態の変更を行う。

## 管理画面

管理画面にアクセスするには、http://127.0.0.1:8000/admin/ にアクセスし、作成した管理者アカウントでログインする。


