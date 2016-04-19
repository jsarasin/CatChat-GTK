import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Pango, GdkPixbuf

import cc_pictures

class ChatBubbleRenderer(object):
	sender_id = 0
	sender_says_tag = Gtk.TextTag()
	cchttp = None

	def __init__(self, cchttpv):
		self.cchttp = cchttpv
		self.sender_id = self.cchttp.userid

	def setup_tags(self, textbuffer):
		#background="orange", justification=Gtk.Justification.RIGHT
		textbuffer.create_tag("says",		   weight=Pango.Weight.BOLD)
		textbuffer.create_tag("message",		indent=10
												)
		textbuffer.create_tag("time-sent",	  variant=Pango.Variant.SMALL_CAPS,
												scale=0.75,
												wrap_mode_set=Gtk.WrapMode.NONE)


		textbuffer.create_tag("bubble-left",	paragraph_background="lightgreen",
												right_margin=50)

		textbuffer.create_tag("bubble-right",   justification=Gtk.Justification.RIGHT,
												paragraph_background="lightblue",
												left_margin = 100,
												direction=Gtk.TextDirection.RTL,
												wrap_mode=Gtk.WrapMode.WORD_CHAR,
												right_margin = 0)

	def get_bubble(self, message, textbuffer):
		#textbuffer.get_iter_at_mark()
		insert_at = textbuffer.get_end_iter()

		mark_begin = textbuffer.create_mark("begin" + str(message['idchats']), insert_at, True)
		mark_end = textbuffer.create_mark("end" + str(message['idchats']), insert_at, False)

		textbuffer.insert(insert_at, "\n")
		textbuffer.insert_with_tags_by_name(insert_at, str(message['creator']) + " says:\n", "says")

		# Just a normal text message
		if(message['message_type'] == 0):
			textbuffer.insert_with_tags_by_name(insert_at, message['message'] , "message")

		# A fancy pants image message!
		if (message['message_type'] == 1):
			picture = cc_pictures.get_pixbuf_thumbnail_from_hash(self.cchttp, message['message'])
			textbuffer.insert_pixbuf(insert_at, picture)

		textbuffer.insert_with_tags_by_name(insert_at, "\nTime sent: " + message['msg_written'], "time-sent")



		begm = textbuffer.get_iter_at_mark(mark_begin)
		endm = textbuffer.get_iter_at_mark(mark_end)

		if(message['creator'] == self.sender_id):
			textbuffer.apply_tag_by_name("bubble-left", begm, endm)
		else:
			textbuffer.apply_tag_by_name("bubble-right", begm, endm)




# {u'msg_written': u'2016-04-16 23:50:00',
# u'message': u'hot dogs are ok i guess.',
# u'creator': 0,
# u'message_type': 0,
# u'idchats': 1}
