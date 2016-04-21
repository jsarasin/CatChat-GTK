import cc_pictures
from datetime import datetime

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Pango, GdkPixbuf, GLib

BUBBLE_TIME_WINDOW = 5		# 5 minutes
NON_VISIBLE_SPACE = " "	# Used for separating marks. Can I replace with the unicode replacement character,
							# or will that mess with the TextBuffer operation?

class BubbleMarkName:
	SBubble = "sbubble",
	EBubble = "ebubble"
	SMessage = "smessage"
	EMessage = "emessage"
	SSays = "ssays"
	ESays = "esays"
	STime = "stime"
	ETime = "etime"

def get_mark_name(type, value1, value2=None, value3=None):
	name = type
	if value1: name += str(value1)
	if value2: name += str(value2)
	if value3: name += str(value3)
	return name

class Bubble:
	messages = []
	text_buffer = None
	# TODO, experiment with static ID, maybe this keyword?

	def __init__(self, id, textbuffer, owner, date_time):
		self.start = date_time
		self.end = date_time
		self.owner = owner
		self.messages = []
		self.text_buffer = textbuffer
		self.id = id

	def _get_insertion_point(self, id_chats):
		last = 0
		for i in range(0, len(self.messages)):
			if i > 0:
				last = self.messages[i - 1]

			if last < id_chats > self.messages[i]['idchats']:
				if last == 0:
					last_mark = get_mark_name(BubbleMarkName.SBubble, self.id)
				else:
					last_mark = get_mark_name(BubbleMarkName.SMessage, self.messages[i]['idchats'])
				return last_mark, i

		return None, len(self.messages)

	def add_message(self, message):
		insert_after_mark, i = self._get_insertion_point(message['idchats'])

		self.messages.insert(message['idchats'], i)

		#iterator =
		pass

class Bubbles:
	bubbles = []
	text_buffer = None
	new_bubble_id = 0

									# Scott Meyer says something I dont remember about passing a variable through a
	def __init__(self, textbuffer):	# bunch of things just cause the end thing needs it, hmmm, what was that now.
		self.text_buffer = textbuffer

	def _find_bubble_from_time(self, owner, date_time):
		# Iterate through all the bubbles looking for a compatible one
		for i in self.bubbles:
			if (i.start - datetime.min(BUBBLE_TIME_WINDOW) < date_time < i.end - datetime.min(BUBBLE_TIME_WINDOW) and
				owner == i.owner):
				return x
		# We didn't find one
		return False

	def _create_bubble_for_message(self, owner, date_time):
		new_bubble = Bubble(self.new_bubble_id, self.text_buffer, owner, date_time)
		self.new_bubble_id += 1
		return new_bubble

	def _bubble_merge_seek(self):
		pass

	def _bubble_join_bubble(self):
		pass

class BubbleBuffer(Gtk.TextBuffer):
	mark_name_list = []
	last_cat = 0

	def __init__(self, owner_id):
		Gtk.TextBuffer.__init__(self)
		self.setup_tags_and_buffer()
		self.owner_id = owner_id

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

		self.insert(self.get_end_iter(), "\n\n")

	def create_mark(self, name, itera, left_gravity=True):
		if name in self.mark_name_list:
			raise ValueError("You already created a mark with this name!")

		offset = itera.get_offset()

		if itera.get_offset() == 0:
			print "hi"
			self.insert(self.get_start_iter(), "\n")
			itera = self.get_iter_at_offset(1)


		Gtk.TextBuffer.create_mark(self, name,itera,left_gravity)
		mark = self.get_mark(name)
		mark.set_visible(True)

		self.mark_name_list.append(name)



	def insert_message(self, message):
		self.create_mark("catman" + str(self.last_cat), self.get_start_iter())
		self.last_cat += 1
		#insertion_point =
		pass
