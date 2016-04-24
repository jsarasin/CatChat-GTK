import cc_pictures
import datetime

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Pango, GdkPixbuf, GLib

BUBBLE_TIME_WINDOW = 1		# The time allowed between messages


class Bubble:
	messages = []
	text_buffer = None
	begin_mark = None
	begin_messages_mark = None
	begin_time_mark = None
	end_mark = None
	newest_message = None
	chttp = None

	"""
	@param 	id - A unique identifier for this bubble, not needed?
			textbuffer - The text buffer object that this object will insert text into
			owner - The user ID who this bubble belongs to
			date_time - When a new bubble is initially created, its start and end parameters will be set to this time
			insert_at - An iterator where we should create out new bubble
	@returns	tuple(Gtk.Iterator, message[] list index position in which to insert this message
	@caution	This will lock to the top and the bottom!
	"""
	def __init__(self, id, textbuffer, owner, date_time, insert_at, chttp):
		self.start = date_time
		self.end = date_time
		self.owner = owner
		self.messages = []
		self.text_buffer = textbuffer
		self.id = id
		self.chttp = chttp

		# Retair the iterators position
		self.text_buffer.insert(insert_at, "\n")
		self.begin_mark = self.text_buffer.create_mark(None, insert_at, True)
		self.text_buffer.insert(insert_at, str(owner) + " says:\n")
		self.begin_message_mark = self.text_buffer.create_mark(None, insert_at, True)
		self.text_buffer.insert(insert_at,  "\n")
		self.begin_time_mark = self.text_buffer.create_mark(None, insert_at, True)
		self.text_buffer.insert(insert_at, " ")
		self.end_mark = self.text_buffer.create_mark(None, insert_at, True)
		self.text_buffer.insert(insert_at, "\n")

		self.text_buffer.apply_tag_to_mark_range("says", self.begin_mark, self.begin_message_mark)


	"""
	@desc 	Get an iterator and index position in the messages list where this new message belongs
	@param 	id_chats -The idchats number associated with this message.
	@returns	list index
	"""
	def _get_insertion_point_mark(self, id_chats):
		if len(self.messages) == 0:
			return 0

		for i in range(0, len(self.messages)):		# can i use the build in function 'enumerate' ?
			if i == 0:
				last = 0
			else:
				last = self.messages[i-1]

			if last < id_chats < self.messages[i]['idchats']:
				return i

		return len(self.messages)

	def update_bubble_latest_time(self):
		current_time_start = self.text_buffer.get_iter_at_mark(self.begin_time_mark)
		current_time_end = self.text_buffer.get_iter_at_mark(self.end_mark)
		current_time_end.backward_char()
		#current_time_end.backward_char()
		self.text_buffer.delete(current_time_start, current_time_end)

		insert_at = self.text_buffer.get_iter_at_mark(self.begin_time_mark)
		self.text_buffer.insert(insert_at, str(self.newest_message))
		self.text_buffer.apply_tag_to_mark_range("time-sent", self.begin_time_mark, self.end_mark)

	"""
	@desc		Called by the widgets user to insert a new message
	@param	message		- The CatChat message format as a dict
	"""
	def add_message(self, message):
		index =  self._get_insertion_point_mark(message['idchats'])
		if index == 0:
			insert_at_mark = self.begin_message_mark
		elif index == len(self.messages):
			insert_at_mark = self.messages[len(self.messages)-1]['end_mark']
		else:
			insert_at_mark = self.messages[index]['start_mark']

		insert_at = self.text_buffer.get_iter_at_mark(insert_at_mark)

		if not isinstance(insert_at_mark, Gtk.TextMark):
			print "fucky: " + str(insert_at_mark)

		message['start_mark'] = self.text_buffer.create_mark(None, insert_at, True)

		# Actually insert the message, be it a text one, or an image
		if (message['message_type'] == 0):
			self.text_buffer.insert(insert_at, message['message'] + "\n")
		if (message['message_type'] == 1):
			picture = cc_pictures.get_pixbuf_thumbnail_from_hash(self.chttp, message['message'])
			self.text_buffer.insert_pixbuf(insert_at, picture)
			self.text_buffer.insert(insert_at, "\n")

		message['end_mark'] = self.text_buffer.create_mark(None, insert_at, False)
		self.messages.insert(index, message)

		if self.newest_message == None:
			self.newest_message = message['msg_written']
		elif message['msg_written'] > self.newest_message:
			self.newest_message = message['msg_written']

		self.update_bubble_latest_time()

"""
@desc	This holds a list of created Bubbles, and manages them.
"""
class Bubbles:
	bubbles = []
	text_buffer = None
	new_bubble_id = 0
	viewer_id = None
	chttp = None
	last_chat_bubble_owner = None

	def __init__(self, textbuffer, chttp):
		self.chttp = chttp
		self.text_buffer = textbuffer
		self.viewer_id = self.chttp.userid

	def _find_bubble_from_time(self, owner, date_time):
		# Iterate through all the bubbles looking for a compatible one
		for i in reversed(self.bubbles):
			min_time = i.start - datetime.timedelta(minutes=BUBBLE_TIME_WINDOW)
			max_time = i.end + datetime.timedelta(minutes=BUBBLE_TIME_WINDOW)

			if ((min_time < date_time < max_time) and
				owner == i.owner):
				return i

		# We didn't find one
		return False

	def _create_bubble_for_message(self, owner, date_time):
		insert_at = self.text_buffer.get_end_iter()
		new_bubble = Bubble(self.new_bubble_id, self.text_buffer, owner, date_time, insert_at, self.chttp)
		self.new_bubble_id += 1
		self.bubbles.append(new_bubble)
		return new_bubble

	def _bubble_merge_seek(self):
		pass

	def _bubble_join_bubble(self):
		pass

	def add_message(self, message):		# TODO: Creator, owner are the same thing. In the DB it's called creator_id. Uhg
		if self.last_chat_bubble_owner == message['creator']:
			bubble = self._find_bubble_from_time(message['creator'], message['msg_written'])
		else:
			bubble = False
			self.last_chat_bubble_owner = message['creator']

		if(bubble == False):
			bubble = self._create_bubble_for_message(message['creator'], message['msg_written'])

		if(message['creator'] == self.viewer_id):
			self.text_buffer.apply_tag_to_mark_range("bubble-left", bubble.begin_mark, bubble.end_mark)
		else:
			self.text_buffer.apply_tag_to_mark_range("bubble-right", bubble.begin_mark, bubble.end_mark)

		bubble.add_message(message)

"""
@desc This is an abstraction of the TextBuffer object.
"""
class BubbleBuffer(Gtk.TextBuffer):
	mark_name_list = []
	last_cat = 0
	mymark = None
	bubbles = None
	owner_id = None

	def __init__(self, cc_http_connection):
		Gtk.TextBuffer.__init__(self)
		self.setup_tags_and_buffer()
		self.owner_id = cc_http_connection.userid
		self.bubbles = Bubbles(self, cc_http_connection)

	def _get_not_so_start_iter(self):
		me = self.get_start_iter()
		me.forward_char()
		if not me: raise(ValueError("Someone soiled the buffer!"))
		return me

	def setup_tags_and_buffer(self):
		self.create_tag("says",				weight=Pango.Weight.BOLD)
		self.create_tag("message",			indent=10)
		self.create_tag("time-sent",		variant=Pango.Variant.SMALL_CAPS,
											scale=0.75,
											wrap_mode_set=Gtk.WrapMode.NONE)

		self.create_tag("bubble-left",		paragraph_background="lightgreen",
											right_margin=50)

		self.create_tag("bubble-right",  	justification=Gtk.Justification.RIGHT,
											paragraph_background="lightblue",
											left_margin = 100,
											direction=Gtk.TextDirection.RTL,
											wrap_mode=Gtk.WrapMode.WORD_CHAR,
											right_margin = 0)
		self.create_tag("highlight",		background="orange");

	def apply_tag_to_mark_range(self, tag_name, start_mark, end_mark):
		if (not isinstance(start_mark, Gtk.TextMark) or not isinstance(end_mark, Gtk.TextMark)):
			raise(ValueError("Cannot apply tag to non TextMark objects"))
		mark1 = self.get_iter_at_mark(start_mark)
		mark2 = self.get_iter_at_mark(end_mark)

		self.apply_tag_by_name(tag_name, mark1, mark2)


	def create_mark(self, name, itera, left_gravity=True):
		if name in self.mark_name_list and name != None:
			raise ValueError("You already created a mark with this name!")

		offset = itera.get_offset()

		new_mark = Gtk.TextBuffer.create_mark(self, name,itera,left_gravity)
		#new_mark.set_visible(True)

		self.mark_name_list.append(name)
		return new_mark

	def insert_message(self, message):
		self.last_cat += 1
		self.bubbles.add_message(message)
		print "Real line count" + str(self.get_line_count())
		pass
