import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import cc_http
import cc_chatbubblerenderer

class cc_chat(object):
    chat_history = Gtk.TextBuffer()
    bubble_maker = None
    cchttp = None
    chatroom = 0
    chat_range_start = 0
    chat_range_end = 0

    def __init__(self, cchttpv):
        self.cchttp = cchttpv
        self.bubble_maker = cc_chatbubblerenderer.ChatBubbleRenderer(cchttpv)
        self.bubble_maker.setup_tags(self.chat_history)

        reply = self.cchttp.get_chat_from_id_range(self.chatroom)

        for message in reply['chat_log']:
            self.add_message_bubble(message)

    def add_message_bubble(self, message):
        if (message['idchats'] < self.chat_range_start):
            self.chat_range_start = message['idchats']
        if (message['idchats'] > self.chat_range_end):
            self.chat_range_end = message['idchats']

        self.bubble_maker.get_bubble(message, self.chat_history)

    def say(self, message):
        self.cchttp.say(self.chatroom, message)

    def say_picture(self, hash):
        self.cchttp.say_picture(self.chatroom, hash)

    def maybe_send_file_return_hash(self, filename):
        md5 = self.cchttp.md5(filename)

        if(self.cchttp.check_hash_exists(md5) == False  ):
            self.cchttp.send_file(self.chatroom, filename)

        return md5


    def update(self):
        reply = self.cchttp.get_chat_from_id_range(self.chatroom, self.chat_range_end)
        for message in reply['chat_log']:
            self.add_message_bubble(message)

