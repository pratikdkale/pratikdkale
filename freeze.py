# freeze.py
from app import app                 # make sure this imports your Flask app = Flask(__name__)
from flask_frozen import Freezer

app.config['FREEZER_DESTINATION'] = 'docs'     # GitHub Pages will serve from /docs
app.config['FREEZER_RELATIVE_URLS'] = True     # makes /static and link paths relative

freezer = Freezer(app)

# If you have dynamic routes with params, register generators here.
# For simple pages (/  /about  /blogs), nothing extra is needed.

if __name__ == "__main__":
    freezer.freeze()
