from flask import Flask, render_template, redirect, url_for,session, Blueprint
from auth import login_required
from ui import login,logout, main_window, change_password,user_management,contract_management, payment_management, expense_management  # 在这里添加 expense_management
from database import init_db,User  # 添加这一行
#from flask_caching import Cache
from cache_config import cache
from contracts import contracts_bp
from payments import payments_bp
from costs import costs_bp
from flask import Flask, request, jsonify, render_template
from ui import ui_bp
from flask_login import LoginManager
from flask_socketio import SocketIO
import openai
openai.api_key = "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"

# main.py
app = Flask(__name__)

socketio = SocketIO(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = 'your_secret_key'
app.register_blueprint(login.bp)
app.register_blueprint(logout.bp)
app.register_blueprint(main_window.bp)
app.register_blueprint(contract_management.bp)
app.register_blueprint(payment_management.bp)
app.register_blueprint(expense_management.bp)
app.register_blueprint(user_management.bp)
app.register_blueprint(change_password.bp)
app.config['CACHE_TYPE'] = 'simple'
app.register_blueprint(contracts_bp)
app.register_blueprint(payments_bp)
app.register_blueprint(ui_bp)
app.register_blueprint(costs_bp)
app.config['UPLOAD_FOLDER'] = 'uploads'
cache.init_app(app)

def generate_bot_response(user_message):
    prompt = f"User: {user_message}\nAI:"
    response = openai.Completion.create(
        model="gpt-3.5-turbo",  # 使用 GPT-3.5 模型
        prompt=prompt,
        max_tokens=1000,  # 设置回复的最大长度
        n=1,
        stop=None,
        temperature=0.3,  # 控制回复的随机性，范围从 0 到 1
    )

    # 提取生成的回复
    bot_message = response.choices[0].text.strip()

    return bot_message

@app.route('/')
def index():
    return redirect(url_for('login.login'))
from database import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.context_processor
def inject_user():
    if 'username' in session:
        current_username = session['username']
        user = User.query.filter_by(username=current_username).first()
    else:
        user = None
    return {'user': user}

@app.route('/chat', methods=['POST'])

@login_required
def chat():
    user_message = request.form.get('message')
    
    # 调用 GPT-3.5 生成回复
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"User: {user_message}\nBot:",
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )

    bot_message = response.choices[0].text.strip()
    return jsonify({'message': bot_message})
@socketio.on('send_message')
def handle_send_message_event(data):
    user_message = data['message']
    # 在这里调用 GPT-3.5 模型并生成回复
    bot_message = generate_bot_response(user_message)
    socketio.emit('receive_message', {'message': bot_message})

@socketio.on('send_message')
def handle_send_message_event(data):
    user_message = data['message']
    # 在这里调用 GPT-3.5 模型并生成回复
    bot_message = generate_bot_response(user_message)
    socketio.emit('receive_message', {'message': bot_message})

init_db(app)

if __name__ == '__main__':
    app.run(debug=True)
