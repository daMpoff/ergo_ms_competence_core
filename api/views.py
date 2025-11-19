from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Prefetch
from django.contrib.contenttypes.models import ContentType
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from core.api.src.core.utils.mixins import SwaggerSafeMixin
from modules.competence_core.api.models import (
    Competence, CompetenceComponent, CompetenceLevel,
    VacancyCompetenceProfile, VacancyCompetence
)
from modules.competence_core.api.serializers import (
    CompetenceSerializer, CompetenceCreateSerializer, CompetenceUpdateSerializer,
    CompetenceDetailSerializer, CompetenceComponentSerializer,
    CompetenceComponentCreateSerializer, CompetenceComponentUpdateSerializer,
    VacancyCompetenceProfileSerializer, VacancyCompetenceProfileCreateSerializer,
    VacancyCompetenceProfileDetailSerializer, VacancyCompetenceSerializer,
    VacancyCompetenceCreateSerializer, VacancyCompetenceUpdateSerializer,
    CompetenceLevelChoiceSerializer
)

# Импорт для работы с моделями skill_map (только для чтения данных)
from modules.competence_core.api.skill_map.models import Skill, SkillTechnology


class CompetenceViewSet(SwaggerSafeMixin, viewsets.ModelViewSet):
    """
    ViewSet для управления компетенциями.

    Предоставляет полный CRUD функционал для работы с компетенциями,
    включая компоненты, уровни и связи с вакансиями.

    Требует аутентификации. Список и чтение доступны всем аутентифицированным пользователям,
    создание, обновление и удаление требуют прав администратора.
    """
    queryset = Competence.objects.all()
    serializer_class = CompetenceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['level', 'is_core']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'popularity', 'relevance', 'created_at', 'updated_at']
    ordering = ['-popularity', 'name']

    @swagger_auto_schema(
        operation_description="Получить список компетенций",
        security=[{'Bearer': []}],
        responses={
            200: CompetenceSerializer(many=True),
            401: "Неавторизованный доступ"
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Создать новую компетенцию",
        security=[{'Bearer': []}],
        request_body=CompetenceCreateSerializer,
        responses={
            201: CompetenceSerializer,
            400: "Ошибка валидации",
            401: "Неавторизованный доступ"
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Получить компетенцию по ID",
        security=[{'Bearer': []}],
        responses={
            200: CompetenceDetailSerializer,
            404: "Компетенция не найдена",
            401: "Неавторизованный доступ"
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Обновить компетенцию",
        security=[{'Bearer': []}],
        request_body=CompetenceUpdateSerializer,
        responses={
            200: CompetenceSerializer,
            400: "Ошибка валидации",
            404: "Компетенция не найдена",
            401: "Неавторизованный доступ"
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Частично обновить компетенцию",
        security=[{'Bearer': []}],
        request_body=CompetenceUpdateSerializer,
        responses={
            200: CompetenceSerializer,
            400: "Ошибка валидации",
            404: "Компетенция не найдена",
            401: "Неавторизованный доступ"
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Удалить компетенцию",
        security=[{'Bearer': []}],
        responses={
            204: "Компетенция успешно удалена",
            404: "Компетенция не найдена",
            401: "Неавторизованный доступ"
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от действия"""
        if self.action == 'create':
            return CompetenceCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return CompetenceUpdateSerializer
        elif self.action == 'retrieve':
            return CompetenceDetailSerializer
        return CompetenceSerializer

    def get_queryset(self):
        """Получение queryset с оптимизацией"""
        if self.action == 'retrieve':
            return self.get_safe_queryset(
                Competence.objects.prefetch_related(
                    Prefetch('components', queryset=CompetenceComponent.objects.select_related(
                        'skill', 'skill_technology', 'skill_technology__technology'
                    ))
                )
            )
        return self.get_safe_queryset(Competence.objects.all())

    @swagger_auto_schema(
        operation_description="Получить список доступных уровней компетенций",
        security=[{'Bearer': []}],
        responses={
            200: CompetenceLevelChoiceSerializer(many=True),
            401: "Неавторизованный доступ"
        }
    )
    @action(detail=False, methods=['get'])
    def levels(self, request):
        """Получить список доступных уровней компетенций"""
        levels = [
            {'value': choice[0], 'label': choice[1]}
            for choice in CompetenceLevel.choices
        ]
        serializer = CompetenceLevelChoiceSerializer(levels, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Получить самые популярные компетенции",
        security=[{'Bearer': []}],
        manual_parameters=[
            openapi.Parameter(
                'limit',
                openapi.IN_QUERY,
                description="Количество компетенций для возврата",
                type=openapi.TYPE_INTEGER,
                default=10
            )
        ],
        responses={
            200: CompetenceSerializer(many=True),
            401: "Неавторизованный доступ"
        }
    )
    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Получить самые популярные компетенции"""
        limit = int(request.query_params.get('limit', 10))
        queryset = self.get_queryset().order_by('-popularity')[:limit]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Получить компетенции по уровню",
        security=[{'Bearer': []}],
        manual_parameters=[
            openapi.Parameter(
                'level',
                openapi.IN_QUERY,
                description="Уровень компетенций",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: CompetenceSerializer(many=True),
            400: "Параметр level обязателен",
            401: "Неавторизованный доступ"
        }
    )
    @action(detail=False, methods=['get'])
    def by_level(self, request):
        """Получить компетенции по уровню"""
        level = request.query_params.get('level')
        if not level:
            return Response(
                {'error': 'Параметр level обязателен'},
                status=status.HTTP_400_BAD_REQUEST
            )

        queryset = self.get_queryset().filter(level=level)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Получить компоненты компетенции",
        security=[{'Bearer': []}],
        responses={
            200: CompetenceComponentSerializer(many=True),
            404: "Компетенция не найдена",
            401: "Неавторизованный доступ"
        }
    )
    @action(detail=True, methods=['get'])
    def components(self, request, pk=None):
        """Получить компоненты компетенции"""
        competence = self.get_object()
        components = competence.components.select_related(
            'skill', 'skill_technology', 'skill_technology__technology'
        ).all()
        serializer = CompetenceComponentSerializer(components, many=True)
        return Response(serializer.data)


class CompetenceComponentViewSet(SwaggerSafeMixin, viewsets.ModelViewSet):
    """
    ViewSet для управления компонентами компетенций.

    Предоставляет функционал для работы с компонентами компетенций,
    включая связи с умениями и технологиями.

    Требует аутентификации. Список и чтение доступны всем аутентифицированным пользователям,
    создание, обновление и удаление требуют прав администратора.
    """
    queryset = CompetenceComponent.objects.all()
    serializer_class = CompetenceComponentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['competence', 'skill', 'required_level']
    search_fields = ['competence__name', 'skill__name']
    ordering_fields = ['importance', 'weight', 'created_at']
    ordering = ['-importance', '-weight']

    @swagger_auto_schema(
        operation_description="Получить список компонентов компетенций",
        security=[{'Bearer': []}],
        responses={
            200: CompetenceComponentSerializer(many=True),
            401: "Неавторизованный доступ"
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Создать новый компонент компетенции",
        security=[{'Bearer': []}],
        request_body=CompetenceComponentCreateSerializer,
        responses={
            201: CompetenceComponentSerializer,
            400: "Ошибка валидации",
            401: "Неавторизованный доступ"
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от действия"""
        if self.action == 'create':
            return CompetenceComponentCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return CompetenceComponentUpdateSerializer
        return CompetenceComponentSerializer

    def get_queryset(self):
        """Получение queryset с оптимизацией"""
        return self.get_safe_queryset(
            CompetenceComponent.objects.select_related(
                'competence', 'skill', 'skill_technology', 'skill_technology__technology'
            )
        )

    @swagger_auto_schema(
        operation_description="Получить компоненты для конкретной компетенции",
        security=[{'Bearer': []}],
        manual_parameters=[
            openapi.Parameter(
                'competence_id',
                openapi.IN_QUERY,
                description="ID компетенции",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: CompetenceComponentSerializer(many=True),
            400: "Параметр competence_id обязателен",
            401: "Неавторизованный доступ"
        }
    )
    @action(detail=False, methods=['get'])
    def by_competence(self, request):
        """Получить компоненты для конкретной компетенции"""
        competence_id = request.query_params.get('competence_id')
        if not competence_id:
            return Response(
                {'error': 'Параметр competence_id обязателен'},
                status=status.HTTP_400_BAD_REQUEST
            )

        queryset = self.get_queryset().filter(competence_id=competence_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class VacancyCompetenceProfileViewSet(SwaggerSafeMixin, viewsets.ModelViewSet):
    """
    ViewSet для управления профилями компетенций вакансий.

    Предоставляет функционал для создания и управления профилями
    компетенций для вакансий из различных источников.

    Требует аутентификации. Список и чтение доступны всем аутентифицированным пользователям,
    создание, обновление и удаление требуют прав администратора.
    """
    queryset = VacancyCompetenceProfile.objects.all()
    serializer_class = VacancyCompetenceProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['vacancy_source']
    search_fields = ['vacancy_title']
    ordering_fields = ['vacancy_title', 'created_at', 'updated_at']
    ordering = ['-created_at']

    @swagger_auto_schema(
        operation_description="Получить список профилей компетенций вакансий",
        security=[{'Bearer': []}],
        responses={
            200: VacancyCompetenceProfileSerializer(many=True),
            401: "Неавторизованный доступ"
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Создать новый профиль компетенций вакансии",
        security=[{'Bearer': []}],
        request_body=VacancyCompetenceProfileCreateSerializer,
        responses={
            201: VacancyCompetenceProfileSerializer,
            400: "Ошибка валидации",
            401: "Неавторизованный доступ"
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Получить профиль компетенций вакансии по ID",
        security=[{'Bearer': []}],
        responses={
            200: VacancyCompetenceProfileDetailSerializer,
            404: "Профиль не найден",
            401: "Неавторизованный доступ"
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от действия"""
        if self.action == 'create':
            return VacancyCompetenceProfileCreateSerializer
        elif self.action == 'retrieve':
            return VacancyCompetenceProfileDetailSerializer
        return VacancyCompetenceProfileSerializer

    def get_queryset(self):
        """Получение queryset с оптимизацией"""
        if self.action == 'retrieve':
            return self.get_safe_queryset(
                VacancyCompetenceProfile.objects.prefetch_related(
                    Prefetch('vacancy_competences',
                           queryset=VacancyCompetence.objects.select_related('competence'))
                )
            )
        return self.get_safe_queryset(VacancyCompetenceProfile.objects.all())

    @swagger_auto_schema(
        operation_description="Получить профили по источнику вакансий",
        security=[{'Bearer': []}],
        manual_parameters=[
            openapi.Parameter(
                'source',
                openapi.IN_QUERY,
                description="Источник вакансий",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: VacancyCompetenceProfileSerializer(many=True),
            400: "Параметр source обязателен",
            401: "Неавторизованный доступ"
        }
    )
    @action(detail=False, methods=['get'])
    def by_source(self, request):
        """Получить профили по источнику вакансий"""
        source = request.query_params.get('source')
        if not source:
            return Response(
                {'error': 'Параметр source обязателен'},
                status=status.HTTP_400_BAD_REQUEST
            )

        queryset = self.get_queryset().filter(vacancy_source=source)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Получить компетенции профиля вакансии",
        security=[{'Bearer': []}],
        responses={
            200: VacancyCompetenceSerializer(many=True),
            404: "Профиль не найден",
            401: "Неавторизованный доступ"
        }
    )
    @action(detail=True, methods=['get'])
    def competences(self, request, pk=None):
        """Получить компетенции профиля вакансии"""
        profile = self.get_object()
        competences = profile.vacancy_competences.select_related(
            'competence'
        ).order_by('priority', '-weight')
        serializer = VacancyCompetenceSerializer(competences, many=True)
        return Response(serializer.data)


class VacancyCompetenceViewSet(SwaggerSafeMixin, viewsets.ModelViewSet):
    """
    ViewSet для управления связями вакансий и компетенций.

    Предоставляет функционал для создания и управления связями
    между профилями вакансий и компетенциями.

    Требует аутентификации. Список и чтение доступны всем аутентифицированным пользователям,
    создание, обновление и удаление требуют прав администратора.
    """
    queryset = VacancyCompetence.objects.all()
    serializer_class = VacancyCompetenceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['vacancy_profile', 'competence', 'is_mandatory']
    search_fields = ['competence__name', 'vacancy_profile__vacancy_title']
    ordering_fields = ['priority', 'weight', 'created_at']
    ordering = ['priority', '-weight']

    @swagger_auto_schema(
        operation_description="Получить список связей вакансий и компетенций",
        security=[{'Bearer': []}],
        responses={
            200: VacancyCompetenceSerializer(many=True),
            401: "Неавторизованный доступ"
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Создать новую связь вакансия-компетенция",
        security=[{'Bearer': []}],
        request_body=VacancyCompetenceCreateSerializer,
        responses={
            201: VacancyCompetenceSerializer,
            400: "Ошибка валидации",
            401: "Неавторизованный доступ"
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от действия"""
        if self.action == 'create':
            return VacancyCompetenceCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return VacancyCompetenceUpdateSerializer
        return VacancyCompetenceSerializer

    def get_queryset(self):
        """Получение queryset с оптимизацией"""
        return self.get_safe_queryset(
            VacancyCompetence.objects.select_related(
                'vacancy_profile', 'competence'
            )
        )

    @swagger_auto_schema(
        operation_description="Получить связи для конкретного профиля вакансии",
        security=[{'Bearer': []}],
        manual_parameters=[
            openapi.Parameter(
                'profile_id',
                openapi.IN_QUERY,
                description="ID профиля вакансии",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: VacancyCompetenceSerializer(many=True),
            400: "Параметр profile_id обязателен",
            401: "Неавторизованный доступ"
        }
    )
    @action(detail=False, methods=['get'])
    def by_profile(self, request):
        """Получить связи для конкретного профиля вакансии"""
        profile_id = request.query_params.get('profile_id')
        if not profile_id:
            return Response(
                {'error': 'Параметр profile_id обязателен'},
                status=status.HTTP_400_BAD_REQUEST
            )

        queryset = self.get_queryset().filter(vacancy_profile_id=profile_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Получить обязательные компетенции",
        security=[{'Bearer': []}],
        responses={
            200: VacancyCompetenceSerializer(many=True),
            401: "Неавторизованный доступ"
        }
    )
    @action(detail=False, methods=['get'])
    def mandatory(self, request):
        """Получить обязательные компетенции"""
        queryset = self.get_queryset().filter(is_mandatory=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Получить высокоприоритетные компетенции",
        security=[{'Bearer': []}],
        manual_parameters=[
            openapi.Parameter(
                'max_priority',
                openapi.IN_QUERY,
                description="Максимальный приоритет (включительно)",
                type=openapi.TYPE_INTEGER,
                default=2
            )
        ],
        responses={
            200: VacancyCompetenceSerializer(many=True),
            401: "Неавторизованный доступ"
        }
    )
    @action(detail=False, methods=['get'])
    def high_priority(self, request):
        """Получить высокоприоритетные компетенции"""
        max_priority = int(request.query_params.get('max_priority', 2))
        queryset = self.get_queryset().filter(priority__lte=max_priority)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)