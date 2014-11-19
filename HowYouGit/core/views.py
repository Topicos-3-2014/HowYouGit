from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect

from HowYouGit.core.services import GitHubService

def index(request):
    return render(request, 'index.html')

def user(request):
    if request.method == 'POST':
        username = request.POST['username']

        github_service = GitHubService()
        user_ok = github_service.verify_user(username)
        if user_ok:
            repos = github_service.get_user_repos(username)
            languages = github_service.get_user_language_statistics(username)
            contributors = github_service.get_user_contributors_statistics(username)
            who_to_follow = github_service.get_who_to_follow(username)
            size_contributors=len(contributors)
            if size_contributors>0:
                max_contributor=max(contributors.values())
            else:
                max_contributor=0
            print(max_contributor)
            
            return render(request, 'user_stats.html', { 'repos' : repos, 'username' : username, 'languages' : languages, 'contributors' : contributors, 'who_to_follow' : who_to_follow ,'size_contributors' : size_contributors,'max_contributor':max_contributor})
        else:
            return render(request, 'user.html', { 'invalid_message' : 'a valid' })

    else:
        return render(request, 'user.html')

def location(request):
    if request.method == 'POST':
        location = request.POST['location']
        location = location.replace(" ", "+")

        github_service = GitHubService()

        users = github_service.get_location_users(location)

        if len(users) > 0:
            languages = github_service.get_location_language_statistics(location)

            location = location.replace("+", " ")

            return render(request, 'location_stats.html', { 'location' : location, 'users' : users, 'languages' : languages })
        else:
            location = location.replace("+", " ")
            message = 'no github users were found on the location\n'
            return render(request, 'location.html', { 'invalid_message' : message, 'location' : location })
    else:
        return render(request, 'location.html')

def repos_location(request):
    if request.method == 'POST':
        location = request.POST['location']
        location = location.replace(" ", "+")

        github_service = GitHubService()
        repos=github_service.get_repos_by_location(location)
        location = location.replace("+", " ")
        if len(repos) > 0:
            return render(request,'important_repos.html',{'location' : location,'repos' : repos})
        else:
            message = 'no repositories were found on the location\n'
            return render(request, 'repos_location.html', { 'invalid_message' : message, 'location' : location })
    else:
        return render(request, 'repos_location.html')
