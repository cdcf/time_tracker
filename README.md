Time Tracker app for Freelance
==============================

Code for my app to track my freelance activity when I am only selling worked days, regardless to tasks done within the
day. Purpose to create this app was that I only need to quickly calculate how many days I have been working in a
month by selecting days in an agenda without capturing all tasks done.
Possible improvements for this app would be to give the choice to either identify worked days and/or insert detailed
 tasks done within the day.

Requirements
------------

- Python 3.4
- virtualenv (or pyvenv if you are using Python 3.4)
- git

Setup
-----

**Step 1**: Clone the git repository

    $ git clone https://github.com/cdcf/time_tracker.git
    $ cd time_tracker

**Step 2**: Create a virtual environment.

For Linux, OSX or any other platform that uses *bash* as command prompt (including Cygwin on Windows):

    $ virtualenv venv
    $ source venv/bin/activate
    (venv) $ pip install -r requirements.txt

For Windows users working on the standard command prompt:

    > virtualenv venv
    > venv\scripts\activate
    (venv) > pip install -r requirements.txt

**Step 3**: Create an administrator user

    (venv) $ python manage.py adduser <your-email-address> <your-username>
    Password: <pick-a-password>
    Confirm: <pick-a-password>
    User <your-username> was registered successfully.

**Step 4**: Run the initial database migration:

    (venv) $ python manage.py db migrate -m "initial migration"
    (venv) $ python manage.py db upgrade
     
**Step 5**: Start the application:

    (venv) $ python manage.py runserver
     * Running on http://127.0.0.1:5000/
     * Restarting with reloader

Now open your web browser and type [http://localhost:5000](http://localhost:5000) in the address bar to see the
application running. If you feel adventurous click on the "Presenter Login" link on the far right of the navigation
bar and ensure the account credentials you picked above work.
If you need to add non-admin users, you can now do it from within the app.
