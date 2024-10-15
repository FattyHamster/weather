import json
import os
import requests
import urllib
from flask import Flask, render_template, request, redirect, url_for, send_file
# from boto3 import resource
# from boto3.dynamodb.conditions import Attr, Key
import backend

from backend import get_api, filter_api, create_json_file, check_api

application = Flask(__name__)
# table = resource('dynamodb').Table('dynamo-python')


@application.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        user_input = request.form["location"]

        check = check_api(user_input)
        if check:
            filter_j = check
            # str_filter_j = json.dumps(filter_j)
            # table.put_item(Item=
            # {
            #     'customer_id': 'cus-03',
            #     'order_id': 'ord-01',
            #     'status': 'pending',
            #     'info': str_filter_j
            # })
            return redirect(url_for('display', location=user_input))
        else:
            data = get_api(user_input)
            filter_j = filter_api(data)
            create_json_file(filter_j, user_input)
            str_filter_j = json.dumps(filter_j)

            # table.put_item(Item=
            # {
            #     'customer_id': 'cus-03',
            #     'order_id': 'ord-01',
            #     'status': 'pending',
            #     'info': str_filter_j
            # })
            return redirect(url_for('display', location=user_input))
    return render_template('home.html')


@application.route('/display', methods=['GET','POST'])
def display():
    bg_color = os.getenv('BG_COLOR', '#ffffff')
    location = request.args.get('location')
    weather_data = backend.read_json_file(location)
    # if request.method == 'POST':
    #     if 'store_button' in request.form:
    #         # Store data in DynamoDB when button is clicked
    #         table.put_item(Item={
    #             'customer_id': '1',
    #             'order_id': "1",
    #             'location': location,
    #             'weather_data': json.dumps(weather_data)
    #         })
    return render_template('display.html', data=weather_data)


@application.route('/downloadskies', methods=['GET'])
def downloadskies():
    image_path = "sky.jpg"
    urllib.request.urlretrieve("https://d1p8hpk7shng87.cloudfront.net/sky.jpg", image_path)

    # Send the file to the client
    return send_file(
        image_path,
        as_attachment=True,
    )




if __name__ == '__main__':
    application.run()
