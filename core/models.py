from django.db import models

class Constituency(models.Model):
    sl_no = models.IntegerField(unique=True)
    name = models.CharField(max_length=150)
    winning_candidate_2021 = models.CharField(max_length=150)
    winning_party_2021 = models.CharField(max_length=50)
    district = models.CharField(max_length=100)

    live_leading_party = models.CharField(max_length=50, blank=True, null=True) 
    live_status = models.CharField(max_length=50, blank=True, null=True) # E.g., "Leading", "Won"
    live_margin = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} - {self.district}"
