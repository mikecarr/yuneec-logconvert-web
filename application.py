# -*- coding: utf-8 -*-
"""

    :copyright: (c) 2015 by Mike Carr
    :license: BSD, see LICENSE for more details.

"""

import logging
import os, time
import csv
import random
import string

from converttoqpx import createGPXTrack
from flask import Flask, render_template, session, request, abort, make_response, Response, redirect, url_for, flash, g
# from xml.dom import minidom
from StringIO import StringIO
from logging.config import fileConfig
from doarama import doarama_params, post_file, create_visualisation, set_activity_info
# from sqlite3 import dbapi2 as sqlite3
from contextlib import closing
from werkzeug import secure_filename

application = Flask(__name__)
application.config.from_object('config')

fileConfig('logging_config.ini')
logger = logging.getLogger()

entries = []
doarama_params.update({'api-key' : os.environ['DOARAMA_API_KEY']})

@application.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

# def init_db():
#     with closing(connect_db()) as db:
#         with app.open_resource('schema.sql') as f:
#             db.cursor().executescript(f.read())
#         db.commit()

# def connect_db():
#     """ Connects to the database """
#     return sqlite3.connect(app.config['DATABASE'])

# @app.before_request
# def before_request():
#     g.db = connect_db()

# @app.after_request
# def after_request(response):
#     g.db.close()
#     return response

def init_filesystem():
    logger.debug("init_filesystem")
    filename = application.config['UPLOAD_FOLDER']
    d = os.path.dirname(filename)
    if not os.path.exists(d):
        os.makedirs(d)

@application.route('/api/cleanFiles')
def cron_clean_files():
    logger.debug("cron_clean_files")
    folder = application.config['UPLOAD_FOLDER']
    age = int(application.config['DAYS_TO_KEEP_LOGS'])
    age = int(age) * 86400


    for file in os.listdir(folder):
        now = time.time()
        filepath = os.path.join(folder, file)
        modified = os.stat(filepath).st_mtime
        if modified < now - age:
            if os.path.isfile(filepath):
                os.remove(filepath)
                logging.info("Deleted: " + file + "(" + str(modified) + ")")

    return "OK"


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in application.config['ALLOWED_EXTENSIONS']

@application.route('/visualisation')
def show_visualisation():
    return render_template('visualisation.html', entries=entries)

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@application.route('/import', methods=['POST'])
def import_objects():
    output_file = 'flightlog.gpx'

    file = request.files['file']
    logging.debug('uploading file ' + file.filename)
    if file and allowed_file(file.filename):
        # extract content
        content = file.read()
        csvreader = csv.DictReader(StringIO(content))
        order = ['', 'latitude', 'longitude', 'altitude']

        logger.debug("create Gpx Track")
        gpxData = createGPXTrack(csvreader, output_file, order)

        user_id = str(1234)
        doarama_params.update({'user-id': user_id})

        # create temp file
        init_filesystem()
        logger.debug("creating temp file")
        filename = application.config['UPLOAD_FOLDER']  + "flightlog" + id_generator() + ".gpx"
        gpxFile = open(filename, 'w')
        gpxFile.write(gpxData)
        gpxFile.close()

        # post temp file
        logger.debug("post file to doarama")
        gpxFile = open(filename, 'rb')
        post_id = post_file(user_id, gpxFile)
        print("Activity Id: " + str(post_id))

        # remove temp file
        if application.config['UPLOAD_FOLDER'] == True:
            os.remove(filename)

        # Each activity must be assigned a valid activity type. This is used to control various aspects of the
        # visualisation including playback rate and elevation correction so please set appropriately.
        set_activity_info(30, post_id)

        # create a visual key which will be passed to iframe in visualisation.html
        logger.debug("create_visualisation, post id: " + str(post_id))
        key_id = create_visualisation(post_id)
        print("Key Id: " + str(key_id))

        global entries
        entries = [dict(key_id=key_id,file_name=filename)]

        return redirect(url_for('show_visualisation'))

    else:
        abort(make_response("File extension not acceptable", 400))


if __name__ == "__main__":
    # get port
    default_port = application.config['PORT']
    port = int(os.environ.get('PORT', default_port))

    application.debug = True

    # init_db()
    init_filesystem()



    # run app
    application.run(host='0.0.0.0', port=port)
    #application.run()
