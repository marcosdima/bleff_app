from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow, Schema
from sqlalchemy import Column, Integer, String, Float, Boolean
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
import os

app = Flask(__name__)
app.debug = True

# db
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "bleff.db")}'
app.config['JWT_SECRET_KEY'] = 'SECRET' # Change later...


ma = Marshmallow(app)
db = SQLAlchemy(app)
jwt = JWTManager(app)


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
                    word = "HOME",
                    meaning = "A place where you live."
                )
    userAux = User (
                    name = "Marcos",
                    lastname = "Di Matteo",
                    email = "marcosdimatteo@gmail.com",
                    password = "1234"
                )
    db.session.add(wordAux)
    db.session.add(userAux)

    db.session.commit()
    print('Database seeded!')


# Routes...
@app.route("/word/add", methods=['POST'])
@jwt_required
def add_word():
    # Check if it's a json...
    if request.is_json:
        word = request.json['word']
        meaning = request.json['meaning']
    else:
        word = request.form['word']
        meaning = request.form['meaning']

    word = word.upper()
    wordAux = Word.query.filter_by(word=word).first()

    if wordAux:
        return message(f"There is already a word '{word}' in the database..."), 401
    else:
        newWord = word
        db.session.add(Word(word=newWord, meaning=meaning))
        db.session.commit()    
        return message(f"{word} added succesfully!"), 201


@app.route("/words", methods=['GET'])
def words():
    words_list = Word.query.all()
    return jsonify(words_schema.dump(words_list)) 


@app.route("/users", methods=['GET'])
def users():
    users_list = User.query.all()
    return jsonify(users_schema.dump(users_list))


@app.route("/register", methods=['POST'])
def register():
    email = request.form['email']
    exists = User.query.filter_by(email=email).first()

    # Check if already exists an user with that mail...
    if exists:
        return message("That mail already exists."), 409
    else:
        user = User (
                    email = request.form['email'],
                    name = request.form['name'],
                    lastname = request.form['lastname'],
                    password = request.form['password']
                )
        db.session.add(user)
        db.session.commit()
        return message("User created!"), 201


@app.route("/login", methods=['POST'])
def login():
    # Check if it's a json...
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']

    user = User.query.filter_by(email=email, password=password).first()

    if user:
        access_token = create_access_token(identity=email)
        return jsonify(message="Login succeeded!", access_token=access_token)
    else:
        return message("Bad email or password"), 401
        

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
    password = Column(String)


# Schema
class WordSchema(Schema):
    class Meta:
        fields = ('word', 'meaning')


class UserSchema(Schema):
    class Meta:
        fields = ('name', 'lastname', 'email')


word_schema = WordSchema()
words_schema = WordSchema(many=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)


# Functions...
def message(msg: str):
    return jsonify(message=msg)


if __name__ == "__main__":
    app.run()