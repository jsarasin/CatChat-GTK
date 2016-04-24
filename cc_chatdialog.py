import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango, Gdk, GObject

from cc_chatbubblerenderer import BubbleBuffer
from datetime import datetime

TARGET_TYPE_URI_LIST = 80



class MyWindow(Gtk.Window):
	chatroom = None

	def __init__(self, CCHttp):
		chatroom = cc_chatdialog.cc_chatdialog(CCHttp)

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
		self.textview.set_editable(False)
		self.textview.set_cursor_visible(False)
		color = Gdk.RGBA(1, 0, 0, 0)
		#self.textview.override_background_color(Gtk.StateType.NORMAL, color)

		self.chat_scrollwindow.add(self.textview)
		self.box.add(self.chat_scrollwindow)

		# Create the text entry
		self.entry = Gtk.Entry()
		self.entry.connect("activate", self.on_entry_return)

		GObject.timeout_add_seconds(2, self.update_chat)



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
		self.scroll_to_bottom()


	def scroll_to_bottom(self):
		iter =  self.chatroom.bubblebuffer.get_iter_at_line(self.chatroom.bubblebuffer.get_line_count()-1)
		self.textview.scroll_to_iter(iter, 0, True, 0, 1)
		print self.chatroom.bubblebuffer.get_line_count()


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


class cc_chatdialog(object):
	chatroom = 0
	chat_range_start = 0
	chat_range_end = 0

	def __init__(self, cchttpv):
		self.cchttp = cchttpv
		self.bubblebuffer = BubbleBuffer(self.cchttp)

		self.update_required()

	def say(self, message):
		self.cchttp.say(self.chatroom, message)

	def say_picture(self, hash):
		self.cchttp.say_picture(self.chatroom, hash)

	def maybe_send_file_return_hash(self, filename):
		md5 = self.cchttp.md5(filename)

		if(self.cchttp.check_hash_exists(md5) == False  ):
			self.cchttp.send_file(self.chatroom, filename)
		return md5



	def add_message_bubble(self, message):
		if (message['idchats'] < self.chat_range_start):
			self.chat_range_start = message['idchats']
		if (message['idchats'] > self.chat_range_end):
			self.chat_range_end = message['idchats']

		self.bubblebuffer.insert_message(message)

	def update_required(self):
		pass
		reply = self.cchttp.get_chat_from_id_range(self.chatroom, self.chat_range_end)
		if (reply.get('up_to_date', False) == True):
			return False

		# We got some messages.
		for message in reply['chat_log']:
			# Let's convert the msg_written string to a datetime object
			date_object = datetime.strptime(message['msg_written'], '%Y-%m-%d %H:%M:%S')
			message['msg_written'] = date_object
			self.add_message_bubble(message)

		return True
