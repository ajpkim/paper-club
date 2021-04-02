from django.contrib import admin

from .models import Election, ElectionProposal, Score, Proposal, Vote

admin.site.register([Election, ElectionProposal, Score, Proposal, Vote])
