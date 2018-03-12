from django.contrib import admin
from .models import GameStudio, Game, Player, Comment, ReportingMessage

admin.site.register(GameStudio)
admin.site.register(Game)
admin.site.register(Player)
admin.site.register(Comment)

admin.site.register(ReportingMessage)



