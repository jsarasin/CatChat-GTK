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
		self.global_settings_visible(False)
		self.window.show_all()

	def update_url_fields_for_index(self, index):
		service_info = self.editing_config['services'][index]
		server_url_address = self.builder.get_object('server_url_address')
		server_url_username = self.builder.get_object('server_url_username')
		server_url_password = self.builder.get_object('server_url_password')

		server_url_address.set_text(service_info['server-url'])
		server_url_username.set_text(service_info['username'])
		server_url_password.set_text(service_info['password'])

	# This is called to update the configuration details area
	# As there may be multiple types of connections, we need to
	# update global properties, and then call for specific types
	def update_fields_for_index(self, index):
		service_info = self.editing_config['services'][index]

		server_display_name = self.builder.get_object('server_display_name')
		server_type = self.builder.get_object('server_type')

		server_display_name.set_text(service_info['display-name'])

		selectables = {
			'url':0,
		}

		if service_info['server-type'] == 'url':
			combo_selection = 0
		else:
			raise(ValueError('Unknown Server Type'))

		server_type.set_active(combo_selection)

		if service_info['server-type'] is 'url':
			self.update_url_fields_for_index(index)

	def save_changes(self):
		pass


	# Hide the global settings. We need to do this when we're on the first tab with the sad cat
	def global_settings_visible(self, visible):
		gb1 = self.builder.get_object('global_config_box1')
		gb1.set_visible(visible)

	def onTreeViewSelectionChange(self, selection):
		model, iterator = selection.get_selected()
		if iterator is None:
			self.notebook.set_current_page(0)
			self.global_settings_visible(False)
			return

		selectables = {
			'url':1,
		}

		self.global_settings_visible(True)
		note_page = getattr(selectables, model[iterator][2], 1)
		self.notebook.set_current_page(note_page)

		selected_index = model[iterator][1]
		self.update_fields_for_index(selected_index)


	def onCloseWindow(self, widget, event ):
		self.window.hide()
		return True
