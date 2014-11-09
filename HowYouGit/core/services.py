import urllib, urllib2, json, operator,datetime
from urllib2 import Request, urlopen
from operator import itemgetter


class GitHubService:

    def get_user_repos(self, username):

        token =  '68b68209f023a81a55c5cec85b38152100badca7'

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

        token =  '68b68209f023a81a55c5cec85b38152100badca7'

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

        token =  '68b68209f023a81a55c5cec85b38152100badca7'

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

    def check_user_active(self,user):
        i = datetime.datetime.now()
        update_at=user["updated_at"]
        year =update_at[0:4]
        year_int=int(year)
        month=update_at[5:7]
        month_int=int(month)
        if i.year==year_int:
            if i.month-month_int<3:
                return True
        return False;

    def get_location_users(self, location):

        token =  '68b68209f023a81a55c5cec85b38152100badca7'
        count_top_users=0;
        i=0;
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
        while i <len(location_users) and count_top_users<10 :
            
            github_user = 'https://api.github.com/users/'+location_users[i]['username']
            request = Request(github_user)
            request.add_header('Authorization', 'token %s' % token)
            user = json.load(urlopen(request))
            if self.check_user_active(user)==True:
                image = user['avatar_url']
                location_users[i]['image'] = image
                top_users.append(location_users[i])
                count_top_users+=1
            i+=1


        return top_users


    def get_location_language_statistics(self, location):

        token =  '68b68209f023a81a55c5cec85b38152100badca7'

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

        return languages 

    def get_repos_by_location(self,location):

        token =  '68b68209f023a81a55c5cec85b38152100badca7'
        github_location_users='https://api.github.com/legacy/user/search/location:' + location
        request = Request(github_location_users)
        request.add_header('Authorization', 'token %s' % token)
        data = json.load(urlopen(request))
        data = data['users']
        repos=[]
        list_repos=[]
        i=0
        counter=0
        size_iteration=30
        if len(data)<30:
            size_iteration=len(data)

        for counter in range(0,size_iteration):
            user=data[counter]
            username=user['username']
            github_user_repos = 'https://api.github.com/users/' + username + '/repos'
            request = Request(github_user_repos)
            request.add_header('Authorization', 'token %s' % token)
            data_repos_user = json.load(urlopen(request))
            repos.extend(data_repos_user)
            counter=counter+1
        for repo in repos:
            #owner_login=repo['owner']['login']
            #github_user_repo = 'https://api.github.com/repos/' + owner_login + '/'+repo['name']
            #request = Request(github_user_repo)
            #request.add_header('Authorization', 'token %s' % token)
            #data_repo_user = json.load(urlopen(request))
            #watchers_count=data_repo_user['subscribers_count']
            name=repo['name']
            html_url=repo['html_url']
            description=repo['description']
            pts=0.7* repo['stargazers_count']+0.2*repo['forks_count']
            list_repos.append({ 'name': name, 'html_url' : html_url, 'description' : description, 'pts' : pts })
            i=i+1
    
        list_repos = sorted(list_repos, key=itemgetter('pts'), reverse=True)
        if len(list_repos)>=10:
            list_repos=list_repos[0:9]
        else:
            list_repos=list_repos[0:(len(list_repos)-1)]

        return list_repos
    

    def check_contributors_list(self,list_contributors,contributor,username):
        if contributor['login']==username:
            return True;
        for c in list_contributors:
            if c["login"]==contributor["login"]:
                return True;
        
        return False;
    



    def get_who_to_follow(self,username):
        

        list_who_to_follow=[]
        list_contributors=[]
        list_org_members=[]
        boolean_contrib=True
        counter_rem_followers=0
        token =  '3b0f1e62caf99cdfefb8bcb20050b4aff025e165'
        
        github_user_repos = 'https://api.github.com/users/' + username + '/repos?type=all'
        request = Request(github_user_repos)
        request.add_header('Authorization', 'token %s' % token)
        repos = json.load(urlopen(request))

        github_followers='https://api.github.com/users/'+username + '/following'
        request = Request(github_followers)
        request.add_header('Authorization', 'token %s' % token)
        followers = json.load(urlopen(request))
        
        github_user_orgs = 'https://api.github.com/users/'+ username +'/orgs'
        request = Request(github_user_orgs)
        request.add_header('Authorization', 'token %s' % token)
        orgs = json.load(urlopen(request))


        for repo in repos:
            
            name = repo['name']
            owner= repo['owner']
            owner_login=owner['login']
            owner["site_admin"]=False
            owner["contributions"]=1

            github_repo_contributors = 'https://api.github.com/repos/' + owner_login + '/' + name + '/contributors'
            request = Request(github_repo_contributors)
            request.add_header('Authorization', 'token %s' % token)
            contributors=(json.load(urlopen(request)))
            
            if username!=owner_login:
                contributors.append(owner)
            
            for contributor in contributors:
                if self.check_contributors_list(list_contributors,contributor,username) ==False:
                    list_contributors.append(contributor)



        
        for contributor in list_contributors:
            if self.check_contributors_list(followers,contributor,username)==False:
                list_who_to_follow.append({ 'login' : contributor['login'],'image' : contributor['avatar_url']})

        
        if len(list_who_to_follow)>=10:
            list_who_to_follow=list_who_to_follow[0:10]
        else:
            counter_rem_followers=len(list_who_to_follow)
            for org in orgs:
                github_org_members = 'https://api.github.com/orgs/'+org['login'] +'/members'
                request = Request(github_org_members)
                request.add_header('Authorization', 'token %s' % token)
                org_members = json.load(urlopen(request))
                for org_member in org_members:
                    if self.check_contributors_list(list_org_members,org_member,username)==False:
                        list_org_members.append({ 'login' : org_member['login'],'image' : org_member['avatar_url']})
                    if self.check_contributors_list(followers,org_member,username)==False:
                        if self.check_contributors_list(list_who_to_follow,org_member,username)==False:
                            if(counter_rem_followers>=10):
                                break;
                                break;
                            else:    
                                list_who_to_follow.append({ 'login' : org_member['login'],'image' : org_member['avatar_url']})
                                counter_rem_followers+=1

        return list_who_to_follow



    