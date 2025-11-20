from django.urls import path, include
from rest_framework.routers import DefaultRouter
from modules.competence_core.api.skill_map.views import (
    SkillViewSet,
    SkillSynonymViewSet,
    TechnologyViewSet,
    TechnologyAliasViewSet,
    SkillTechnologyViewSet,
    TechnologyMaintenanceViewSet,
)

# Создаем роутер для автоматической генерации URL
router = DefaultRouter()
router.register(r'skills', SkillViewSet, basename='skill')
router.register(r'skill-synonyms', SkillSynonymViewSet, basename='skill-synonym')
router.register(r'technologies', TechnologyViewSet, basename='technology')
router.register(r'technology-aliases', TechnologyAliasViewSet, basename='technology-alias')
router.register(r'skill-technologies', SkillTechnologyViewSet, basename='skill-technology')
router.register(
    r'technology-maintenance',
    TechnologyMaintenanceViewSet,
    basename='technology-maintenance',
)

urlpatterns = [
    path('', include(router.urls)),
]