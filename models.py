from django.db import models
from django.contrib.auth.models import User

class Candidate(models.Model):
    """
    All candidates are stored here.
    """
    name = models.CharField(max_length=255)
    rank = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

    """
    A function to compute the average score of each candidate after a vote has been cast.
    """
    def get_average_rank(candidate_id):
        candidate = Candidate.objects.get(id=candidate_id)
        rates = Rate.objects.filter(candidate_id=candidate_id)
        total = 0
        for rate in rates:
            total = total + rate.rate
        average = total/len(rates)
        candidate.rank = average
        candidate.save()

class Rate(models.Model):
    """
    Vote against each candidate is held here.
    """
    candidate = models.ForeignKey(Candidate)
    user = models.ForeignKey('auth.user')
    rate = models.SmallIntegerField()

    def __str__(self):
        return self.candidate.name
