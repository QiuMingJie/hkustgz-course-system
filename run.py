#!/usr/bin/env python3
from app import app
from app import db
from random import randint
from app.models import Review, Course, Student, User
import sys

debug = False
for arg in sys.argv:
    if arg == '-d':
        debug = True

def start():
    if debug:
        with app.app_context():
            db.create_all()
        app.run(port=2021, threaded=True, host='0.0.0.0')
    else:
        app.run(port=3000, threaded=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1433, debug='-d' in __import__('sys').argv)
