from django.contrib import admin
from .models import Venue
from .models import VenueSearch, Chat, UserProfile, User, Display

class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile
    list_display = ['get_username', 'get_email']

    def get_username(self, obj):
        return obj.username
    def get_email(self,obj):
        return obj.email
    get_username.short_description = 'Username'
    get_email.short_description = 'Email'

    search_fields = ('username', 'email')


class VenueAdmin(admin.ModelAdmin):
    model = Venue
    list_display = ['get_name', 'get_phone']

    def get_name(self, obj):
        return obj.name
    def get_phone(self,obj):
        return obj.phone_number
    get_name.short_description = 'Place'
    get_phone.short_description = 'Phone Number'


class DisplayAdmin(admin.ModelAdmin):
    model = Display
    list_display = ['get_from', 'get_to']

    def get_from(self, obj):
        return obj.displayed_by
    def get_to(self, obj):
        return obj.displayed
    get_from.short_description = 'Displayed By'
    get_to.short_description = 'Displayed'


class VenueSearchAdmin(admin.ModelAdmin):
    model = VenueSearch
    list_display = ['food', 'search_owner', 'where']

    def food(self, obj):
        return obj.query
    def search_owner(self,obj):
        return obj.owner
    def where(self,obj):
        return obj.near
    search_fields = ['query','near']
    food.short_description = 'Food'
    search_owner.short_description = 'User'
    where.short_description = 'Where'


class ChatAdmin(admin.ModelAdmin):
    model = Chat
    list_display = ['from_user', 'to_user', 'message']
    search_fields = ('from_user', 'to_user', 'message')


admin.site.register(Venue, VenueAdmin)
admin.site.register(VenueSearch, VenueSearchAdmin)
admin.site.register(Chat, ChatAdmin)
admin.site.unregister(User)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Display, DisplayAdmin)
