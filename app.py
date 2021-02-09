# Import dependencies
from flask import Flask, render_template
from flask_pymongo import flask_pymongo
import scraping

# Set up Flask
app = Flask(__name__)

# Connect to Mongo using PyMongo
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mars_app'
mongo = PyMongo(app)

# Define route for HTML page
@app.rout('/')
def index():
    mars = mongo.db.mars.find_one()
    return render_template('index.html', mars=mars)

    # Set up scraping route
    @app.route('/scrape')
    def scrape():

        # Assign a new variable that point to Mongo
        mars = mongo.db.mars

        # Create a variable that will hold newly scraped data
        mars_data = scraping.scrape_all()

        # Update the database
        # {} adds an empty JSON object
        # upsert=True tells Mongo to create a new document if one doesn't
        # already exist
        mars.update({}, mars_data, upsert=True)

        # Navigate page back to / to see updated content
        return redirect('/', code=302)

        if __name__ == '__main__':
            app.run()

