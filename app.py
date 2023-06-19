from flask import Flask, render_template, request, redirect, session
from controllers.quiz import generate_quiz
from difflib import SequenceMatcher

app = Flask(__name__)
app.secret_key = 'Your Secret Key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz', methods=['POST'])
def quiz():
    theme = request.form['theme']
    question, answer = generate_quiz(theme)
    print('checkpoint1')
    session['answer'] = answer
    return render_template('quiz.html', question=question)

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
        print('checkpoint3')
    elif similarity >= 0.1:
        result='惜しいです...なお、解答に不備があった場合には申し訳ございません。'
        print('checkpoint4')
    else:
        result = "間違いです。"
        print('checkpoint5')
    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
