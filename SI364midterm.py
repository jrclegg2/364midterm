###############################
####### SETUP (OVERALL) #######
###############################

## Import statements
# Import statements
import os
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, RadioField
from wtforms.validators import Required, Length
from flask_sqlalchemy import SQLAlchemy
import requests
import json
from credentials import key

## App setup code
app = Flask(__name__)
app.debug = True
app.use_reloader = True

## All app.config values
app.config['SECRET_KEY'] = "umich is an 16 awesome 20 place"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://jack:jack@localhost/jrcleggmidterm"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

## Statements for db setup (and manager setup if using Manager)
db = SQLAlchemy(app)


######################################
######## HELPER FXNS (If any) ########
######################################

# creates dict to be represented in html file from API request
def craftDict(form):
    dictData = {}
    song = form.song.data
    artist = form.artist.data
    rating = int(form.rating.data)
    requestURL = "http://api.musixmatch.com/ws/1.1/track.search"
    params = {'q_track' : song, 'q_artist' : artist, 'apikey' : key}
    requesting = requests.get(requestURL, params).text.encode('utf-8')
    jsonDict = json.loads(requesting)
    dictData['status'] = jsonDict['message']['header']['status_code']
    if jsonDict['message']['header']['status_code'] == 200:
        try:
            dictData['track'] = jsonDict['message']['body']['track_list'][0]['track']['track_name']
            dictData['rating'] = jsonDict['message']['body']['track_list'][0]['track']['track_rating']
            dictData['difference'] = abs(dictData['rating'] - rating)
            dictData['guessRating'] = rating
            dictData['artist'] =jsonDict['message']['body']['track_list'][0]['track']['artist_name']
        except:
            dictData['status'] = -1
    else:
        dictData['status'] = -1
    return dictData

# get, or create, a song instance from songs table
def get_or_create_song(song_name, song_artist):
    songCheck = Song.query.filter_by(name = song_name, artist = song_artist).first()
    if not songCheck:
        song = Song(name = song_name, artist = song_artist)
        db.session.add(song)
        db.session.commit()
        return song
    else:
        return songCheck
#get, or create, a user instance from users table
def get_or_create_user(user_name):
    userCheck = User.query.filter_by(name = user_name).first()
    if not userCheck:
        user = User(name = user_name)
        db.session.add(user)
        db.session.commit()
        return user
    else:
        return userCheck
# get, or create, a rating instance from ratings table
def get_or_create_rating(songID, userID, rating):
    ratingCheck = Ratings.query.filter_by(songID = songID, userID = userID).first()
    # rating never been entered
    if not ratingCheck:
        rating = Ratings(songID = songID, userID = userID, rating = rating)
        db.session.add(rating)
        db.session.commit()
        return rating
    # if user has submitted rating for that song, flash error
    else:
        flash ("You've already rated this!")
        return ratingCheck
##################
##### MODELS #####
##################

class Name(db.Model):
    __tablename__ = "names"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64))

    def __repr__(self):
        return "{} (ID: {})".format(self.name, self.id)

# songs table with columns ID, name, artist
class Song(db.Model):
    __tablename__ = "songs"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    artist = db.Column(db.String(64))
    ratings = db.relationship('Ratings', backref = 'Song')
    def __repr__(self):
        return "{} by {}".format(self.name, self.artist)

#users table with columns ID, name
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    ratings = db.relationship('Ratings', backref = 'User')
    def __repr__(self):
        return "Name: {}, ID: {}".format(self.name, self.id)

# ratings table with columns ID, songID, userID, and rating
class Ratings(db.Model):
    __tablename__ = "ratings"
    id = db.Column(db.Integer, primary_key = True)
    songID = db.Column(db.Integer, db.ForeignKey('songs.id'))
    userID = db.Column(db.Integer, db.ForeignKey('users.id'))
    rating = db.Column(db.Integer)
    def __repr__(self):
        return "Rating from user {} for song {}".format(self.userID, self.songID)


### URL API: https://developer.musixmatch.com/documentation/api-reference/track-search

###################
###### FORMS ######
###################

class NameForm(FlaskForm):
    name = StringField("Please enter your name.",validators=[Required()])
    submit = SubmitField()

class RatingForm(FlaskForm):
    song = StringField("Enter a song: ", validators = [Required()])
    artist = StringField("Enter the artist: ", validators = [Required()])
    rating = StringField("What do you rate it 1-100? ", validators = [Required()])
    name = StringField("What should your username be?", validators = [Required()])
    submit = SubmitField()
    # username field does not include spaces
    def validate_name(self, field):
        if len(field.data.split(' ')) > 1:
            raise ValidationError("Username must be one word!!")
    # rating field is an integer between 1 and 100, inclusive
    def validate_rating(self, field):
        try:
            if (int(field.data) <= 0) or (int(field.data) > 100):
                raise ValidationError("Rating must be between 1 and 100, inclusive!")
        except:
            raise ValidationError("Rating must be an integer between 1 and 100!")

class ViewForm(FlaskForm):
    type = RadioField("Are you searching by username or song?", choices = [('username', 'Username'), ('song', 'Song')], validators = [Required()])
    query = StringField("Enter the username or song: ", validators = [Required()])
    submit = SubmitField()

###### VIEW FXNS ######
#######################

@app.route('/', methods = ['GET', 'POST'])
def home():
    form = RatingForm(request.form)
    # if user entered a form
    if request.method == "POST" and form.validate_on_submit():
        jsonDict = craftDict(form)
        ratings = Ratings.query.all()
        tupData = []
        # create ratings tuples
        for rank in ratings:
            song = Song.query.filter_by(id = rank.songID).first()
            tupleInfo = (rank.rating, song.name)
            tupData.append(tupleInfo)
        # if API search was successful
        if jsonDict['status'] == 200:
            song = get_or_create_song(jsonDict['track'], jsonDict['artist'])
            user = get_or_create_user(form.name.data)
            get_or_create_rating(song.id, user.id, form.rating.data)
            return render_template('songdata.html', dict = jsonDict, data = tupData, working = True)
        # if api search wasn't successful
        else:
            return render_template('songdata.html', dict = jsonDict, working = False)
    # if user hasn't entered a form, or form wasn't validated
    else:
        errors = [v for v in form.errors.values()]
        if len(errors) > 0:
            flash("!!!! ERRORS IN FORM SUBMISSION - " + str(errors))
        form = RatingForm()
        return render_template('home.html',form = form)

@app.route('/displayratings', methods = ['GET', 'POST'])
def display_ratings():
    try:
        # try checking if what the user entered was not blank, if an error skip to 'except block'
        if (type(request.args.get('type')) != type(None)) and (type(request.args.get('query')) != type(None)):
            if request.args.get('type') == 'username':
                user = User.query.filter_by(name = request.args.get('query')).first()
                ratings = Ratings.query.filter_by(userID = user.id).all()
                listRatings = []
                for rank in ratings:
                    song = Song.query.filter_by(id = rank.songID).first()
                    tupleData = (rank.rating, song.name)
                    listRatings.append(tupleData)
                return render_template("displayuserratings.html", data = listRatings, username = user.name)
            if request.args.get('type') == 'song':
                song = Song.query.filter_by(name = request.args.get('query')).first()
                ratings = Ratings.query.filter_by(songID = song.id).all()
                listRatings = []
                for rank in ratings:
                    user = User.query.filter_by(id = rank.userID).first()
                    tupleData = (rank.rating, user.name)
                    listRatings.append(tupleData)
                return render_template("displaysongratings.html", data = listRatings, song = song.name)
        else:
            flash ("Something is wrong with your fields! Either you didn't enter everything EXACTLY (case sensitive), or the song/username doesn't exist in our database yet...")
            form = ViewForm()
            return redirect(url_for('search_ratings'))
    # if user screws up the form, print message and try again
    except:
        flash ("Something is wrong with your fields! Either you didn't enter everything EXACTLY (case sensitive), or the song/username doesn't exist in our database yet...")
        form = ViewForm()
        return redirect(url_for('search_ratings'))

# show search ratings form
@app.route('/searchratings')
def search_ratings():
    form = ViewForm()
    return render_template('allratings.html', form = form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


## Code to run the application...

# Put the code to do so here!
if __name__ == '__main__':
    db.create_all() # Will create any defined models when you run the application
    app.run(use_reloader=True,debug=True) # The usual
# NOTE: Make sure you include the code you need to initialize the database structure when you run the application!
