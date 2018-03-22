from django.contrib import admin
from .models import GameStudio, Game, Player, Comment, ReportingMessage, ApprovalRequest

class ReportingMessageAdmin(admin.ModelAdmin):
    list_display = ('reporter','player', 'message',)

class ApprovalRequestAdmin(admin.ModelAdmin):
    list_display = ('player', 'message',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('player', 'comment',)

admin.site.register(GameStudio)
admin.site.register(Game)
admin.site.register(Player)
admin.site.register(Comment)

admin.site.register(ReportingMessage, ReportingMessageAdmin)
admin.site.register(ApprovalRequest)



