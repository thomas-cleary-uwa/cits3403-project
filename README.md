# README: CITS3403 - Project - 2021 Semester 1

## Students
---
Thomas Cleary    - 21704985<br>
Michael LASTNAME - 22737938<br>
Jason LASTNAME   - 22732794<br>
Calvin LASTNAME  - 22509815<br>
<br>

## Purpose and Context
---
The purpose of the site we have branded "ezTrees" is to teach some basic theory about graph and tree data structures. 

All group members have a shared belief that there is not many easily locatable web resources that attempt to teach the theory of graphs and trees (no programming) at a beginner level. Therefore we believed this was a suitable topic for our project.

Early on we decided we wished to use a multi-choice quiz as the assessment method. (This was largely developed by Michael)

All group members were complete beginners in the field of web development at the start of the semester and have had to learn alot to develop this project. 
<br><br>

## Design and Development Process
---
<br>

### Initial Design Process:
Before commencing development of the project, the group met in a Zoom call on 28/03/21 to discuss
the theme and purpose we wanted the website to have. After some discussion we decided something within
the realm of teaching algorithms and data structures to a beginner level audience interested all of us.

The group met again, this time in person on the 08/04/21 to discuss:
- What topic we would like to cover
- What we want the different pages to look like
- What stastics we might track about users

During the meeting it was decided that we wanted to focus on an introduction to graphs/trees.
We also decided that we wanted to use a multi-choice quiz as our assessment mechanism. 
The group worked together on a whiteboard to draw sketches of what we wanted each user view to look like.

After this meeting each group member was assigned a task to work on over the next two weeks:
- Calvin -> Writing up the content for the learning page and creating some quiz questions
- Jason -> Implementing the index page we had designed on the whiteboard
- Michael -> Implementing the basic logic for the multi-choice quiz
- Thomas -> Setting up the backend for the website (Flask App, Flask-Login, Flask-Admin)

Our goal was to in two weeks time have a basic function Flask app that we could build upon.

<br><br>

### Initial Development Process
During these two weeks the foundation was laid for the website:
- A basic flask app was created
- The database schema was designed
- SQLalchemny and Flask-Migrate were used to implement the design schema
- Login and registration functionality was added with Flask-Login
- Admin access to the database was added with Flask-Admin

Our assessment mechanism made good progress:
- The quiz page showed a list of questions and could give feedback on the input answers

The content for the learning page was worked on.<br>
The index page for the home page of the website was worked on<br>
<br><br>

### Refining Page Structures
After we had learnt was capable with the Flask framework and other modules, we continued to further refine how each of the page views looked and what they presented.

Michael:
- Worked on furthering the quiz page by creating a menu bar to show and hide questions on the page

Thomas 
- Worked on enhancing the quiz feedback page and providing links in the users's profile to return to these feedback pages

Jason
- Worked on the beginning style of the website and further enhanced the index page

Calvin
- Worked on implementing the structure for the learning page

<br><br>

### Implementing a Consistent Style
After we were happy with how each page was structured we worked together to implement a consistent style for the website by implementing CSS in ezTrees.css. The group had a meeting where we worked together in writing the basic classes the site would use. After this session individual efforts were made by all further enhance the CSS stylings for the website.
<br><br>

### Learning Git
All group members were at best novices at using version control, and it took several weeks before it seemed as if all of us were comfortable with the concepts of pushing/pulling/branching/merging. Towards the end of the project though we had come to appreciate how easy it was for us to work collaboratively and get tasks done together.
<br><br>

## Architecture of the Web Application
---
The site is a Flask app that uses several extensions to provide further functionality
- Flask-login to manage user login/registration
- Flask-admin to allow the admin user to access the database for the app
- Flask-sqlalchemy to abstract the implementation of the database when accessing it
- Flask-migrate to implement database migrations when updating its schema
<br><br>

## Running Tests
---
MICHAEL ADD STUFF HERE
<br><br>


## Launching From localhost
---
THOMAS DESCRIBE HOW TO LAUNCH FROM LOCALHOST HERE
<br><br>


## Git Logs
---
The git logs have been included in a seperate file, "git-log.txt"
<br><br>

