import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Pango, GdkPixbuf

import cc_http, os

def download_thumbnail_from_hash(cc_http_connection, hash):
    return cc_http_connection.get_picture_thumbnail(hash)

def get_pixbuf_thumbnail_from_hash(cc_http_connection, hash):
    # Do we already have the file?
    cached_file_name = "thumbnails/" + hash

    if os.path.isfile(cached_file_name) == False:
        if download_thumbnail_from_hash(cc_http_connection, hash) == True:
            picture = GdkPixbuf.Pixbuf.new_from_file(cached_file_name)
        else:
            picture = GdkPixbuf.Pixbuf.new_from_file("missing.png")
    else:
        picture = GdkPixbuf.Pixbuf.new_from_file(cached_file_name)


    return picture
