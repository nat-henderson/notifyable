from api_reader_daemon import APIReaderDaemon
import random
import urllib2
import json

class FacebookReader(APIReaderDaemon):
    APP_ID = "1398970760322735"
    APP_SECRET = "eee97fc2ad0ae9666a6f178932a09893"
    REDIRECT_URL = "FILL_THIS_IN"
    SCOPE = ""

    access_token = 'CAAT4W0M4Xq8BAEr2XZApp0zNd9pdOMHe0QW6X7feflCvFPXqAlnV4ZAnoT7LTkQC8qFEfrzl92UIRvZBruZATlzofd5DaLrmHgKbpMUKTydqzcNXUiVu0SXpkfO4jro0deE0wiOtOzkg0Kz7w9Q89NHcq3mdSvUZD'

    def get_dialog_url(self):
        return "http://www.facebook.com/dialog/oauth/?client_id="+self.APP_ID+"&redirect_uri="+self.REDIRECT_URL+"&scope="+self.SCOPE+"&state="+str(random.randint(1, 1000))
        
    def get_access_token_url(self, code):
        return "https://graph.facebook.com/oauth/access_token?client_id="+self.APP_ID+"&redirect_uri="+self.REDIRECT_URL+"&client_secret="+self.APP_SECRET+"&code="+code

    def get_user_details(self, access_token):
        list={}
        url = "https://graph.facebook.com/me?access_token="+access_token;
        req = urllib2.Request(url)
        try: 
            response= urllib2.urlopen(req)
            str=response.read()
            list = json.dumps(str)
        except Exception, e:
            print e
     
        return list    

    def start(self):
        print self.get_user_details(self.access_token)

if __name__=="__main__":
    FacebookReader().start()