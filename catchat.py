import cc_chatdialog
import cc_http
import cc_configurator
from cc_main_window import cc_main_window

import urllib
import os

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango, Gdk, GObject

builder = None

def start_program():
    builder = Gtk.Builder()

    main_window = cc_main_window(builder)

    Gtk.main()


if __name__ == "__main__":
    start_program()
