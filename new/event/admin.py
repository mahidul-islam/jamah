from django.contrib import admin
from .models import Event, EventMember, Cost
from polls.models import Question

class PollsInline(admin.TabularInline):
    model = Question
    extra = 1

class EventMemberInline(admin.TabularInline):
    model = EventMember
    extra = 0

class CostInline(admin.TabularInline):
    model = Cost
    extra = 0

class EventAdmin(admin.ModelAdmin):
    inlines = [PollsInline, EventMemberInline, CostInline]

admin.site.register(Event, EventAdmin)
admin.site.register(EventMember)
admin.site.register(Cost)
