import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Pango, GdkPixbuf

import cc_pictures

class ChatBubbleRenderer(object):
	sender_id = 0
	sender_says_tag = Gtk.TextTag()
	cchttp = None
	textbuffer = None
	last_writter = -1	# The ID of the last bubble inserted

	class BubbleMark:
		SBubble 	= "sbubble",
		EBubble 	= "ebubble"
		SMessage 	= "smessage"
		EMessage	= "emessage"
		SSays		= "ssays"
		ESays		= "esays"
		STime		= "stime"
		ETime		= "etime"


	def __init__(self, cchttpv, textbuffer):
		self.cchttp = cchttpv
		self.sender_id = self.cchttp.userid
		self.textbuffer = textbuffer

	def setup_tags(self):
		#background="orange", justification=Gtk.Justification.RIGHT
		self.textbuffer.create_tag("says",			weight=Pango.Weight.BOLD)
		self.textbuffer.create_tag("message",		indent=10,

													)
		self.textbuffer.create_tag("time-sent",		variant=Pango.Variant.SMALL_CAPS,
													scale=0.75,
													wrap_mode_set=Gtk.WrapMode.NONE)


		self.textbuffer.create_tag("bubble-left",	paragraph_background="lightgreen",
												right_margin=50)

		self.textbuffer.create_tag("bubble-right",  justification=Gtk.Justification.RIGHT,
													paragraph_background="lightblue",
													left_margin = 100,
													direction=Gtk.TextDirection.RTL,
													wrap_mode=Gtk.WrapMode.WORD_CHAR,
													right_margin = 0)

	def create_mark(self, mark_type, mark_value, where):
		if(mark_type[0] == "s"):
			left_gravity = True
		elif (mark_type[0] == "e"):
			left_gravity = False

		self.textbuffer.create_mark(mark_type + ":" + str(mark_value), where, left_gravity),

	def get_iter_at_mark(self, mark_type, mark_value):
		mark_name = mark_type + ":" + mark_value

		iter = self.textbuffer.get_iter_at_mark(mark_name)

		if (iter == None):
			raise ValueError("Cannot find mark to return iterator")

		return iter


	##############################
	# Visible things added to chat
	def insert_image(self, iterator, message):
		self.create_mark(self.BubbleMark.SMessage, message["idchats"], iterator)
		self.create_mark(self.BubbleMark.EMessage, message["idchats"], iterator)
		picture = cc_pictures.get_pixbuf_thumbnail_from_hash(self.cchttp, message['message'])
		self.textbuffer.insert_pixbuf(iterator, picture)

	def insert_text(self, iterator, message):
		self.create_mark(self.BubbleMark.SMessage, message["idchats"], iterator)
		self.create_mark(self.BubbleMark.EMessage, message["idchats"], iterator)
		self.textbuffer.insert_with_tags_by_name(iterator, message['message'] , "message")

	def insert_says(self, iterator, message):
		self.create_mark(self.BubbleMark.SSays, message["creator"], iterator)
		self.create_mark(self.BubbleMark.ESays, message["creator"], iterator)
		self.textbuffer.insert_with_tags_by_name(iterator, str(message['creator']) + " says:\n", "says")

	def insert_time(self, iterator, message):
		self.create_mark(self.BubbleMark.STime, message["msg_written"], iterator)
		self.create_mark(self.BubbleMark.ETime, message["msg_written"], iterator)
		self.textbuffer.insert_with_tags_by_name(iterator, "\nTime sent: " + message['msg_written'], "time-sent")

	def get_bubble(self, message):
		#self.textbuffer.get_iter_at_mark()
		#insert_at =

		self.textbuffer.insert(insert_at, "\n")



		self.insert_says(insert_at, message)

		# Just a normal text message
		if(message['message_type'] == 0):
			self.insert_text(insert_at, message)
		# A fancy pants image message!
		if (message['message_type'] == 1):
			self.insert_image(insert_at, message)

		self.insert_time(insert_at, message)

		#begm = self.textbuffer.get_iter_at_mark(mark_begin)
		#endm = self.textbuffer.get_iter_at_mark(mark_end)

		#if(message['creator'] == self.sender_id):
		#	self.textbuffer.apply_tag_by_name("bubble-left", begm, endm)
		#else:
		#	self.textbuffer.apply_tag_by_name("bubble-right", begm, endm)




# {u'msg_written': u'2016-04-16 23:50:00',
# u'message': u'hot dogs are ok i guess.',
# u'creator': 0,
# u'message_type': 0,
# u'idchats': 1}
