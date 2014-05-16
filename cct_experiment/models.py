from django.db import models
from datetime import datetime

# Create your models here.
class EEG(models.Model):
	delta = models.CharField(max_length=2000)
	theta = models.CharField(max_length=2000)
	low_alpha = models.CharField(max_length=2000)
	high_alpha = models.CharField(max_length=2000)
	low_beta = models.CharField(max_length=2000)
	high_beta = models.CharField(max_length=2000)
	low_gamma = models.CharField(max_length=2000)
	mid_gamma = models.CharField(max_length=2000)
	state = models.CharField(max_length=2000)
	answer = models.CharField(max_length=2000)
	created = models.DateTimeField(datetime.now(), auto_now_add=True)
	created.editable=True