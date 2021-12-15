
# Capstone 1 Proposal

## Goal of Project:
The goal of this website is to make an advanced To Do list web app. Within the web, users can create a new board of each project, add lists of progress and each step under the list. The target users can be anyone who wants to manage their assignments or projects. (For the collab functions, I may add it if I have times)

## Data and API:
After I read through the Trello API, I think the most important elements for the database are users, boards, lists and cards. The basic data be looked like below:
![This is an image](/data.png)

Users table has information of username, password and board_id (refer to boards table).
Boards table has information of board name
Lists table has information of list name
Cards table has information of cards name, description, deadline.

_ _Haven’t found solutions to connect boards, lists and cards
The database may add more data based on the features that I want to add._ _


(Added)API:
OpenWeatherMap API, based on users location show current weather and 4-days weather

## User Flow:
Users have to signup/login first, and then they can see their existing boards or add a new board. After clicking on the board they want to see, the page will jump to the board page. Then users can adjust their lists and cards.
![This is an image](/user-flow.png)


