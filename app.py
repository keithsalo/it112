#!/usr/local/bin/python3

from flask import Flask, render_template, request, redirect, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests
import json

# formData = {}


# convert datetime str to obj a
def convert(date_time):
    format = '%b %d %Y %I:%M%p'  # The format
    datetime_str = datetime.datetime.strptime(date_time, format)


# convert datetime str to obj b
my_date_string = "Mar 11 2011 11:31AM"
datetime_object = datetime.strptime(my_date_string, '%b %d %Y %I:%M%p')


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
with app.app_context():
    db = SQLAlchemy(app)

date_bug_fix = datetime(2012, 3, 3, 10, 10, 10)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Thing %r>' % self.id

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'content': self.content,
            'date_created': self.date_created
        }


# API call from all data in  database


@app.get('/api/grocery_list')
def grocery_list():
    # return db query results as a JSON list
    return jsonify([grocery_list.serialize for grocery_list in Todo.query.all()])

# route to add to list in  database


# API route to add to db
# add only id and content in postman ex. {"id": 19, "content": "adding item"}


@app.post('/api/groceries')
def add_list():
    data = request.get_json()

    try:
        content = request.get_json()['content']
        new_item = Todo(content=content)
        db.session.add(new_item)
        db.session.commit()
        return jsonify({"status": "success"})
    except:
        return app.response_class(response={"status": "failure"}, status=500, mimetype='application/json')


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


@app.route('/detail/<int:id>')
def detail(id):
    item = Todo.query.get_or_404(id)

    return jsonify(item.serialize)


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

# collapsed if blocks
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
# end collapse
    return render_template('game.html')


@app.route('/api/data')
def api_data():
    url = "https://data.seattle.gov/resource/2khk-5ukd.json"
    try:
        result = requests.get(url)
        # since result is already JSON, it shouldn't be serialized again
        response = app.response_class(
            response=result.text,
            status=200,
            mimetype='application/json'
        )
        return response
    except:
        return jsonify({"error": f"Unable to get {url}"})


if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
