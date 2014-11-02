import urllib, urllib2, json, operator
from urllib2 import Request, urlopen
from operator import itemgetter

class GitHubService:

    def get_user_repos(self, username):

        token =  '3b0f1e62caf99cdfefb8bcb20050b4aff025e165'

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

        token =  '3b0f1e62caf99cdfefb8bcb20050b4aff025e165'

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

        token =  '3b0f1e62caf99cdfefb8bcb20050b4aff025e165'

        github_user_repos = 'https://api.github.com/users/' + username + '/repos?type=all'

        request = Request(github_user_repos)
        request.add_header('Authorization', 'token %s' % token)
        data = json.load(urlopen(request))

        contributors_dict = dict()

        for repo in data:
            name = repo['name']
            owner= repo['owner']
            owner_login=owner['login']
            github_repo_contributors = 'https://api.github.com/repos/' + owner_login + '/' + name + '/contributors'

            request = Request(github_repo_contributors)
            request.add_header('Authorization', 'token %s' % token)
            contributors = json.load(urlopen(request))
            owner["site_admin"]=False
            owner["contributions"]=1
            contributors.insert(0,owner)
            for contributor in contributors:
                name = contributor['login']
                if name != username:
                    if name in contributors_dict:
                        contributors_dict[name] += 1
                    else:
                        contributors_dict[name] = 1

        return contributors_dict


    def get_location_users(self, location):

        token =  '3b0f1e62caf99cdfefb8bcb20050b4aff025e165'

        github_location_users = 'https://api.github.com/legacy/user/search/location:' + location

        request = Request(github_location_users)
        request.add_header('Authorization', 'token %s' % token)
        data = json.load(urlopen(request))

        data = data['users']

        location_users = []

        for user in data:
            username = user['username']
            repos = user['repos']
            followers = user['followers_count']
            language = user['language']
            pts = repos*0.6 + followers * 0.4

            location_users.append({ 'username' : username, 'repos' : repos, 'followers' : followers, 'language' : language, 'pts' : pts })

        location_users = sorted(location_users, key=itemgetter('pts'), reverse=True)

        #get only the 10 most relevant, by punctuation, and add their images
        top_users = []
        for i in range(0, 10):
            
            github_user_image = 'https://api.github.com/users/'+location_users[i]['username']
            request = Request(github_user_image)
            request.add_header('Authorization', 'token %s' % token)
            data = json.load(urlopen(request))

            image = data['avatar_url']
            location_users[i]['image'] = image

            top_users.append(location_users[i])

        return top_users


    def get_location_language_statistics(self, location):

        token =  '3b0f1e62caf99cdfefb8bcb20050b4aff025e165'

        github_location_users = 'https://api.github.com/legacy/user/search/location:' + location

        request = Request(github_location_users)
        request.add_header('Authorization', 'token %s' % token)
        data = json.load(urlopen(request))

        data = data['users']

        languages = dict()
        total = 0

        for user in data:
            language = user['language']

	    if language != None:
                total += 1
                if language in languages:
                    languages[language] += 1
                else:
                    languages[language] = 1

        for i in languages:
            languages[i] = "{0:.2f}".format((languages[i]/float(total))*100)

        return get_location_language_statistics 

    def get_repos_by_location(self,location):

        token =  '3b0f1e62caf99cdfefb8bcb20050b4aff025e165'
        github_location_users='https://api.github.com/legacy/user/search/location:' + location
        request = Request(github_location_users)
        request.add_header('Authorization', 'token %s' % token)
        data = json.load(urlopen(request))
        data = data['users']
        repos=[]

        for user in data:
            username=user['username']
            github_user_repos = 'https://api.github.com/users/' + username + '/repos'
            request = Request(github_user_repos)
            request.add_header('Authorization', 'token %s' % token)
            data_repo_user = json.load(urlopen(request))
            repos.extend(data_repo_user)

        
