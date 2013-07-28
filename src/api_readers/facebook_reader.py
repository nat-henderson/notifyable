from api_readers.api_reader_daemon import APIReaderDaemon
import random
import urllib2
import json
import time
from models import Status

class FacebookReader(APIReaderDaemon):
    #testing on a hard-coded access_token
    access_tokens = ["CAAT4W0M4Xq8BAEqKediuZCztZC5XBrTlHJY0ZBVW9xuZB07lHlMKZAHHq1TsjBIyA69fMAsi6DscYJzY0v0KqWQzncvWc6wSXldexfMmatsnenBONetHXZAqoabmPIRwWEX6F86XiAMEorcHmNyRXIZCw2hUZBhhMZAgZD"]
    pagination_next = {}

    def get_data(self, url):
        str=""
        req = urllib2.Request(url)
        try: 
            response= urllib2.urlopen(req)
            str=response.read()
        except Exception, e:
            print e
        return str

    def start(self):
        base_url = "https://graph.facebook.com"
        while True:
            for access_token in self.access_tokens:
                user_id = int(json.loads(self.get_data(base_url + "/me?access_token="+access_token))["id"])
                posts = None
                if user_id in self.pagination_next:
                    posts = json.loads(self.get_data(self.pagination_next[user_id]))
                else:
                    posts = json.loads(self.get_data(base_url + "/me/feed?access_token="+access_token))
                if "paging" in posts.keys():
                    self.pagination_next[user_id] = posts["paging"]["next"]
                posts = posts["data"]
                for post in posts:
                    status = post["story"]
                    from_name = post["from"]["name"]
                    picture = None
                    if("picture" in post.keys()):
                        picture = post["picture"]
                    entry = Status(status, from_name, user_id, pic_url=picture)
                    import ipdb; ipdb.set_trace()
                    self.session.add(entry)
            self.session.commit()
            time.sleep(60)

    def stop(self):
        pass

    def __init__(self, **kwargs):
        pass


if __name__=="__main__":
    FacebookReader().start()