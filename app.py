from flask import Flask, request, send_file, make_response
from flask import json
from tinydb import TinyDB
from flask_cors import CORS
import os
from WidgetDatabase import Widget
from WidgetDatabase import WidgetDatabase
app = Flask(__name__)
CORS(app)
database = WidgetDatabase()
@app.route('/')
def hello_world():
    return 'Hello, World!'

#get All widgets
@app.route('/widgets')
def getWidgets():
    try:
        resp = make_response(json.dumps(database.getAllWidgets()))
        resp.headers['content-type'] = 'application/json'
        return resp
    except:
        print("error in getting widgets")

# get widget by id
@app.route('/widgets/<widget_id>')
def getWidget(widget_id):
    try:
        resp = make_response(json.dumps(database.getWidget(widget_id)))
        resp.headers['content-type'] = 'application/json'
        return resp
    except:
        return "Error occurred in getting widget:" + repr(widget_id)

#delete widget by id
@app.route('/widgets/<widget_id>', methods=["DELETE"])
def deleteWidget(widget_id):
    try:
        resp = make_response(json.dumps(database.deleteWidget(widget_id)))
        resp.headers['content-type'] = 'application/json'
        return resp
    except:
         return "Error occurred in deleting widget:" + repr(widget_id)


@app.route('/upload/<widget_name>', methods=['POST'])
def uploadWidget(widget_name):
    if request.method == 'POST':
        try:
            script = request.files['widget_data']
            styles = request.files['widget_styles']
            tags = request.form.get('widget_tags')
            types = request.form.get('widget_types')
            os.makedirs(f'uploads/{widget_name}')
            script.save(f'uploads/{widget_name}/element.js')
            styles.save(f'uploads/{widget_name}/styles.css')
            widget = Widget()    
            widget.name = widget_name
            widget.src = f'uploads/{widget_name}/element.js'
            widget.styles = f'uploads/{widget_name}/styles.css' 
            widget.tags = tags
            widget.types = types
            database.addWidget(widget)
            resp = make_response(json.dumps({'Status': 'Successfully uploaded!', 'ID': widget_name}))
            resp.headers['content-type'] = 'application/json'
            return resp
        except:
            return "error in adding wisget", 400
        else:
            return "Something went wrong", 400

@app.route('/download/<widget_name>')
def download(widget_name):
    try:
        print('download file')
        return send_file(f'uploads/{widget_name}/element.js')
    except request.exceptions.Timeout as errt:
            return "A Timeout Error occurred:" + repr(errt)
   

@app.route('/download/styles/<widget_name>')
def downloadSTyle(widget_name):
    try:
        print('download style file')
        return send_file(f'uploads/{widget_name}/styles.css')
    except request.exceptions.Timeout as errt:
            return "A Timeout Error occurred:" + repr(errt)



