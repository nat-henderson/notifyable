from api_reader_daemon import APIReaderDaemon
import datetime
import time
from github import Github
from models import GithubRepo
from models import GithubRepoEvent

class GithubReaderDaemon(APIReaderDaemon):
    def __init__(self, **kwargs):
        # neh.  don't need it.
        pass

    def start(self):
        while True:
            repos_to_read = self.session.query(GithubRepo).all()
            for repo in repos_to_read:
                gh = Github()
                a_minute_ago = datetime.datetime.now() - datetime.timedelta(seconds = 30)
                repo = gh.get_repo(repo.github_user + '/' + repo.github_repo)
                events = repo.get_events()
                if events[0].created_at > a_minute_ago and events[0].type == 'PushEvent':
                    author = events[0].actor
                    commit = events[0].payload['commits'][0]['message']
                    new_event = GithubRepoEvent(repo.id, author.name,
                            author.avatar_url, commit)
                    self.session.add(new_event)
            self.session.commit()
            time.sleep(60)

    def stop(self):
        # or whatever
        pass

if __name__ == '__main__':
    GithubReaderDaemon().start()
