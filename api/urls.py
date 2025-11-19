from django.urls import path, include
from rest_framework.routers import DefaultRouter

from modules.competence_core.api.views import (
    CompetenceViewSet, CompetenceComponentViewSet,
    VacancyCompetenceProfileViewSet, VacancyCompetenceViewSet
)

# Создаем роутер для автоматической генерации URL
router = DefaultRouter()
router.register(r'competences', CompetenceViewSet, basename='competence')
router.register(r'competence-components', CompetenceComponentViewSet, basename='competence-component')
router.register(r'vacancy-profiles', VacancyCompetenceProfileViewSet, basename='vacancy-profile')
router.register(r'vacancy-competences', VacancyCompetenceViewSet, basename='vacancy-competence')

urlpatterns = [
    path('skill-map/', include('modules.competence_core.api.skill_map.urls')),
    path('', include(router.urls)),
]