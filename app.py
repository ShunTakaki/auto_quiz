from flask import Flask, render_template, request
from common.models.user import db
from controllers.auth import auth
from __init__ import create_app

app = create_app()

@app.route('/')
def index():
    title = 'index'
    return render_template('index.html', title=title)


if __name__ == '__main__':
    app.run(debug=True)