from api_readers.api_reader_daemon import APIReaderDaemon
import random
import urllib2
import json
from models import Status

class FacebookReader(APIReaderDaemon):
    APP_ID = "1398970760322735"
    APP_SECRET = "eee97fc2ad0ae9666a6f178932a09893"
    REDIRECT_URL = "http://amagit.com:5000/"
    SCOPE = "read_stream"

    access_tokens = ["CAAT4W0M4Xq8BAEqKediuZCztZC5XBrTlHJY0ZBVW9xuZB07lHlMKZAHHq1TsjBIyA69fMAsi6DscYJzY0v0KqWQzncvWc6wSXldexfMmatsnenBONetHXZAqoabmPIRwWEX6F86XiAMEorcHmNyRXIZCw2hUZBhhMZAgZD"]
    pagination_next = {}

    def get_dialog_url(self):
        return "http://www.facebook.com/dialog/oauth/?client_id="+self.APP_ID+"&redirect_uri="+self.REDIRECT_URL+"&scope="+self.SCOPE+"&state="+str(random.randint(1, 1000))
        
    def get_access_token_url(self, code):
        return "https://graph.facebook.com/oauth/access_token?client_id="+self.APP_ID+"&redirect_uri="+self.REDIRECT_URL+"&client_secret="+self.APP_SECRET+"&code="+code

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

    def stop(self):
        pass

    def __init__(self, **kwargs):
        pass


if __name__=="__main__":
    FacebookReader().start()