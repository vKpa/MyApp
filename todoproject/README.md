# Todoリストアプリケーション

このプロジェクトは、Django を使用して開発された簡単な Todo リストアプリケーションです。ユーザーはタスクの作成、編集、削除、および完了状態の管理ができます。

## 機能

- ユーザー認証（登録、ログイン、ログアウト）
- タスクの作成、編集、削除
- タスクの完了状態の切り替え（Ajax使用）
- タスクのカテゴリ分け（色分け機能付き）
- タスクの優先度設定（高、中、低）
- タスクのフィルタリング（カテゴリ、優先度、完了状態）
- タスクの並び替え（タイトル、期限、優先度）
- タスクの検索機能
- ページネーション
- レスポンシブデザイン（Bootstrap使用）

## 最新の改善点

- ユニットテストを実装し、主要な機能のテストカバレッジを向上
- テストカバレッジの測定を行い、全体で94%のカバレッジを達成

## テスト実施について

1. テストの実行方法：
   ```
   python manage.py test todo
   ```

2. テストカバレッジの測定：
   ```
   coverage run --source='.' manage.py test todo
   coverage report
   coverage html
   ```

3. テストカバレッジの結果：
- 全体のカバレッジ: 94%
- 主要なファイルのカバレッジ：
  - todo/views.py: 96%
  - todo/models.py: 92%
  - todo/forms.py: 100%
  - todo/urls.py: 100%


## 必要条件

- Python 3.8以上
- Django 4.2以上

## インストール

1. リポジトリをクローン：
   ```
   git clone git@github.com:vKpa/MyApp.git
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

5. フィルター、ソート、検索機能を使用してタスクを管理する。

## 管理画面

管理画面では、タスクやカテゴリなどのアプリケーションデータを直接管理することができます。

### アクセス方法

1. 開発サーバーを起動する: `python manage.py runserver`
2. ブラウザで http://127.0.0.1:8000/admin/ にアクセスする
3. 作成した管理者アカウントでログインする

### カテゴリの追加

1. 管理画面にログインした後、「Categories」セクションに移動する
2. 「ADD CATEGORY」ボタンをクリックする
3. 以下の情報を入力する：
   - Name: システム内部で使用するカテゴリ名
   - Display name: ユーザーに表示されるカテゴリ名
   - Color: カテゴリの色（HEXコード）
4. 「Save」ボタンをクリックして、新しいカテゴリを保存する

注意: カテゴリを追加した後、Todoアプリケーション内でタスクの作成や編集時に新しいカテゴリが選択可能になります。

### その他の管理機能

- タスクの一括編集や削除
- ユーザーアカウントの管理
- アプリケーション全体の設定管理

管理画面を通じて、アプリケーションのデータを効率的に管理し、必要に応じてカスタマイズすることができます。