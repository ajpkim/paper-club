import string

# from .models import Proposal

# def get_user_clubs(user):
#     return [cm.club for cm in ClubMember.objects.filter(member=user)]

# def get_unscored_proposals(club, user):
#     user_scored_prop = Proposal.objects.filter(score__club=club, score__user=user)
#     return club.proposals.difference(user_scored_prop)

# def get_candidates_dict(club):
#     if club.election:
#         return dict(zip(string.ascii_uppercase,
#                         [c for c in club.election.candidates.all()]))
#     return {}
