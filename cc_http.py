# Interface to the catchat server http requests
import requests
import json
import datetime
import hashlib


class cc_http(object):
    server_url = 'http://azenguard.com/CatChat/'
    username='james'
    password='computer'
    userid=0

    def md5(self, fname):
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def get_chat_from_id_range(self, chat_id, after=0, before=""):
        r = requests.post(self.server_url + 'getchat.php', data={               'chatroom': str(chat_id),
                                                                                'rangetype': "id",
                                                                                'after': str(after),
                                                                                'before': str(before)
                                                                                } )
        print r.text
        return json.loads(r.text)

    def say(self, chat_id, message):
        now = datetime.datetime.now()
        r = requests.post(self.server_url + 'writechat.php', data={             'chatroom': str(chat_id),
                                                                                'message':message,
                                                                                'msg_written': str(now),
                                                                                'message_type' : 0,
                                                                                'creator_id' : self.userid
                                                                                })
    def say_picture(self, chat_id, hash):
        now = datetime.datetime.now()
        r = requests.post(self.server_url + 'writechat.php', data={             'chatroom': str(chat_id),
                                                                                'message':hash,
                                                                                'msg_written': str(now),
                                                                                'message_type' : 1,
                                                                                'creator_id' : self.userid
                                                                                })

    def send_file(self, chat_id, filename):
        md5_file = self.md5(filename)
        now = datetime.datetime.now()
        files = {'userfile':open(filename, 'rb')}
        datas = {                                                               'creator_id':self.userid,
                                                                                'msg_written': str(now),
                                                                                'chatroom': str(chat_id),
                                                                                }
        r = requests.post(self.server_url + 'writechatfile.php', data=datas, files=files)

    def check_hash_exists(self, hash):
        datas = {                                                               'hash':hash
                                                                                }

        r = requests.post(self.server_url + "check_hash_exists.php", data=datas)
        reply = json.loads(r.text)

        return reply['exists']

    def get_picture_thumbnail(self, hash):
        r = requests.post(self.server_url + "thumbnails/" + hash)

        if(r.headers['content-type'] == "image/png"):
            open("thumbnails/" + hash, 'wb').write(r.content)
            return True
        else:
            print "get_picture_thumbnail failed!, Status Code: " + str(r.status_code) #+ str(r.headers.items()) + "\n"
            return r.status_code
# text/plain
# image/png

#CaseInsensitiveDict({'content-length': '42790', 'accept-ranges': 'bytes', 'server': 'Apache/2.4.6 (CentOS) OpenSSL/1.0.1e-fips mod_fcgid/2.3.9 PHP/5.4.16', 'last-modified': 'Mon, 18 Apr 2016 08:49:53 GMT', 'etag': '"a726-530be71b95ffb"', 'date': 'Mon, 18 Apr 2016 08:52:44 GMT', 'content-type': 'image/png'})
#http://azenguard.com/CatChat/thumbnails/cc9f2d22efdd1a8a161860a27eadc72f
