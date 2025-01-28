from django.contrib import admin

from main.models import App, Category, SubCategory, Task, User

# Register your models here.
admin.site.register(App)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Task)
admin.site.register(User)
