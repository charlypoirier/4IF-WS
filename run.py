# Before running with 
# $ flask run or $ python run.py
# make sure to run these:
# $ export export FLASK_APP=run.py
# $ export FLASK_ENV=development

from app import app

if __name__ == "__main__":
    app.run()

