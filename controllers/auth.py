from flask import Blueprint, render_template, url_for, flash, redirect, request
from common.models.user import User, db

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        mail = request.form['mail']
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(mail=mail).first()

        if user is None:
            new_user = User()
            new_user.mail = mail
            new_user.username = username
            new_user.set_pass(password)
            db.session.add(new_user)
            db.session.commit()
            flash('登録成功!')
            return redirect(url_for('auth.login'))
        else:
            flash('入力頂いたメールアドレスは既に使われております。別のメールアドレスをお試しください。')

        return render_template('signup.html')
