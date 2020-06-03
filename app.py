from flask import Flask, render_template, jsonify, request, url_for
import json
import os
import pandas as pd
from retrieve_definition import retrieve_definition


# Create Flask app
app = Flask(__name__)


# Creating the main route for the api page
@app.route('/', methods=['GET', 'POST'])
def home():
    """ Home page of site """
    message = "You are now home"
    return render_template('base.html', message=message)


# Creating a serach route to access retrieve_definition function
@app.route('/search', methods=['GET', 'POST'])
def wiki_search():
    """Accessing wikipedia's api with 
    retrieve_definition function"""
    searchword = request.args.get('word')
    data = retrieve_definition(searchword)
    return data

# Create a route to return heatmap
@app.route('/heatmap', methods=['GET', 'POST'])
def calender_heatmap():
    """Returning the plotly visual in html form"""
     data = request.get_json()

    """ Input from user. Each field is required for the DataFrame"""
    host_is_superhost = data['host_is_superhost']
    latitude = data['latitude']
    longitude = data['longitude']
    property_type = data['property_type']
    accommodates = data['accommodates']
    bathrooms = data['bathrooms']

     """ Place for default values if any are used. """

    """ Features dictionary for model """
    features = {'host_is_superhost': host_is_superhost,
                'latitude': latitude,
                'longitude': longitude,
                'property_type': property_type,
                'accommodates': accommodates,
                'bathrooms': bathrooms}

    predict_data = pd.DataFrame(features, index=[1])

    fig.write_html("templates/heatmap.html")
    return render_template('heatmap.html')


@app.route('/delete_map')
def delete():
    os.remove('templates/heatmap.html')


if __name__ == '__main__':
    app.run(debug=True)
