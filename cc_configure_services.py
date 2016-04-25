from cc_configurator import get_cc_config


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango, Gdk, GObject

class cc_configure_services(object):
	builder = None
	window = None
	liststore = None
	listview = None
	editing_config = None 	# This is a copy of the global configure we're going to work on
	notebook = None

	def __init__(self, builder):
		self.builder = builder
		builder.add_from_file("glade/configure_services.glade")

		# Get local references to builder objects
		self.notebook = builder.get_object('services_notebook')
		self.listview = self.builder.get_object('connection_names_list')
		self.window = builder.get_object("configure_services")

		# Create the list store
		self.liststore = Gtk.ListStore(str, int, str)

		# Setup our listview
		self.listview.set_model(self.liststore)
		renderer = Gtk.CellRendererText()
		column = Gtk.TreeViewColumn("Services", renderer, text=0)
		self.listview.append_column(column)

		# Connect various signals
		self.builder.connect_signals(self)
		select = self.listview.get_selection()
		select.connect('changed', self.onTreeViewSelectionChange)

	def update_liststore(self):
		c = self.editing_config
		self.liststore.clear()
		for item in range(0, len(c['services'])):
			name = str(c['services'][item]['display-name'])
			self.liststore.append([name, item, c['services'][item]['server-type']])


	def delete_window(self):
		print "setup close cancel handler"
		pass

	def open_window(self):
		self.editing_config = get_cc_config()
		self.update_liststore()
		self.window.show_all()

	def onTreeViewSelectionChange(self, selection):
		model, iterator = selection.get_selected()
		if iterator is None:
			self.notebook.set_current_page(0)
			return

		selectables = {
			'url':1,
		}

		note_page = getattr(selectables, model[iterator][2], 1)

		self.notebook.set_current_page(note_page)



	def onCloseWindow(self, widget, event ):
		self.window.hide()
		return True
