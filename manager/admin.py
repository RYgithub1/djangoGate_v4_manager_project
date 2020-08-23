from django.contrib import admin

from manager.models import Person
from manager.models import Manager
from manager.models import Worker


# Register your models here.
admin.site.register(Person)
admin.site.register(Manager)
admin.site.register(Worker)
