from django.contrib import admin
from .models import Jamah, JamahMember

class JamahMemberInline(admin.TabularInline):
    model = JamahMember
    extra = 0

class JamahAdmin(admin.ModelAdmin):
    inlines = [JamahMemberInline]

admin.site.register(Jamah, JamahAdmin)

admin.site.register(JamahMember)
