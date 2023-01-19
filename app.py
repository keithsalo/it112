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


# @app.route('/')
# def index():
#     return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        item_content = request.form['content']
        new_item = Todo(content=item_content)

        try:
            db.session.add(new_item)
            db.session.commit()
            return redirect('/')

        except:
            return 'There was an issue adding to list'

    else:
        items = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', items=items)


@app.route('/delete/<int:id>')
def delete(id):
    item_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting item from list'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    item = Todo.query.get_or_404(id)

    if request.method == 'POST':
        item.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your item'
    else:
        return render_template('update.html', item=item)


@app.route('/game', methods=['GET', 'POST'])
def game():
    fortune = None

    if request.method == 'POST':
        color = request.form.get("color")
        number = request.form.get("number")

        if color == "red":
            if number == "1":
                fortune = "Rainy"
            elif number == "2":
                fortune = "Sunny"
            elif number == "3":
                fortune = "Grim"
            elif number == "4":
                fortune = "Unclear"

        if color == "yellow":
            if number == "1":
                fortune = "Great"
            elif number == "2":
                fortune = "Excellent"
            elif number == "3":
                fortune = "Not Good"
            elif number == "4":
                fortune = "Hazy"

        if color == "blue":
            if number == "1":
                fortune = "Swell"
            elif number == "2":
                fortune = "Not Good bro"
            elif number == "3":
                fortune = "Cloudy"
            elif number == "4":
                fortune = "Misty"

        if color == "green":
            if number == "1":
                fortune = "Stormy"
            elif number == "2":
                fortune = "Foggy"
            elif number == "3":
                fortune = "Smelly"
            elif number == "4":
                fortune = "Fantastic"

        return render_template('game.html', user=request.form.get("user"), fortune=fortune)

    return render_template('game.html')

    # database route test


# @app.route('/database', methods=['POST', 'GET'])
# def database():
#     if request.method == 'POST':
#         item_content = request.form['content']
#         new_item = Todo(content=item_content)

#         try:
#             db.session.add(new_item)
#             db.session.commit()
#             return redirect('/database')

#         except:
#             return 'There was an issue adding to list'

#     else:
#         items = Todo.query.order_by(Todo.date_created).all()
#         return render_template('database.html', items=items)


# @app.route('/database/delete/<int:id>')
# def delete(id):
#     item_to_delete = Todo.query.get_or_404(id)

#     try:
#         db.session.delete(item_to_delete)
#         db.session.commit()
#         return redirect('/database')
#     except:
#         return 'There was a problem deleting item from list'


# @app.route('/database/update/<int:id>', methods=['GET', 'POST'])
# def update(id):
#     item = Todo.query.get_or_404(id)

#     if request.method == 'POST':
#         item.content = request.form['content']
#         try:
#             db.session.commit()
#             return redirect('/database')
#         except:
#             return 'There was an issue updating your item'
#     else:
#         return render_template('update.html', item=item)
    # end route test
if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
