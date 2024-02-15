from django.contrib import admin
from .models import *
# Models registered here for admin
register_models = [audio]
admin.site.register(register_models)