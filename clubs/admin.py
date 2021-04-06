from django.contrib import admin

from .models import Candidate, Club, ClubMember, Election, Meeting, Score, Proposal, Vote

admin.site.register([Candidate, Club, ClubMember, Election, Meeting, Score, Proposal, Vote])
