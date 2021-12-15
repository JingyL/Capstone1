# from trello import TrelloClient   
from flask import Flask, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, CollabBoard, CollabList
from forms import boardForm, listForm
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

# client = TrelloClient(
#     api_key='73ac60f9e2503794796f272568e34347',
#     api_secret='mysecret',
#     token='605ac71e5c83d0481157a2236c56eae0adadd20a545fec6f2e46a5b6a5bdb81a',
#     token_secret='1ccd9f6fce839f781ae4fd7564587e0d47e3923c112fb82b111376f358964571'
# )

connect_db(app)
db.create_all()

create_board_url = "https://api.trello.com/1/boards/"

@app.route("/", methods=['GET', 'POST'])
def root():
    """Homepage."""
    # response = requests.get("https://api.trello.com/1/members/me/boards",
    #     params = {
    #         "key":"73ac60f9e2503794796f272568e34347",
    #         "token":"605ac71e5c83d0481157a2236c56eae0adadd20a545fec6f2e46a5b6a5bdb81a"
    #     })
    # boards = response.json()
    boards = CollabBoard.query.all()
    return render_template('homepage.html', boards=boards)

##############################################################################
# Board
@app.route("/create-board", methods=['GET', 'POST'])
def createboard():
    """Create Board."""
    form = boardForm()
    if form.validate_on_submit():
        name = form.name.data
        response = requests.post("https://api.trello.com/1/boards/",
        params = {
            "key":"73ac60f9e2503794796f272568e34347",
            "token":"605ac71e5c83d0481157a2236c56eae0adadd20a545fec6f2e46a5b6a5bdb81a",
            "name":f"{name}"
        })
        res = response.json()
        boardID = res['id']
        new_board = CollabBoard(name=name,boardID=boardID )

        db.session.add(new_board)
        db.session.commit()
        # try:
        #     db.session.commit()
        # except IntegrityError:
        #     form.name.errors.append('Name taken.  Please pick another')
        #     return render_template('create-board.html', form=form)
        # flash('Successfully Created Board')

        # response = requests.post("https://api.trello.com/1/boards/",
        # params = {
        #     "key":"",
        #     "token":"",
        #     "name":f"{name}"
        # })
        board = CollabBoard.query.filter_by(name=name).first()
        return redirect(f'/board/{board.id}')
    return render_template('create-board.html', form=form)


@app.route("/board/<int:board_id>", methods=['GET', 'POST'])
def show_board(board_id):
    """Show Board, List."""
    board = CollabBoard.query.get_or_404(board_id)
    board_response = requests.get(f"https://api.trello.com/1/boards/{board.boardID}",
        params = {
            "key":"73ac60f9e2503794796f272568e34347",
            "token":"605ac71e5c83d0481157a2236c56eae0adadd20a545fec6f2e46a5b6a5bdb81a",
        })
    res = board_response.json()

    list_response = requests.get(f"https://api.trello.com/1/boards/{board.boardID}/lists",
        params = {
            "key":"73ac60f9e2503794796f272568e34347",
            "token":"605ac71e5c83d0481157a2236c56eae0adadd20a545fec6f2e46a5b6a5bdb81a",
        })
    list_res = list_response.json()


    return render_template('show-board.html', response=res, lists=list_res)

##############################################################################
# List
@app.route("/create-list/<boardID>", methods=['GET', 'POST'])
def createlist(boardID):
    """Create List."""
    form = listForm()
    if form.validate_on_submit():
        name = form.name.data
        response = requests.post(f"https://api.trello.com/1/boards/{boardID}/lists",
        params = {
            "key":"73ac60f9e2503794796f272568e34347",
            "token":"605ac71e5c83d0481157a2236c56eae0adadd20a545fec6f2e46a5b6a5bdb81a",
            "name":f"{name}"
        })
        b_id = CollabBoard.query.filter_by(boardID=boardID).first()
        new_list = CollabList(name=name,boards_id=b_id)

        db.session.add(new_list)
        db.session.commit()
        return redirect(f'/board/{b_id}')
    return render_template('create-list.html', form=form)
