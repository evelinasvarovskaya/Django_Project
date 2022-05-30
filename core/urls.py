from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from api.views.candidate import CandidateViewSet
from api.views.company import CompanyViewSet
from api.views.blogpost import BlogPostViewSet
from api.views.interviews import InterviewViewSet
from api.views.user import UserViewSet
from api.views.vacancy import VacancyViewSet

router = DefaultRouter()
router.register('candidates', CandidateViewSet)
router.register('companies', CompanyViewSet)
router.register('posts', BlogPostViewSet)
router.register('vacancies', VacancyViewSet)
router.register('interviews', InterviewViewSet)
router.register('user', UserViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
