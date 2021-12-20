
# Capstone 1 Proposal

## Goal of Project:
The goal of this website is to make an advanced To Do list web app. Within the web, users can create a new board of each project, add lists of progress and each step under the list. Within the list, user can move their steps. The target users can be anyone who wants to manage their assignments or projects. 

## Data and API:
The most important elements for the database are users, boards, lists and cards. The basic data be looked like below:
![This is an image](/data2.png)

Users table has information of username, password, email, firstname, lastname, city and state.
Boards table has information of board name, archive(boolean value), users_id(refer to users table).
Lists table has information of list name, boards_id, users_id(refer to boards and users table).
Cards table has information of cards name, description, deadline, lists_id,boards_id, users_id (refer to lists,boards and users table).

API:
This web used OpenWeatherMap API, which shows user with his/her place's weather based on user's location. The location data are saved in users table.

## User Flow:
Users have to signup/login first, and then they can see their existing boards or add a new board. After clicking on the board they want to see, the page will jump to the board page. User can add, delete/archive their boards. Users can also adjust their lists and cards.
![This is an image](/user-flow.png)

## Web App Outlook:

Main Page
![This is an image](/main.png)

Board Page
![This is an image](/board.png)

List Page
![This is an image](/list.png)
