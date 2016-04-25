from cc_configurator import get_cc_config


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango, Gdk, GObject

class cc_configure_services(object):
	builder = None
	window = None

	def __init__(self, builder):
		self.builder = builder
		builder.add_from_file("glade/configure_services.glade")
		self.window = builder.get_object("configure_services")

		self.builder.connect_signals(self)
		self.build_liststore()

	def build_liststore(self):
		c = get_cc_config()

	def delete_window(self):
		print "setup close cancel handler"
		pass

	def open_window(self):
		self.window.show_all()

	def onCloseWindow(self, widget, event ):
		self.window.hide()
		return True
