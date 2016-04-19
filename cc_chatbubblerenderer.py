import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Pango, GdkPixbuf

import cc_pictures

class ChatBubbleRenderer(object):
	sender_id = 0
	sender_says_tag = Gtk.TextTag()
	cchttp = None
	textbuffer = None

	def __init__(self, cchttpv, textbuffer):
		self.cchttp = cchttpv
		self.sender_id = self.cchttp.userid
		self.textbuffer = textbuffer

	def setup_tags(self):
		#background="orange", justification=Gtk.Justification.RIGHT
		self.textbuffer.create_tag("says",		   weight=Pango.Weight.BOLD)
		self.textbuffer.create_tag("message",		indent=10
												)
		self.textbuffer.create_tag("time-sent",	  variant=Pango.Variant.SMALL_CAPS,
												scale=0.75,
												wrap_mode_set=Gtk.WrapMode.NONE)


		self.textbuffer.create_tag("bubble-left",	paragraph_background="lightgreen",
												right_margin=50)

		self.textbuffer.create_tag("bubble-right",   justification=Gtk.Justification.RIGHT, paragraph_background="lightblue", left_margin = 100, direction=Gtk.TextDirection.RTL, wrap_mode=Gtk.WrapMode.WORD_CHAR, right_margin = 0)

	def insert_image(self, iterator, hash):
		picture = cc_pictures.get_pixbuf_thumbnail_from_hash(self.cchttp, hash)
		self.textbuffer.insert_pixbuf(iterator, picture)

	def insert_text(self, iterator, message):
		self.textbuffer.insert_with_tags_by_name(iterator, message , "message")

	def get_bubble(self, message):
		#self.textbuffer.get_iter_at_mark()
		insert_at = self.textbuffer.get_end_iter()

		mark_begin = self.textbuffer.create_mark("begin" + str(message['idchats']), insert_at, True)
		mark_end = self.textbuffer.create_mark("end" + str(message['idchats']), insert_at, False)

		self.textbuffer.insert(insert_at, "\n")
		self.textbuffer.insert_with_tags_by_name(insert_at, str(message['creator']) + " says:\n", "says")

		# Just a normal text message
		if(message['message_type'] == 0):
			self.insert_text(insert_at, message['message'])
		# A fancy pants image message!
		if (message['message_type'] == 1):
			self.insert_image(insert_at, message['message'])

		self.textbuffer.insert_with_tags_by_name(insert_at, "\nTime sent: " + message['msg_written'], "time-sent")



		begm = self.textbuffer.get_iter_at_mark(mark_begin)
		endm = self.textbuffer.get_iter_at_mark(mark_end)

		if(message['creator'] == self.sender_id):
			self.textbuffer.apply_tag_by_name("bubble-left", begm, endm)
		else:
			self.textbuffer.apply_tag_by_name("bubble-right", begm, endm)




# {u'msg_written': u'2016-04-16 23:50:00',
# u'message': u'hot dogs are ok i guess.',
# u'creator': 0,
# u'message_type': 0,
# u'idchats': 1}
