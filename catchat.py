import cc_chat
import cc_http
import urllib
import os

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango, Gdk, GObject


TARGET_TYPE_URI_LIST = 80

CCHttp = cc_http.cc_http()

def get_file_path_from_dnd_dropped_uri(uri):
	# get the path to file
	path = ""
	if uri.startswith('file:\\\\\\'):  # windows
		path = uri[8:]  # 8 is len('file:///')
	elif uri.startswith('file://'):  # nautilus, rox
		path = uri[7:]  # 7 is len('file://')
	elif uri.startswith('file:'):  # xffm
		path = uri[5:]  # 5 is len('file:')

	path = urllib.url2pathname(path)  # escape special chars
	path = path.strip('\r\n\x00')  # remove \r\n and NULL

	return path

class MyWindow(Gtk.Window):
	chatroom = cc_chat.cc_chat(CCHttp)

	def __init__(self):
		#########################
		# Setup the main window
		Gtk.Window.__init__(self, title="Chat")
		self.set_border_width(5)
		self.set_size_request(400, 700)
		self.set_position(Gtk.WindowPosition.CENTER)

		#############################
		# Create the internal widgets

		# Create the chat area box
		self.box = Gtk.Box(spacing=5, orientation=Gtk.Orientation.VERTICAL)
		self.add(self.box)

		# Create the chat message area
		self.chat_scrollwindow = Gtk.ScrolledWindow()
		self.chat_scrollwindow.set_vexpand(True)
		self.chat_scrollwindow.set_hexpand(False)

		self.textview = Gtk.TextView()
		self.textview.set_buffer(self.chatroom.bubblebuffer)
		self.textview.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
		# self.textview.set_editable(False)
		# self.textview.set_cursor_visible(False)
		self.textview.connect("move-cursor", self.move_cursor_info)
		self.textview.connect("button-release-event", self.mouse_click)

		self.chat_scrollwindow.add(self.textview)
		self.box.add(self.chat_scrollwindow)

		# Create the text entry
		self.entry = Gtk.Entry()
		self.entry.connect("activate", self.on_entry_return)

		self.label = Gtk.Label()
		self.label.set_halign(Gtk.Align.START)
		self.box.add(self.label)


		#########GObject.timeout_add_seconds(2, self.update_chat)



		#####################
		# Setup the DND Files
		self.textview.drag_dest_set(Gtk.DestDefaults.ALL, [Gtk.TargetEntry.new("text/uri-list", 0, 80)], Gdk.DragAction.COPY)
		self.textview.drag_dest_add_text_targets();
		self.textview.connect("drag-motion", self.drag_over)
		self.textview.connect("drag-data-received", self.drag_drop_receive)

		self.entry.drag_dest_set(Gtk.DestDefaults.ALL, [Gtk.TargetEntry.new("text/uri-list", 0, 80)], Gdk.DragAction.COPY)
		self.entry.drag_dest_add_text_targets();
		self.entry.connect("drag-motion", self.drag_over)
		self.entry.connect("drag-data-received", self.drag_drop_receive)

		self.box.add(self.entry)

		self.update_chat()


	def mouse_click(self, widget, event):
		self.update_info_label()
		return False

	def move_cursor_info(self, text_view,step,count,extend_selection):
		self.update_info_label()

	def update_info_label(self):
		text = self.chatroom.bubblebuffer.get_iter_at_mark(self.chatroom.bubblebuffer.get_mark('insert'))
		self.label.set_text(str(text.get_offset()))
		pass

	def scroll_to_bottom(self):
		iter =  self.chatroom.bubblebuffer.get_iter_at_line(self.chatroom.bubblebuffer.get_line_count() - 1)


	def on_entry_return(self, input):
		if(self.entry.get_text() == ""):
			self.update_chat();
			return

		self.chatroom.say(self.entry.get_text())
		self.entry.set_text("")

		if(self.chatroom.update_required()):
			self.scroll_to_bottom()

	def drag_over(self, widget, context, x,y, time):
		Gdk.drag_status(context, Gdk.DragAction.COPY, time)
		return True

	def update_chat(self):
		if(self.chatroom.update_required()):
			self.scroll_to_bottom()

		return True



	def drag_drop_receive(self, widget, context, x, y, selection, target_type, time):
		if target_type == TARGET_TYPE_URI_LIST:
			uri = selection.get_data().strip('\r\n\x00')
			uri_splitted = uri.split()  # we may have more than one file dropped
			for uri in uri_splitted:
				path = get_file_path_from_dnd_dropped_uri(uri)
				if os.path.isfile(path):  # is it file?
					hash = self.chatroom.maybe_send_file_return_hash(path)
					self.chatroom.say_picture(hash)
					if(self.chatroom.update_required()):
						self.scroll_to_bottom()

win = MyWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
