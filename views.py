from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template import loader
from django.utils import timezone
from django.shortcuts import render_to_response
import requests, gspread, os, json
from oauth2client.client import SignedJwtAssertionCredentials
from .models import Candidate, Rate

"""
Ajax callback function to get Candidate names similar to names entered in textfield.
This is the callbackfor the autocomplete
"""
def get_candidate(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        rates = Rate.objects.filter(user=request.user)
        candidate_ids = []
        for rate in rates:
            candidate_ids.append(rate.candidate.id)
        candidates = Candidate.objects.filter(name__icontains=q).exclude(id__in=candidate_ids)[:20]
        results = []
        for candidate in candidates:
            candidate_json = {}
            candidate_json = candidate.name
            results.append(candidate_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

"""
Plinterview home page. This is where the rank is displayed if you are logged in.
"""
def plinterview(request):
    template = loader.get_template('plinterview/home.html')
    if request.user.id:
        candidates = get_ranked_list(request.user)
        excluded_ids = get_not_voted_candidates(request.user)
    else:
        candidates = []
        excluded_ids = []
    return HttpResponse(template.render({'candidates': candidates, 'excluded_ids': excluded_ids}, request))

def login_view(request):
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/interview')

    return render_to_response('home.html',{'username': username}, context_instance=RequestContext(request))

def signup_view(request):
    if request.POST:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect('/interview')
    logout(request)
    user = User.objects.create_user('username', 'email', 'password')
    login(request, user)
    return render_to_response('home.html',{'username': username}, context_instance=RequestContext(request))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/interview')

"""
This is the form where you can vote against candidates. An autocomplete textbox is present to search your candidate name.
Rated candidates will appear on top after page load.
"""
def form(request):
    template = loader.get_template('plinterview/form.html')
    if not request.user.id:
        return HttpResponseRedirect('/interview')
    try:
        rates = Rate.objects.filter(user=request.user)
    except Rate.DoesNotExist:
        rates = False
    return HttpResponse(template.render({'rates': rates}, request))

"""
Vote casting function
"""
def vote(request):
    if request.POST:
        name = request.POST.get('candidate')
        vote = request.POST.get('vote')
        candidate = Candidate.objects.get(name=name)
        rate = Rate(candidate=candidate, user=request.user, rate=vote)
        rate.save()
        Candidate.get_average_rank(candidate.id)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER','/interview/rankings'))

"""
List all candidates if not logged in. List all candidates with your score and a button to
vote for those candidates that haven't been voted on.
"""
def list(request):
    template = loader.get_template('plinterview/list.html')
    try:
        if request.user.id:
            rates = Rate.objects.filter(user=request.user)
            candidate_ids = []
            for rate in rates:
                candidate_ids.append(rate.candidate.id)
            candidates = Candidate.objects.all().exclude(id__in=candidate_ids)
        else:
            candidates = Candidate.objects.all()
            rates = False
    except Rate.DoesNotExist:
        rates = False
        candidates = Candidate.objects.all()
    return HttpResponse(template.render({'rates': rates, 'candidates': candidates}, request))

"""
Ranked candidates' list.
"""
def get_ranked_list(user):
    candidates = Candidate.objects.all().order_by('-rank')
    return candidates

"""
Candidates who hasn't been voted on by current user.
"""
def get_not_voted_candidates(user):
    rates = Rate.objects.filter(user=user)
    candidate_ids = []
    for rate in rates:
        candidate_ids.append(rate.candidate.id)
    not_voted_candidates = Candidate.objects.all().order_by('-rank').exclude(id__in=candidate_ids)
    excluded_ids = []
    for candidate in not_voted_candidates:
        excluded_ids.append(candidate.id)
    return excluded_ids
