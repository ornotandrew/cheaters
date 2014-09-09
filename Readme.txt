Contributors:
Andrew Van Rooyen
Darren Silke
Brendan Ball

Cheaters is a plagiarism detection system built with python on top of the Django framework to provide access through a web service.

Instructions:
Id db.sqlite3 doesn't exist run python manage.py syncdb before running the server
If changes to model was made then delete db.sqlite3 then run python manage.py syndb before running the server

Dependencies:
Django 1.6.5
Pygments 1.6

To install Django using pip:
pip install django

to install Pygments using pip:
pip install Pygments

to run the server:
python manage.py runserver <portnumber>
to broadcast to other machines:
python manage.py runserver 0.0.0.0 <portnumber>