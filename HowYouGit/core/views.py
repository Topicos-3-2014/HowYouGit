from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect

from HowYouGit.core.services import GitHubService

def index(request):
    if request.method == 'POST':
        username = request.POST['username']

        github_service = GitHubService()

        repos = github_service.get_user_repos(username)
        languages = github_service.get_user_language_statistics(username)
        contributors = github_service.get_user_contributors_statistics(username)

        return render(request, 'user.html', { 'repos' : repos, 'username' : username, 'languages' : languages, 'contributors' : contributors })

    else:
        return render(request, 'index.html')

def location(request):
	if request.method == 'POST':
		location = request.POST['location']
		location = location.replace(" ", "+")

		github_service = GitHubService()

		users = github_service.get_location_users(location)
        languages = github_service.get_location_language_statistics(location)

        location = location.replace("+", " ")

		return render(request, 'location_stats.html', { 'location' : location, 'users' : users, 'languages' : languages })
	else:
		return render(request, 'location.html')
