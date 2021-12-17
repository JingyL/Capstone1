from flask import Flask, redirect, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, CollabBoard, CollabList, CollabCard, User
from forms import boardForm, listForm, cardForm, UserForm, LoginForm
from sqlalchemy.exc import IntegrityError

import requests
import json


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///collab-app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


s_code = {"AL": "01", "AK": "54", "AZ": "02", "AR": "03", "CA": "04", 
        "CO": "05", "CT": "06", "DC": "08", "DE": "07", "FL": "09", "GA": "10", 
          "HI": "52", "ID": "11", "IL": "12", "IN": "13", "IA": "14", "KS": "15", 
          "KY": "16", "LA": "17", "ME": "18", "MD": "19",
          "MA": "20", "MI": "21", "MN": "22", "MS": "23", "MO": "24",
           "MT": "25", "NE": "26", "NV": "27", "NH": "28", "NJ": "29",
          "NM": "30", "NY": "31", "NC": "32", "ND": "33", "OH": "34", "OK": "35", 
          "OR": "36", "PA": "37", "RI": "38", "SC": "39",
          "SD": "40", "TN": "41", "TX": "42", "UT": "43", "VT": "44", "VA": "45", 
          "WA": "46", "WV": "47", "WI": "48", "WY": "49"}

##############################################################################
# register
# login
# logout
@app.route('/')
def inital_page():
    return render_template('initial.html')

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form. first_name.data
        last_name = form.last_name.data
        city =  form.city.data
        state = form.state.data
        new_user = User.register(username, password, email, first_name, last_name, city, state)
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken.  Please pick another')
            return render_template('register.html', form=form)
        session['user_id'] = new_user.id
        session['username'] = new_user.username
        return redirect(f"/{session['username']}/board")

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome Back, {user.username}!")
            session['username'] = user.username
            session['user_id'] = user.id
            return redirect(f"/{session['username']}/board")
        else:
            form.username.errors = ['Invalid username/password.']

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_user():
    session.pop('username')
    session.pop('user_id')
    flash("Goodbye!", "info")
    return redirect('/')

##############################################################################

@app.route("/<username>/board", methods=['GET', 'POST'])
def root(username):
    """Main page."""
    if 'username' not in session or username != session['username']:
        flash("Please login first!")
        return redirect('/')
    user = User.query.filter_by(username=username).first()
    city = user.city
    state = user.state
    state_code = s_code[state]
    weather_res = requests.get("http://api.openweathermap.org/data/2.5/weather",
        params = {
            "q": f"{city}, {state_code}, us",
            "appid":"c69ce1abd18c0eae09db094b5f772100"
        })
    weather = weather_res.json()
    boards = CollabBoard.query.filter_by(user_id=user.id).all()

    return render_template('homepage.html', boards=boards, weather=weather)

##############################################################################
# Board
@app.route("/<username>/create-board", methods=['GET', 'POST'])
def createboard(username):
    """Create Board."""
    if 'username' not in session or username != session['username']:
        flash("Please login first!")
        return redirect('/')
    form = boardForm()
    if form.validate_on_submit():
        name = form.name.data
        user_id = session['user_id']
        new_board = CollabBoard(name=name, user_id=user_id)
        db.session.add(new_board)
        db.session.commit()
        # board = CollabBoard.query.filter_by(name=name).first()
        return redirect(f'/{username}/board/{new_board.id}')
    return render_template('create-board.html', form=form)


@app.route("/<username>/board/<int:board_id>", methods=['GET', 'POST'])
def show_board(username,board_id):
    """Show Board, List."""
    if 'username' not in session or username != session['username']:
        flash("Please login first!")
        return redirect('/')
    # user = User.query.filter_by(username=username).first()
    user_id = session['user_id']
    board = CollabBoard.query.get(board_id)
    lists = [lists for lists in board.colists]
    return render_template('show-board.html', board=board, lists=lists)

##############################################################################
# List
@app.route("/<username>/board/<int:board_id>/create-list", methods=['GET', 'POST'])
def createlist(username,board_id):
    """Create List."""
    if 'username' not in session or username != session['username']:
        return redirect('/')
    form = listForm()
    if form.validate_on_submit():
        name = form.name.data
        user_id = session['user_id']
        new_list = CollabList(name=name,boards_id=board_id,user_id=user_id )
        # session['board_id'] = board_id
        db.session.add(new_list)
        db.session.commit()
        # curr_list = CollabList.query.filter_by(boards_id=board_id, name=name).first()
        # list_id = curr_list.json().id
        # session['list_id'] = list_id
        return redirect(f'/{username}/board/{board_id}')
    return render_template('create-list.html', form=form)

##############################################################################
# Card
@app.route("/<username>/board/<int:board_id>/list/<int:list_id>/create-card", methods=['GET', 'POST'])
def createcard(username, board_id, list_id):
    """Create Card."""
    if 'username' not in session or username != session['username']:
        flash("Please login first!")
        return redirect('/')
    form = cardForm()
    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        deadline = form.deadline.data
        user_id = session['user_id']
        new_card = CollabCard(name=name,description=description, deadline=deadline,lists_id=list_id, boards_id=board_id, user_id=user_id )

        db.session.add(new_card)
        db.session.commit()
        return redirect(f'/{username}/board/{board_id}')
    return render_template('create-card.html', form=form)