import cc_chatdialog
import cc_http
import cc_configurator
from cc_main_window import cc_main_window

import urllib
import os

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango, Gdk, GObject

auto_connect = True
builder = None

def start_program():
	CCHttp = cc_http.cc_http()

	builder = Gtk.Builder()

	main_window = cc_main_window(builder)

	# if auto_connect:
	# 	action_connect = builder.get_object("action_connect")
	# 	action_connect.activate()
	# 	toggle_connect_disconnect_action_items(True)

	Gtk.main()


#Gtk.main_quit
if __name__ == "__main__":
	start_program()

