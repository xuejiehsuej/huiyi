from flask import Flask, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from config import config
import os

app = Flask(__name__)
app.config.from_object(config[os.environ.get('FLASK_ENV') or 'default'])

# 示例用户数据 - 在实际应用中应使用数据库
users = {
    'admin': {
        'password': generate_password_hash('admin123'),
        'name': '管理员'
    },
    'user': {
        'password': generate_password_hash('user123'),
        'name': '普通用户'
    }
}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('请先登录', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in users and check_password_hash(users[username]['password'], password):
            session['username'] = username
            session['name'] = users[username]['name']
            session.permanent = True
            flash(f'欢迎回来, {users[username]["name"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('用户名或密码错误', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('name', None)
    flash('您已成功退出', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=session.get('name', '用户'))

# 1. 线下参会用户的地图指引
@app.route('/map-guide')
@login_required
def map_guide():
    return render_template('features/map_guide.html')

# 2. 问答系统
@app.route('/qa-system')
@login_required
def qa_system():
    return render_template('features/qa_system.html')

# 3. 参会指南
@app.route('/conference-guide')
@login_required
def conference_guide():
    return render_template('features/conference_guide.html')

# 4. 线上用户的会议亮点推荐
@app.route('/highlights')
@login_required
def highlights():
    return render_template('features/highlights.html')

# 5. 论坛关注度排行
@app.route('/forum-ranking')
@login_required
def forum_ranking():
    return render_template('features/forum_ranking.html')

# 6. 感兴趣的内容推荐
@app.route('/recommendations')
@login_required
def recommendations():
    return render_template('features/recommendations.html')

# 7. 相关资料下载入口指引
@app.route('/downloads')
@login_required
def downloads():
    return render_template('features/downloads.html')

# 8. 实时语音转文字、多语言翻译
@app.route('/translation')
@login_required
def translation():
    return render_template('features/translation.html')

# 9. 智能区分发言人会议要点自动总结
@app.route('/speaker-summary')
@login_required
def speaker_summary():
    return render_template('features/speaker_summary.html')

# 10. AI智能分析和总结
@app.route('/ai-summary')
@login_required
def ai_summary():
    return render_template('features/ai_summary.html')

# 11. 用户数据安全与隐私保护
@app.route('/privacy')
@login_required
def privacy():
    return render_template('features/privacy.html')

if __name__ == '__main__':
    app.run(debug=True)