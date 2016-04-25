import cc_chatdialog
import cc_http
from cc_configurator import get_cc_config
from cc_configure_services import cc_configure_services

import urllib
import os

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango, Gdk, GObject

class cc_main_window(object):
	builder = None
	window = None
	configure_services_dialog = None

	def __init__(self, builder):
		self.builder = builder
		builder.add_from_file("glade/main_window.glade")
		self.window = builder.get_object("main_window")

		# Setup Signals
		self.builder.connect_signals(self)
		self.window.connect("delete-event", Gtk.main_quit)

		self.window.show_all()

		# Load other dialogs
		self.configure_services_dialog = cc_configure_services(builder)
		# Startup Operations
		if get_cc_config()['auto-connect']:
			self.onConnectServices(None)


	def delete_window(self):
		Gtk.main_quit


	def toggle_connect_disconnect_action_items(self, connected):
			action_connect = self.builder.get_object("action_connect")
			action_connect.set_sensitive(not connected)
			action_connect = self.builder.get_object("action_disconnect")
			action_connect.set_sensitive(connected)

	# Signal Handlers
	def onConnectServices(self, action):
		self.toggle_connect_disconnect_action_items(True)

	def onDisconnectServices(self, action):
		self.toggle_connect_disconnect_action_items(False)

	def onToggleShowDebugArea(self, menu_item):
		self.builder.get_object('debug_box').set_visible(menu_item.get_active())

	def onConfigureServices(self, action):
		print "Asdf"


