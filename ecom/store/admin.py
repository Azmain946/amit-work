from django.contrib import admin
from .models import *
from django.contrib.auth.models import User

admin.site.register(ImageForCover)
admin.site.register(ImageForLogo)

admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Profile)
admin.site.register(Product_Size)
admin.site.register(AboutWebsite)


class ProfileInLine(admin.StackedInline):
    model = Profile
    fields = ["phone", "address1", "address2", "city", "state", "zipcode", "country", "old_cart"]

class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username", "first_name", "last_name", "email",]
    inlines = [ProfileInLine]

admin.site.unregister(User)

admin.site.register(User, UserAdmin)

