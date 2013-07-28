from api_readers.api_reader_daemon import APIReaderDaemon
import random
import urllib2
import json

class FacebookReader(APIReaderDaemon):
    APP_ID = "1398970760322735"
    APP_SECRET = "eee97fc2ad0ae9666a6f178932a09893"
    REDIRECT_URL = "http://amagit.com:5000/"
    SCOPE = "read_stream"

    access_token = "CAAT4W0M4Xq8BAEqKediuZCztZC5XBrTlHJY0ZBVW9xuZB07lHlMKZAHHq1TsjBIyA69fMAsi6DscYJzY0v0KqWQzncvWc6wSXldexfMmatsnenBONetHXZAqoabmPIRwWEX6F86XiAMEorcHmNyRXIZCw2hUZBhhMZAgZD"

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
        print self.get_dialog_url()
        print self.get_access_token_url('AQBFkdQ62e8SKEV5I4T9VuKg7Tj6ximM0cKSqqTqZa7eRaUk_CrMRgpUt0F3z1a8Btj6LWOQC7tOgtQ78fPPhxJ-v9YujyoMkRDBZKmGf0zC_VCC7mf-cbNdJeFfIigh2vIWoKTBPm4jY6lHdqJIVAkz6I1Bg-GWlhSPsBD_drTQZ0otoktCKi6Angwyd7qibQmZ3Ae_QK5FSnoVkKGDPFJH1uvZXX9QAWJ4KAdxRFEgcHlQwuYAtlr1UfmouCt803lk1Gdw5rzJ-ckT_3m34JG7O84c_2A7XNK8shMyY55HZdf6lYjjSef-H_vtpqA_UEM')
        print self.get_user_details(self.access_token)

if __name__=="__main__":
    FacebookReader().start()