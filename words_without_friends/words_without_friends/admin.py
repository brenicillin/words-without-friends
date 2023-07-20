from django.contrib import admin
from games.models import Game
from users.models import User

admin.site.register(Game)
admin.site.register(User)