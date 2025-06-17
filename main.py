from flask import Flask, request, jsonify
import hashlib
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

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

if __name__ == '__main__':
    init_db()
    app.run(debug=True)セッション管理を実装するために必要な権限をいただけますか？Flask-Loginをrequirements.txtに追加し、main.pyにセッション管理機能を実装する必要があります。
