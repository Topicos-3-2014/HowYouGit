from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect

from HowYouGit.core.services import GitHubService

def index(request):
    if request.method == 'POST':
        username = request.POST['username']

        github_service = GitHubService()

        repos = github_service.get_user_repos(username)
        languages = github_service.get_user_language_statistics(username)

        return render(request, 'usuario.html', { 'repos' : repos, 'username' : username, 'languages' : languages })

    else:
        return render(request, 'index.html')
