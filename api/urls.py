from django.urls import path, include

urlpatterns = [
    path('skill-map/', include('modules.competence_core.api.skill_map.urls')),
]