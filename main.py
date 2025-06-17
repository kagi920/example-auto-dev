from flask import Flask, request, jsonify, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import hashlib
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

def get_db_connection():
    db_path = app.config.get('DATABASE', 'users.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

class User(UserMixin):
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    user_data = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    if user_data:
        return User(user_data['id'], user_data['username'], user_data['email'])
    return None

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ('username', 'email', 'password')):
            return jsonify({'error': '必須フィールドが不足しています'}), 400
        
        username = data['username']
        email = data['email']
        password = data['password']
        
        if len(password) < 6:
            return jsonify({'error': 'パスワードは6文字以上である必要があります'}), 400
        
        password_hash = hash_password(password)
        
        conn = get_db_connection()
        try:
            conn.execute(
                'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
                (username, email, password_hash)
            )
            conn.commit()
            return jsonify({'message': 'ユーザーが正常に作成されました'}), 201
        except sqlite3.IntegrityError:
            return jsonify({'error': 'ユーザー名またはメールアドレスが既に存在します'}), 409
        finally:
            conn.close()
            
    except Exception as e:
        return jsonify({'error': 'サーバーエラーが発生しました'}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ('username', 'password')):
            return jsonify({'error': 'ユーザー名とパスワードが必要です'}), 400
        
        username = data['username']
        password = data['password']
        password_hash = hash_password(password)
        
        conn = get_db_connection()
        user_data = conn.execute(
            'SELECT * FROM users WHERE username = ? AND password_hash = ?',
            (username, password_hash)
        ).fetchone()
        conn.close()
        
        if user_data:
            user = User(user_data['id'], user_data['username'], user_data['email'])
            login_user(user)
            return jsonify({'message': 'ログインしました', 'user_id': user.id}), 200
        else:
            return jsonify({'error': 'ユーザー名またはパスワードが正しくありません'}), 401
            
    except Exception as e:
        return jsonify({'error': 'サーバーエラーが発生しました'}), 500

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'ログアウトしました'}), 200

@app.route('/profile')
@login_required
def profile():
    return jsonify({
        'user_id': current_user.id,
        'username': current_user.username,
        'email': current_user.email
    }), 200

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
パスワードリセット機能の実装のため、以下の変更が必要です：

1. データベーステーブル追加（password_reset_tokens）
2. メール送信機能の実装
3. トークン生成・検証機能
4. `/reset-password` エンドポイント

ファイル編集の権限を許可していただければ、実装を進めます。
