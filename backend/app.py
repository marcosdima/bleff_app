import os
import random
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow, Schema
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import validates
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

app = Flask(__name__)
app.debug = True

# db
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "bleff.db")}'
app.config['JWT_SECRET_KEY'] = 'SECRET' # Change later...


ma = Marshmallow(app)
db = SQLAlchemy(app)
jwt = JWTManager(app)


# Constant
WORD_CHOICES = 5
MIN_USERS = 2
MAX_USERS = 5
MINUTES_TO_WRITE = 20


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
    userAux2 = User (
        name = "Marcos",
        lastname = "Di Matteo",
        email = "marcosdimatteo2@gmail.com",
        password = "1234"
    )

    db.session.add(wordAux)
    db.session.add(userAux)
    db.session.add(userAux2)

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


@app.route("/word/<id_word>")
def get_word(id_word):
    # Check if it's a json...
    word = Word.query.filter_by(word=id_word).first()

    if word:
        return jsonify(word_schema.dump(word)), 200
    else:
        return message("That word doesn't exists..."), 404


@app.route("/words", methods=['GET'])
def words():
    words_list = Word.query.all()
    return jsonify(words_schema.dump(words_list)) 


@app.route("/users", methods=['GET'])
def users():
    users_list = User.query.all()
    return jsonify(users_schema.dump(users_list))


@app.route("/max_users", methods=['GET'])
def get_max_users():
    return jsonify(max_users=MAX_USERS), 200


@app.route("/games", methods=['GET'])
def games_data():
    games = Game.query.filter_by(finished=False).all()
    gamesSchemas = games_schemas.dump(games)
    for game in gamesSchemas:
        game['users'] = Plays.query.filter_by(id_game=game['id_game']).count()
    return jsonify(gamesSchemas), 200
    

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


@app.route("/test")
def test():
    new_try = Try(id_hand=2, writer=2, content='Contenido del intento', is_right=False, is_the_original=False)

    # Agregar el nuevo registro a la sesión
    db.session.add(new_try)

    # Confirmar la transacción para insertar el nuevo registro en la base de datos
    db.session.commit()
    return jsonify("Test!")


# Game logic...
@app.route("/game/create", methods=['POST'])
@jwt_required()
def create_game():
    user = get_user(get_jwt_identity())

    # Checks of the player it's playing another game already...
    if user_in_N_games(user.id) >= 1:
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

    return jsonify({ 'id_game': game.id_game }), 201
    

@app.route("/game/in", methods=['POST'])
@jwt_required()
def get_in_game():
    user = get_user(get_jwt_identity())
    if user_in_N_games(user.id) > 0:
        return message("You're already playing a game..."), 401

    id_game = int(request.form['id_game'])

    db.session.add(Plays(
            id_user=user.id, 
            id_game=id_game
        )
    )
    db.session.commit()

    return {}, 201


@app.route("/game/start", methods=['POST'])
@jwt_required()
def start_game():
    user = get_user(get_jwt_identity())
    id_game = get_user_game(user.id)

    if not id_game:
        return message("You're not in a game..."), 404

    usersInGame = N_users_in_game(id_game)

    if (usersInGame < MIN_USERS):
        return message(f"You need {MIN_USERS - usersInGame} more users..."), 403

    create_hand(id_game=id_game)

    hand = db.session.query(Hand).filter(Hand.finished==False, Hand.id_game==id_game).first()

    # If there are at least 3 players in game and can create a hand (There is no hand unfinished)
    if (hand.id_leader == user.id and not hand.id_word):
        return jsonify(words=get_words(id_game=id_game)), 202
    else:
        return message("Just Waiting..."), 200


def create_hand(id_game: int):
    created = False

    hands = Hand.query.filter(Hand.id_game==id_game, Hand.finished==False).first()

    # There is a hand unfinished...
    if hands:
        return created

    hand = Hand(
            id_leader = get_next_leader(id_game),
            id_game = id_game
        )
    db.session.add(hand)
    db.session.commit()

    created = True

    return created


@app.route("/hand")
@jwt_required()
def get_hand():
    user = get_user(get_jwt_identity())
    id_game = get_user_game(user.id)
    hand = get_hand(id_game=id_game)

    if id_game and hand and hand.started_at:
        return jsonify(hand_schema.dump(hand)), 200
    elif id_game and hand:
        return message("Waiting for the leader to select the word..."), 403
    elif id_game:
        return message("The game doesn't start yet..."), 403
    else:
        return message("This user aren't playing..."), 404


@app.route("/hand/start", methods=['POST'])
@jwt_required()
def start_hand():
    user = get_user(get_jwt_identity())
    id_game = get_user_game(user.id)
    hand = get_hand(id_game=id_game)
    word = request.form['word'].upper()

    isAValidWord = Word.query.filter_by(word=word).first()

    #TODO It should create the try that represents the right answer.

    if hand and user.id == hand.id_leader and isAValidWord:
        hand.started_at = func.now()
        hand.id_word = word
        db.session.commit()
        return message('Hand started succesfully!'), 200
    elif not isAValidWord:
        return message(f"The word '{word}' doesn't exists in our database..."), 404
    elif not hand:
        return message("The game doesn't start yet..."), 403
    else:
        return message("You're not the leader of this hand..."), 403


@app.route("/try/add", methods=['POST'])
@jwt_required()
def add_try():
    user = get_user(get_jwt_identity())
    actualGame = db.session.query(Game).join(Plays).filter(
        Plays.id_user == user.id,
        Game.finished == False
    ).first()
    actualHand = Hand.query.filter_by(finished=False, id_game=actualGame.id_game).first()

    if actualHand and not actualHand.id_word:
        return message("The word wasn't assigned yet..."), 404

    tryExists = Try.query.filter_by(id_hand=actualHand.id_hand, writer=user.id).first()
    
    if actualGame and actualHand and not tryExists:
        tryAux = Try (
            id_hand = actualHand.id_hand,
            writer = user.id,
            content = request.form['content']
        )
        db.session.add(tryAux)
        db.session.commit()
        return message('Try added succesfully!'), 201
    elif tryExists:
        return message('You already sended a Try...'), 200
    else:
        return message('There is no game or hand to add a try...'), 404


@app.route("/trys")
@jwt_required()
def get_trys():
    user = get_user(get_jwt_identity())
    id_game = get_user_game(user.id)
    hand = get_hand(id_game)

    started_at = hand.started_at
    writing_time = timedelta(minutes=MINUTES_TO_WRITE)

    trys = Try.query.filter_by(id_hand=hand.id_hand).all()

    # There is time to add trys...
    if (started_at + writing_time > now() and len(trys) < N_users_in_game(id_game=id_game)):
        timeLeft = started_at + writing_time - now()
        return message(f"Wait until the last player send its try... or {timeLeft.seconds // 60} minutes and {timeLeft.seconds % 60} seconds"), 200

    if trys:
        return jsonify(try_schemas.dump(trys)), 200
    else:
        return message("No trys founded..."), 404


@app.route("/try/vote", methods=['POST'])
@jwt_required()
def vote_try():
    user = get_user(get_jwt_identity())
    id_try = int(request.form['try'])
    vote = Vote(
        id_user=user.id,
        id_try=id_try
    )
    db.session.add(vote)
    db.session.commit()


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
    id_word = Column(String, ForeignKey('word.word'), nullable=True)
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


    @validates('id_hand')
    def hand_not_finished(self, key, id_hand):
        ''' Checks if the id_hand it's from a finished hand. '''
        hand = Hand.query.filter_by(id_hand=id_hand).first()

        if hand.finished:
            raise ValueError("The hand is finished, you can't add trys anymore.")
        return id_hand


    @validates('writer')
    def writer_in_game(self, key, writer):
        ''' Checks if the player is playing the hand(id_hand) game. '''
        user_id_game = get_user_game(writer)
        hand = Hand.query.filter_by(id_hand=self.id_hand).first()
        if user_id_game != hand.id_game:
            raise ValueError("You aren't playing this hand!")
        return writer


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


class HandSchema(Schema):
    class Meta:
        fields = ('id_word', 'id_leader', 'started_at', 'finished')


class GameSchema(Schema):
    class Meta:
        fields = ('id_game', 'started_at', 'winner')


class TrySchema(Schema):
    class Meta:
        fields = ('id_try', 'content')


word_schema = WordSchema()
words_schema = WordSchema(many=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

hand_schema = HandSchema()

games_schemas = GameSchema(many=True)

try_schemas = TrySchema(many=True)


# Querys...
def user_in_N_games(id_user: int) -> int:
    return db.session.query(Game).join(Plays).filter(
            Game.finished == False,
            Plays.id_user == id_user
        ).count()


def user_was_N_times_leader(id_user: int, id_game: int) -> int:
    return User.query.join(Plays).join(Game).join(Hand).filter(
                Game.id_game == id_game,
                Hand.id_leader==id_user
            ).count()


def N_users_in_game(id_game: int) -> int:
    return db.session.query(Plays).filter(
                Plays.id_game == id_game
            ).count()


def get_user_game(id_user: int) -> int:
    return db.session.query(Plays.id_game).join(Game).filter(
        Plays.id_game == Game.id_game,
        id_user == Plays.id_user,
        Game.finished == False
    ).scalar()


def get_next_leader(id_game: int) -> int:
    users = User.query.join(Plays).join(Game).filter_by(id_game=id_game)

    minTimesLeader = user_was_N_times_leader(id_user=users[0].id, id_game=id_game)
    id_user = id_user=users[0].id

    for user in users:
        userWasNTimesLeader = user_was_N_times_leader(id_user=user.id, id_game=id_game)

        if (userWasNTimesLeader < minTimesLeader):
            id_user=user.id
            minTimesLeader = userWasNTimesLeader

    return id_user


def get_hand(id_game: int) -> Hand:
    return Hand.query.filter(
        Hand.id_game == id_game,
        Hand.finished == False
    ).first()


def get_words(id_game: int) -> list:
    wordsAlreadyPlayed = db.session.query(Hand.id_word).join(Game, Game.id_game == Hand.id_game).filter(Game.id_game == id_game).distinct().all()
    totalWords = db.session.query(Word.word).all()
    NPosibleWords = len(totalWords) - len(wordsAlreadyPlayed)
    
    # Extracting IDs from query results
    excluded_ids = [row[0] for row in wordsAlreadyPlayed]

    # Filtering the words that were already used...
    posibleWords = [row[0] for row in totalWords if row[0] not in excluded_ids]
    
    if NPosibleWords >= WORD_CHOICES:
        random.shuffle(posibleWords)
        return posibleWords[0:5]
    elif NPosibleWords > 0:
        return posibleWords
    else:
        print("There is no words left...")
        return []


def get_user(email: str) -> User:
    return User.query.filter_by(email=email).first()


# Functions...
def message(msg: str):
    return jsonify(message=msg)


def now():
    return datetime.utcnow()


if __name__ == "__main__":
    app.run()