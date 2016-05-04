from cc_configurator import get_cc_config

from cc_main_window import cc_main_window

from cc_connector import cc_connector_http

import urllib
import os

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango, Gdk, GObject


builder = None
config = None
connections = []

def connect_services():
    global config
    global connections

    config = get_cc_config()


    for item in range(0, len(config['services'])):
        name = config['services'][item]['display-name']
        type = config['services'][item]['server-type']
        username = config['services'][item]['username']
        password = config['services'][item]['password']
        print "Connecting to '" + name + "'"

        if type == "url":
            url = config['services'][item]['server-url']
            new_server = cc_connector_http.cc_connector_http(url, username, password)
            connections.append(new_server)

            new_server.connect()


def start_program():
    builder = Gtk.Builder()
    connect_services()

    main_window = cc_main_window(builder)

    Gtk.main()


if __name__ == "__main__":
    start_program()

