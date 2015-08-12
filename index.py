import logging
import os
import sys
import csv

from converttoqpx import createGPXTrack
from flask import Flask, render_template, request, abort, make_response, Response
from xml.dom import minidom
from StringIO import StringIO
from logging.config import fileConfig

app = Flask(__name__)
app.config.from_object('config')

port = 5000

# log = logging.getLogger()
# log.setLevel(logging.DEBUG)
fileConfig('logging_config.ini')
logger = logging.getLogger()


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/import', methods=['POST'])
def import_objects():
    output_file = 'flightlog.gpx'

    file = request.files['file']
    logging.debug('uploading file ' + file.filename)
    if file and allowed_file(file.filename):
        # extract content
        content = file.read()
        print content

        print('Input file is ', content)
        csvreader = csv.DictReader(StringIO(content))
        order = ['', 'latitude', 'longitude', 'altitude']
        gpxData = createGPXTrack(csvreader, output_file, order)

        # We need to modify the response, so the first thing we
        # need to do is create a response out of the CSV string
        response = make_response(gpxData)

        # This is the key: Set the right header for the response
        # to be downloaded, instead of just printed on the browser
        response.headers["Content-Disposition"] = "attachment; filename=flightlog.gpx"

        return response
    else:
        abort(make_response("File extension not acceptable", 400))


if __name__ == "__main__":
    # get port
    default_port = app.config['PORT']
    port = int(os.environ.get('PORT', default_port))

    # setup logger to log to stdout
    # ch = logging.StreamHandler(sys.stdout)
    # ch.setLevel(logging.DEBUG)
    # formatter = logging.Formatter(
    #     '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # ch.setFormatter(formatter)
    # log.addHandler(ch)

    app.debug = True

    # run app
    app.run(host='0.0.0.0', port=port)
