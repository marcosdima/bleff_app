from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow, Schema
from sqlalchemy import Column, Integer, String, Float, Boolean
import os

app = Flask(__name__)

# db
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "bleff.db")}'
db = SQLAlchemy(app)

# Marshmallow
ma = Marshmallow(app)

# Commands...
@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database created...')


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database dropped...')


@app.cli.command('db_seed')
def db_seed():
    wordAux = Word (
                    word = "Home",
                    meaning = "A place where you live."
                )
    userAux = User(
                    name = "Marcos",
                    lastname = "Di Matteo",
                    email = "marcosdimatteo@gmail.com"
                )
    db.session.add(wordAux)
    db.session.add(userAux)

    db.session.commit()
    print('Database seeded!')

# Routes...
@app.route("/")
def hello():
    return "Hello world!"


@app.route("/variable/<string:name>")
def variable(name: str):
    return f"Hello {name}!"


@app.route("/words", methods=['GET'])
def words():
    words_list = Word.query.all()
    result = words_schema.dump(words_list)
    return jsonify(result) 

# db.Model
class Word(db.Model):
    __tablename__ = 'word'
    word = Column(String, primary_key=True)
    meaning = Column(String)


class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    lastname = Column(String)
    email = Column(String)


# Schema
class WordSchema(Schema):
    class Meta:
        fields = ('word', 'meaning')

class UserSchema(Schema):
    class Meta:
        fields = ('name', 'lastname', 'email')

word_schema = WordSchema()
words_schema = WordSchema(many=True)

if __name__ == "__main__":
    app.run(debug=True)