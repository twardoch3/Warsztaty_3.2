from django.contrib import admin

from .models import *

admin.site.register(Person)
admin.site.register(Address)
admin.site.register(Email)
admin.site.register(PhoneNumber)
