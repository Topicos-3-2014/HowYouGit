import urllib, urllib2, json, operator
from urllib2 import Request, urlopen

class GitHubService:

    def get_user_repos(self, username):

        token =  '<replace by your token>'

        github_user_repos = 'https://api.github.com/users/' + username + '/repos'

        request = Request(github_user_repos)
        request.add_header('Authorization', 'token %s' % token)
        data = json.load(urlopen(request))

        repos = []

        for repo in data:
            name = repo['name']
            github_repo_commits = 'https://api.github.com/repos/' + username + '/' + name + '/commits'
            github_repo_contributors = 'https://api.github.com/repos/' + username + '/' + name + '/contributors'

            request = Request(github_repo_commits)
            request.add_header('Authorization', 'token %s' % token)
            commits = len(json.load(urlopen(request)))

            request = Request(github_repo_contributors)
            request.add_header('Authorization', 'token %s' % token)
            contributors = len(json.load(urlopen(request)))

            repos.append({ 'name' : name, 'language' : repo['language'], 'url' : repo['html_url'], 'commits' : commits, 'contributors' : contributors })

        return repos

    def get_user_language_statistics(self, username):

        token =  '<replace by your token>'

        github_user_repos = 'https://api.github.com/users/' + username + '/repos'

        request = Request(github_user_repos)
        request.add_header('Authorization', 'token %s' % token)
        data = json.load(urlopen(request))

        languages = dict()
        total = 0

        for repo in data:
            language = repo['language']

            if language != None:
                total += 1
                if language in languages:
                    languages[language] += 1
                else:
                    languages[language] = 1

        for i in languages:
            languages[i] = "{0:.2f}".format((languages[i]/float(total))*100)

        return languages

    def get_user_contributors_statistics(self, username):

        token =  '<replace by your token>'

        github_user_repos = 'https://api.github.com/users/' + username + '/repos'

        request = Request(github_user_repos)
        request.add_header('Authorization', 'token %s' % token)
        data = json.load(urlopen(request))

        contributors_dict = dict()

        for repo in data:
            name = repo['name']
            github_repo_contributors = 'https://api.github.com/repos/' + username + '/' + name + '/contributors'

            request = Request(github_repo_contributors)
            request.add_header('Authorization', 'token %s' % token)
            contributors = json.load(urlopen(request))

            for contributor in contributors:
                name = contributor['login']
                if name != username:
                    if name in contributors_dict:
                        contributors_dict[name] += 1
                    else:
                        contributors_dict[name] = 1

        return contributors_dict


