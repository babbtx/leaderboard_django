import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from django.db import transaction
from .models import Company

def index(request):
    return render(request, 'leaderboard/index.html', {})


@require_http_methods(['POST', 'GET'])
def company(request, company_uid):
    if request.method == 'POST':
        return update_company_leaders(request, company_uid)
    else:
        return render_company_leaders(request, company_uid)


# this is an HTML response of all company leaders
def render_company_leaders(request, company_uid):
    pair = Company.objects.get_or_create(uid=company_uid)
    company = pair[0]
    last_updated = company.updated if pair[1] == False else None
    return render(request, 'leaderboard/leaders.html',
                  {'leader_set': company.leader_set,
                  'company_uid': company.uid,
                  'last_updated': last_updated})


# this is a JSON API for company leaders
def update_company_leaders(request, company_uid):
    if request.META['CONTENT_TYPE'] != 'application/json':
        return HttpResponseBadRequest(request.META['CONTENT_TYPE'], status=415)

    jarray = json.loads(request.body.decode('UTF-8'))

    # handle the input
    with transaction.atomic():
        company = Company.objects.get_or_create(uid=company_uid)[0]
        for jleader in jarray:
           leader = company.leader_set.get_or_create(name=jleader['name'])[0]
           leader.score_set.create(category='closed', score=jleader['score'])
        company.save() # force timestamp and transaction collision
    
    # compile a response
    # JSON of name and score for every leader
    data = []
    for leader in company.leader_set.all():
        data.append({'name': leader.name, 'score': leader.closed_score()})
    
    return JsonResponse(data, safe=False)

