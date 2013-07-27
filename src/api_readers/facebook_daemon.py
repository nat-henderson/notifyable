from api_readers.api_reader_daemon import APIReaderDaemon
import random

class FacebookReader(APIReaderDaemon):
    APP_ID='1398970760322735'
    APP_SECRET='eee97fc2ad0ae9666a6f178932a09893'
    REDIRECT_URL='FILL_THIS_IN'
    SCOPE='FILL_THIS_IN'

    def get_dialog_url(self):
        return "http://www.facebook.com/dialog/oauth/?client_id="+APP_ID+"&redirect_uri="+REDIRECT_URL+"&scope="+SCOPE+"&state="+str(random.randint(1, 1000))
        
    def get_access_token_url(self, code):
        return "https://graph.facebook.com/oauth/access_token?client_id="+APP_ID+"&redirect_uri="+REDIRECT_URL+"&client_secret="+APP_SECRET+"&code="+code