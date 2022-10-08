from django.contrib import admin

# Register your models here.

from .models import Admin
from .models import Student
from .models import Complain


admin.site.register(Admin)
admin.site.register(Complain)
admin.site.register(Student)
