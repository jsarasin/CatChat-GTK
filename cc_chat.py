import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from cc_chatbubblerenderer import BubbleBuffer
from datetime import datetime

class cc_chat(object):
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
