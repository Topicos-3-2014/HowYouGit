import json, operator
from operator import itemgetter
import requests
from mongomodels import *
from mongoengine import *

class GitHubService:

    def __init__(self):
        self.headers = {'Authorization': 'token %s' % '68b68209f023a81a55c5cec85b38152100badca7'}
        connect('teste_mongo', host='localhost', port=27017)

    def get_user_repos(self, username):

        user = User.objects.filter(username__exact=username).first()

        return user.repositories

    def get_user_language_statistics(self, username):

        user = User.objects.filter(username__exact=username).first()

        languages = dict()
        total = 0

        for repo in user.repositories:

            language = repo.language

            if language != "":
                total += 1
                if language in languages:
                    languages[language] += 1
                else:
                    languages[language] = 1

        for i in languages:
            languages[i] = "{0:.2f}".format((languages[i]/float(total))*100)

        return languages

    def get_user_contributors_statistics(self, username):

        user = User.objects.filter(username__exact=username).first()

        contributors_dict = dict()

        for repo in user.repositories:

            contributors = repo.contributors

            for contributor in contributors:
                if contributor in contributors_dict:
                    contributors_dict[contributor.username] += 1
                else:
                    contributors_dict[contributor.username] = 1

        return contributors_dict

    def get_location_users(self, location):

        users_location = User.objects.filter(location__icontains=location)

        location_users = []

        for user in users_location:
            pts = len(user.repositories)*0.6 + len(user.followers) * 0.4

            location_users.append({ 'username' : user.username, 'repos' : len(user.repositories), 'followers' : len(user.followers), 'pts' : pts })

        location_users = sorted(location_users, key=itemgetter('pts'), reverse=True)

        #get only the 10 most relevant, by punctuation, and add their images
        top_users = []
        max = 10

        if len(location_users) < 10:
            max = len(location_users)

        for i in range(0, max):
            
            github_user_image = 'https://api.github.com/users/'+location_users[i]['username']
            
            response = requests.get(github_user_image, headers=self.headers)
            data = response.json()

            image = data['avatar_url']
            location_users[i]['image'] = image

            top_users.append(location_users[i])

        return top_users


    def get_location_language_statistics(self, location):

        users_location = User.objects.filter(location__icontains=location)

        languages = dict()
        total = 0

        for user in users_location:
            for repo in user.repositories:

                language = repo.language

                if language != "":
                    total += 1
                    if language in languages:
                        languages[language] += 1
                    else:
                        languages[language] = 1

        for i in languages:
            languages[i] = "{0:.2f}".format((languages[i]/float(total))*100)

        return languages 

    def get_repos_by_location(self, location):

        users_location = User.objects.filter(location__contains=location)

        list_repos = []

        for user in users_location:
            for repo in user.repositories:
                
                pts = 0.7*repo.stargazers + 0.2*repo.forks
                list_repos.append({ 'name': repo.name, 'html_url' : repo.url, 'description' : repo.description, 'pts' : pts, 'owner' : user.username })
       
        list_repos = sorted(list_repos, key=itemgetter('pts'), reverse=True)
        
        if len(list_repos)>=10:
            list_repos=list_repos[0:9]
        else:
            list_repos=list_repos[0:(len(list_repos)-1)]

        return list_repos

    def check_if_already_follows(self, list_following, contributor):
    
        for f_user in list_following:
            if contributor.username == f_user['login']:
                return True
        
        return False

    def who_to_follow(self, username):

        user = User.objects.filter(username__exact=username).first()

        who_to_follow = []

        for repo in user.repositories:

            contributors = repo.contributors

            for contributor in contributors:
                github_user_following = 'https://api.github.com/users/' + username + '/following'
                response = requests.get(github_user_following, headers=self.headers)
                following = response.json()

                if self.check_if_already_follows(following, contributor) == False and len(who_to_follow) < 10:
            
                    github_user_image = 'https://api.github.com/users/'+contributor.username
                    
                    response = requests.get(github_user_image, headers=self.headers)
                    data = response.json()

                    image = data['avatar_url']
                    who_to_follow.append({ 'username' : contributor.username, 'image' : image })

        if len(who_to_follow) < 10:
            top_users = self.get_location_users(user.location)

            for top_user in top_users:
                if top_user['username'] != user.username:
                    if len(who_to_follow) >= 10:
                        break
                    else:
                        github_user_image = 'https://api.github.com/users/'+top_user['username']
                    
                        response = requests.get(github_user_image, headers=self.headers)
                        data = response.json()

                        image = data['avatar_url']
                        who_to_follow.append({ 'username' : top_user['username'], 'image' : image })

        return who_to_follow

