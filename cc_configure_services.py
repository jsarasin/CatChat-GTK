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
		self.window.show_all()

	def delete_window(self):
		print "setup close cancel handler"
		pass

