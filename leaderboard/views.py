from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Company


def index(request):
    return render(request, 'leaderboard/index.html', {})


def company(request, company_uid):
    company = get_object_or_404(Company, uid=company_uid)
    return render(request, 'leaderboard/leaders.html', {'leader_set': company.leader_set})
