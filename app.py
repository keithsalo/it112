from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

formData = {}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
with app.app_context():
    db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Thing %r>' % self.id


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/game', methods=['GET', 'POST'])
def game():
    if request.method == 'POST':
        name = request.form.get("user")
        colors = request.form.get("color")
        digit = request.form.get("number")

        return (f"Hi {name}, you selected the color  {colors} and the number  {digit}.  You are lucky! Play the Lotto!")

    return render_template('game.html')


if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
