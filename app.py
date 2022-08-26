# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
import os

import numpy as np
import pandas as pd
from flask import Flask, render_template, request, url_for, flash, redirect

# Flask constructor takes the name of
# current module (__name__) as argument.
from methods import scrape_website_by_property_id
from model import Model

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
# @app.route('/')
# # ‘/’ URL is bound with hello_world() function.
# def hello_world():
#     return 'Hello World'
#

votes = 0


@app.route('/hello/<name>')
def hello_name(name):
    return 'Hello %s!' % name


@app.route('/success/<name>')
def success(name):
    return 'welcome %s' % name


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        return redirect(url_for('success', name=user))
    else:
        user = request.args.get('nm')
        return redirect(url_for('success', name=user))


messages = [{'title': 'Message One',
             'content': 'Message One Content'},
            {'title': 'Message Two',
             'content': 'Message Two Content'}
            ]


@app.route('/')
def index():
    return render_template('index.html', messages=messages)


@app.route('/create/', methods=['POST'])
def create_POST():
    title = request.form['title']
    content = request.form['content']

    if not title:
        flash('Title is required!')
    elif not content:
        flash('Content is required!')
    else:
        messages.append({'title': title, 'content': content})
        return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/create/', methods=['GET'])
def create():
    return render_template('create.html')


@app.route('/predict/', methods=['POST'])
def predict_POST():
    bedrooms = request.form['bedrooms']
    bathrooms = request.form['bathrooms']

    # title = request.form['title']
    # content = request.form['content']
    # if not title:
    #     title = 'default title'
    # if not content:
    #     content = 'default content'

    something_is_missing = False

    features_ui = [
        (bedrooms, 'bedrooms'),
        (bathrooms, 'bathrooms'),
    ]

    for required_field_name, required_field_value in features_ui:
        if not required_field_name:
            flash(f'{required_field_value.title()} is required!')
            something_is_missing = True

    if not something_is_missing:
        messages.append({'bedrooms': bedrooms, 'bathrooms': bathrooms})
        return redirect(url_for('index'))

    return render_template('predict.html')


@app.route('/predict/', methods=['GET'])
def predict():
    return render_template('predict.html')


@app.route('/scrape/', methods=['POST'])
def scrape_post():
    title = request.form['title']
    content = request.form['content']
    bedrooms = request.form['bedrooms']
    bathrooms = request.form['bathrooms']

    if not title:
        title = 'default title'

    if not content:
        content = 'default content'

    something_is_missing = False

    features_ui = [
        (bedrooms, 'bedrooms'),
        (bathrooms, 'bathrooms'),
    ]

    for required_field_name, required_field_value in features_ui:
        if not required_field_name:
            flash(f'{required_field_value.title()} is required!')
            something_is_missing = True

    if not something_is_missing:
        messages.append({'title': title, 'content': content})
        return redirect(url_for('index'))

    return render_template('predict.html')


@app.route('/scrape/', methods=['GET'])
def scrape():
    return render_template('scrape.html')


@app.route("/up", methods=["POST"])
def upvote():
    global votes
    votes = votes + 1
    return str(votes)


@app.route("/down", methods=["POST"])
def downvote():
    global votes
    if votes >= 1:
        votes = votes - 1
    return str(votes)


@app.route("/ajax_predict", methods=["POST"])
def ajax_predict():
    global votes
    if votes >= 1:
        votes = votes - 1

    bedrooms = request.form['bedrooms']
    bathrooms = request.form['bathrooms']

    features_ui = [
        (bedrooms, 'bedrooms'),
        (bathrooms, 'bathrooms'),
    ]

    for required_field_name, required_field_value in features_ui:
        if not required_field_name:
            flash(f'{required_field_value.title()} is required!')
            something_is_missing = True

    # if not something_is_missing:
    #     messages.append({'title': title, 'content': content})
    #     return redirect(url_for('index'))

    if False:
        data = 'data/data__0011_20220703_5000.csv'
        model_name = 'model__0011_20220703_5000'
        X_pred_np = np.array([[1, 2, 3, 4, 5, 6, 7, 8]])
    else:
        data = 'data/data__bedbath_5000.csv'
        model_name = 'model__bedbath_5000'
        X_pred_np = np.array([[bedrooms, bathrooms]])

    dataset = pd.read_csv(data, header=0)
    # dataset = dataset.drop(['property_age'],axis=1)
    dataset = dataset.dropna()

    dataset_columns = dataset.drop(['Price'], axis=1).columns

    model = Model(f'model/{model_name}.pkl')

    X = dataset.iloc[:, 1:]
    y = dataset.iloc[:, 0]
    model.train(X, y)
    model.save()

    X_pred = pd.DataFrame(X_pred_np, columns=dataset_columns)

    y_pred = model.predict(X_pred)[0]
    return "£{:.2f}".format(y_pred)


@app.route("/ajax_scrape", methods=["POST"])
def ajax_scrape():
    import requests

    global votes
    if votes >= 1:
        votes = votes - 1

    property_id = request.form['property_id']

    if not property_id:
        message = f'property_id is required!'
        flash(message)
        return message

    url = f'https://www.rightmove.co.uk/properties/{property_id}#/?channel=RES_BUY'

    requests_get = requests.get(url)
    html = requests_get.content

    if requests_get.status_code not in [200]:
        message = f'was not able to find property for {property_id}, please recheck (or use 126071096 as an example'
        flash(message)
        return message

    bathrooms, bedrooms = scrape_website_by_property_id(html)

    if False:
        data = 'data/data__0011_20220703_5000.csv'
        model_name = 'model__0011_20220703_5000'
        X_pred_np = np.array([[1, 2, 3, 4, 5, 6, 7, 8]])
    else:
        data = 'data/data__bedbath_5000.csv'
        model_name = 'model__bedbath_5000'
        X_pred_np = np.array([[bedrooms, bathrooms]])

    dataset = pd.read_csv(data, header=0)
    # dataset = dataset.drop(['property_age'],axis=1)
    dataset = dataset.dropna()

    dataset_columns = dataset.drop(['Price'], axis=1).columns

    model = Model(f'model/{model_name}.pkl')

    X = dataset.iloc[:, 1:]
    y = dataset.iloc[:, 0]
    model.train(X, y)
    model.save()

    X_pred = pd.DataFrame(X_pred_np, columns=dataset_columns)

    y_pred = model.predict(X_pred)[0]
    return "£{:.2f}".format(y_pred)


#
# # main driver function
# if __name__ == '__main__':
#     # run() method of Flask class runs the application
#     # on the local development server.
#     app.run()

# Calls the run method, runs the app on port 5000
# app.run(host='0.0.0.0', port='5000')
# Create the main driver function
port = int(os.environ.get("PORT", 5000))  # <-----
app.run(host='0.0.0.0', port=port)  # <-----
