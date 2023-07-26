from flask import Flask, render_template, request, redirect, session, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from controllers.quiz import generate_quiz
from common.db import get_connection, get_hash, get_salt, insert_user, authenticate, get_point, getcount, ranks
from difflib import SequenceMatcher


app = Flask(__name__)
app.secret_key = 'Your Secret Key'

@app.route('/')
def index():
    session.pop('USER', None)
    return render_template('index.html', flag=True, title='メインメニュー')

@app.route('/login')
def login():
    return render_template('login.html', title='ログイン')

@app.route('/login_route', methods=['POST'])
def login_route():
    user_name=request.form.get('username')
    password=request.form.get('password')
    session['USER']  = user_name
    print(user_name,password,"one")
    auth_result, count = authenticate(user_name, password)
    ranknow = ranks()
    num = 1
    if auth_result:
        error= 'ログイン成功!'
        user_name = user_name
        print(error)
        print(ranknow)
        return render_template('index.html', error=error, username=user_name, flag=False, title='メインメニュー', count=count, ranknow=ranknow)
    else:
        error='ユーザ名またはパスワードが違います。'
        print(error)
    input_data={'user_name':user_name, 'password':password}
    print(user_name,password,"ここ")
    return render_template('index.html', error=error, title='   メインメニュー', flag='True')


@app.route('/signup')
def signup():
    return render_template('signup.html', title='会員登録')

@app.route('/register', methods=['POST'])
def register():
    user_name = request.form.get('username')
    password = request.form.get('password')
    count = insert_user(user_name, password)
    if count == 1:
        msg = '登録が完了しました。引き続きログインにお進みください。'
        return render_template('index.html', msg=msg, flag=True, title='メインメニュー')
    else:
        error = '登録に失敗しました。もう一度、ニックネームやパスワードを変更してお試しください。'
        return render_template('index.html', error=error, flag=True, title='メインメニュー')

@app.route('/quiz', methods=['POST'])
def quiz():
    theme = request.form['theme']
    question, answer = generate_quiz(theme)
    print('checkpoint1')
    session['answer'] = answer
    return render_template('quiz.html', question=question, title='クイズ')

@app.route('/check_answer', methods=['POST'])
def check_answer():
    user_answer = request.form['user_answer']
    nowanswer = session.get('answer')
    print(f'checkpoint2{nowanswer}')

    similarity = SequenceMatcher(None, user_answer.lower(), nowanswer.lower()).ratio()
    print(f"ユーザーの答え：{user_answer}")
    print(f"模範解答：{nowanswer}")
    print(f"一致度：{similarity}")

    if similarity >= 0.5:
        result = "正解です！"
        point = get_point(session.get('USER'))
        print('checkpoint3')
    elif similarity >= 0.1:
        result = '惜しいです...なお、解答に不備があった場合には申し訳ございません。'
        print('checkpoint4')
    else:
        result = "間違いです。"
        print('checkpoint5')
    return render_template('result.html', result=result, answer=nowanswer, title='クイズ結果')

@app.route('/continue')
def point():
    user_name=session.get('USER')
    count = getcount(user_name)
    ranknow = ranks()
    return render_template('index.html', username=user_name, count=count, ranknow=ranknow)

if __name__ == '__main__':
    app.run(debug=True)
