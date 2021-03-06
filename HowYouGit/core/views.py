from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect

from HowYouGit.core.services import GitHubService

def index(request):
    return render(request, 'index.html')

def user(request):
    if request.method == 'POST':
        username = request.POST['username']

        github_service = GitHubService()
        repos = github_service.get_user_repos(username)
        languages = github_service.get_user_language_statistics(username)
        contributors = github_service.get_user_contributors_statistics(username)
        who_to_follow = github_service.who_to_follow(username)

        return render(request, 'user_stats.html', { 'repos' : repos, 'username' : username, 'languages' : languages, 'contributors' : contributors, 'who_to_follow' : who_to_follow })
    else:
        return render(request, 'user.html')

def location(request):
    if request.method == 'POST':
        location = request.POST['location']
        #location = location.replace(" ", "+")

        github_service = GitHubService()

        users = github_service.get_location_users(location)

        languages = github_service.get_location_language_statistics(location)

        repos = github_service.get_repos_by_location(location)

        #location = location.replace("+", " ")

        return render(request, 'location_stats.html', { 'location' : location, 'users' : users, 'languages' : languages, 'repos' : repos })
    else:
        return render(request, 'location.html')
