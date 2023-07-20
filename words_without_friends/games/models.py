from django.db import models
from users.models import User

class Game(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  letters = models.CharField(max_length=10)
  words = models.TextField()
  score = models.IntegerField(default=0)
 