from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import User, Candidate, Company, BlogPost, Vacancy, Interview

admin.site.register(User, SimpleHistoryAdmin)
admin.site.register(Candidate, SimpleHistoryAdmin)
admin.site.register(Company, SimpleHistoryAdmin)
admin.site.register(BlogPost, SimpleHistoryAdmin)
admin.site.register(Vacancy, SimpleHistoryAdmin)
admin.site.register(Interview, SimpleHistoryAdmin)
