# server.py

from os.path import join, dirname, realpath
from flask import Flask, url_for, send_file

print(join(dirname(realpath(__file__)), "static"))
server = Flask(__name__, static_folder=join(dirname(realpath(__file__)), "static"))


@server.route('/styles/style.css')
def send_css():
    filepath = join(server.static_folder, "styles", "style.css")
    return send_file(filepath, attachment_filename="style.css")

