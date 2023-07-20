from django.db import models
from users.models import Users

class Games(models.Model):
  user = models.ForeignKey(Users, on_delete=models.CASCADE)
  letters = models.CharField(max_length=10)
  words = models.TextField()
  score = models.IntegerField(default=0)
 