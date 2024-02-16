from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow, Schema
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
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

    game1 = Game()
    game2 = Game()
    
    db.session.add(wordAux)
    db.session.add(userAux)
    db.session.add(game1)
    db.session.add(game2)

    db.session.commit()
    print('Database seeded!')


# Routes...
@app.route("/word/add", methods=['POST'])
@jwt_required()
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


# Game logic...
@app.route("/game/create", methods=['POST'])
@jwt_required()
def create_game():
    user = get_user(get_jwt_identity())

    # Checks of the player it's playing another game already...
    if user_in_N_games(user) > 1:
        return message("You're already playing a game..."), 401
                       

    # Must check if the player it's already playing...
    game = Game()
    db.session.add(game)
    db.session.commit()
    db.session.add(
        Plays (
            id_game=game.id_game,
            id_user=user.id
        )
    )

    db.session.commit()

    return message('Game created!'), 201
    

@app.route("/game/in", methods=['POST'])
@jwt_required()
def get_in_game():
    user = get_user(get_jwt_identity())
    if user_in_N_games(user) > 0:
        return message("You're already playing a game..."), 401
    
    db.session.add(Plays(
            id_user=user.id, 
            id_game=int(request.form['id_game'])
        )
    )
    db.session.commit()

    return message('Player added!'), 201


def create_hand():
    print('TODO')


@app.route("/try/add", methods=['POST'])
@jwt_required()
def add_try():
    user = get_user(get_jwt_identity())
    actualGame = db.session.query(Game).join(Plays).filter(
        Plays.id_user == user.id,
        Game.finished == False
    ).first()
    actualHand = Hand.query.filter_by(finished=False, id_game=actualGame.id_game).first()

    if actualGame and actualHand:
        tryAux = Try (
            hand_id = actualHand.id,
            writer = user.id,
            content = request.form['content']
        )
        db.session.add(tryAux)
        db.session.commit()
        return message('Try added succesfully!'), 201
    else:
        return message('There is no game or hand to add a try...'), 404


# Database Models
class Word(db.Model):
    __tablename__ = 'word'
    word = Column(String, primary_key=True)
    meaning = Column(String)
    hands = db.relationship('Hand', backref='word', lazy=True)


class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    lastname = Column(String)
    alias = Column(String)
    email = Column(String, unique=True, nullable=False)
    password = Column(String)
    games = db.relationship('Game', backref='user', lazy=True)
    hands = db.relationship('Hand', backref='user', lazy=True)
    trys = db.relationship('Try', backref='user', lazy=True)
    votes = db.relationship('Vote', backref='user', lazy=True)
    plays = db.relationship('Plays', backref='user', lazy=True)


class Game(db.Model):
    __tablename__ = "game"
    id_game = Column(Integer, primary_key=True)
    started_at = Column(DateTime, server_default=func.now())
    finished = Column(Boolean, default=False)
    winner = Column(Integer, ForeignKey('user.id'), nullable=True)
    players = db.relationship('Plays', backref='game', lazy=True)
    hands = db.relationship('Hand', backref='game', lazy=True)


class Hand(db.Model):
    __tablename__ = 'hand'
    id_hand = Column(Integer, primary_key=True)
    id_word = Column(String, ForeignKey('word.word'), nullable=False)
    id_leader = Column(Integer, ForeignKey('user.id'), nullable=False)
    id_game = Column(Integer, ForeignKey('game.id_game'), nullable=False)
    started_at = Column(DateTime, nullable=True)
    finished = Column(Boolean, default=False)
    trys = db.relationship('Try', backref='hand', lazy=True)


class Try(db.Model):
    __tablename__ = 'Try'
    id_try = Column(Integer, primary_key=True)
    id_hand = Column(Integer, ForeignKey('hand.id_hand'), nullable=False)
    writer = Column(Integer, ForeignKey('user.id'), nullable=False)
    content = Column(String, nullable=False)
    is_right = Column(Boolean, default=False)
    is_the_original = Column(Boolean, default=False)
    votes = db.relationship('Vote', backref='try', lazy=True)

    __table_args__ = (
        db.UniqueConstraint('id_hand', 'writer', name='unique_hand_writer'),
    )


class Vote(db.Model):
    __tablename__ = 'Vote'
    id_try = Column(Integer, ForeignKey('Try.id_try'), primary_key=True)
    id_user = Column(Integer, ForeignKey('user.id'), primary_key=True)


class Plays(db.Model):
    __tablename__ = 'plays'
    id_game = Column(Integer, ForeignKey('game.id_game'), primary_key=True)
    id_user = Column(Integer, ForeignKey('user.id'), primary_key=True)


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


# Check if...
def user_in_N_games(user: User):
    return db.session.query(Game).join(Plays).filter(
            Game.finished == False,
            Plays.id_user == user.id
        ).count()
    

# Functions...
def message(msg: str):
    return jsonify(message=msg)


def get_user(email: str):
    return User.query.filter_by(email=email).first()


def get_user_game(user: User):
    return db.query(Game).join(Plays).filter(
        Game.finished == False,
        Plays.id_user == user.id
    ).first()

if __name__ == "__main__":
    app.run()