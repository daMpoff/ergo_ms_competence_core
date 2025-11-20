from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count
from django.core.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from core.api.src.core.utils.mixins import SwaggerSafeMixin
from modules.competence_core.api.skill_map.models import (
    Skill,
    SkillSynonym,
    Technology,
    TechnologyAlias,
    SkillTechnology,
    SkillCategory,
    TechnologyCategory,
)
from modules.competence_core.api.skill_map.serializers import (
    SkillSerializer,
    SkillCreateSerializer,
    SkillUpdateSerializer,
    SkillSynonymSerializer,
    SkillSynonymCreateSerializer,
    TechnologySerializer,
    TechnologyCreateSerializer,
    TechnologyUpdateSerializer,
    TechnologyAliasSerializer,
    TechnologyAliasCreateSerializer,
    SkillTechnologySerializer,
    SkillTechnologyCreateSerializer,
    SkillTechnologyUpdateSerializer,
    SkillCategoryChoiceSerializer,
    TechnologyCategoryChoiceSerializer,
)
from modules.competence_core.api.skill_map.scripts import (
    clear_technologies,
    run_init_technologies,
)


class SkillViewSet(SwaggerSafeMixin, viewsets.ModelViewSet):
    """
    ViewSet для управления умениями.
    
    Предоставляет полный CRUD функционал для работы с умениями,
    включая поиск, фильтрацию и дополнительные действия.
    
    Требует аутентификации. Список и чтение доступны всем аутентифицированным пользователям,
    создание, обновление и удаление требуют прав администратора.
    """
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'frequency', 'relevance', 'created_at', 'updated_at']
    ordering = ['-frequency', 'name']
    

    @swagger_auto_schema(
        operation_description="Получить список умений",
        security=[{'Bearer': []}],
        responses={
            200: SkillSerializer(many=True),
            401: "Неавторизованный доступ"
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Создать новое умение",
        security=[{'Bearer': []}],
        request_body=SkillCreateSerializer,
        responses={
            201: SkillSerializer,
            400: "Ошибка валидации",
            401: "Неавторизованный доступ"
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Получить умение по ID",
        security=[{'Bearer': []}],
        responses={
            200: SkillSerializer,
            404: "Умение не найдено",
            401: "Неавторизованный доступ"
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Обновить умение",
        security=[{'Bearer': []}],
        request_body=SkillUpdateSerializer,
        responses={
            200: SkillSerializer,
            400: "Ошибка валидации",
            404: "Умение не найдено",
            401: "Неавторизованный доступ"
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Частично обновить умение",
        security=[{'Bearer': []}],
        request_body=SkillUpdateSerializer,
        responses={
            200: SkillSerializer,
            400: "Ошибка валидации",
            404: "Умение не найдено",
            401: "Неавторизованный доступ"
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Удалить умение",
        security=[{'Bearer': []}],
        responses={
            204: "Умение успешно удалено",
            404: "Умение не найдено",
            401: "Неавторизованный доступ"
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от действия"""
        if self.action == 'create':
            return SkillCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return SkillUpdateSerializer
        return SkillSerializer

    def get_queryset(self):
        """Получение queryset с оптимизацией"""
        return self.get_safe_queryset(
            Skill.objects.select_related().prefetch_related('synonyms')
        )

    @swagger_auto_schema(
        operation_description="Получить список доступных категорий умений",
        security=[{'Bearer': []}],
        responses={
            200: SkillCategoryChoiceSerializer(many=True),
            401: "Неавторизованный доступ"
        }
    )
    @action(detail=False, methods=['get'])
    def categories(self, request):
        """Получить список доступных категорий умений"""
        categories = [
            {'value': choice[0], 'label': choice[1]}
            for choice in SkillCategory.choices
        ]
        serializer = SkillCategoryChoiceSerializer(categories, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Получить самые популярные умения",
        security=[{'Bearer': []}],
        manual_parameters=[
            openapi.Parameter(
                'limit',
                openapi.IN_QUERY,
                description="Количество умений для возврата",
                type=openapi.TYPE_INTEGER,
                default=10
            )
        ],
        responses={
            200: SkillSerializer(many=True),
            401: "Неавторизованный доступ"
        }
    )
    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Получить самые популярные умения"""
        limit = int(request.query_params.get('limit', 10))
        queryset = self.get_queryset().order_by('-frequency')[:limit]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Получить умения по категории",
        security=[{'Bearer': []}],
        manual_parameters=[
            openapi.Parameter(
                'category',
                openapi.IN_QUERY,
                description="Категория умений",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: SkillSerializer(many=True),
            400: "Параметр category обязателен",
            401: "Неавторизованный доступ"
        }
    )
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Получить умения по категории"""
        category = request.query_params.get('category')
        if not category:
            return Response(
                {'error': 'Параметр category обязателен'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.get_queryset().filter(category=category)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Получить синонимы умения",
        security=[{'Bearer': []}],
        responses={
            200: SkillSynonymSerializer(many=True),
            404: "Умение не найдено",
            401: "Неавторизованный доступ"
        }
    )
    @action(detail=True, methods=['get'])
    def synonyms(self, request, pk=None):
        """Получить синонимы умения"""
        skill = self.get_object()
        synonyms = skill.synonyms.all()
        serializer = SkillSynonymSerializer(synonyms, many=True)
        return Response(serializer.data)


class SkillSynonymViewSet(SwaggerSafeMixin, viewsets.ModelViewSet):
    """
    ViewSet для управления синонимами умений.
    
    Требует аутентификации. Список и чтение доступны всем аутентифицированным пользователям,
    создание, обновление и удаление требуют прав администратора.
    """
    queryset = SkillSynonym.objects.all()
    serializer_class = SkillSynonymSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['skill']
    search_fields = ['synonym', 'skill__name']
    ordering_fields = ['synonym', 'created_at']
    ordering = ['synonym']

    @swagger_auto_schema(
        operation_description="Получить список синонимов умений",
        security=[{'Bearer': []}],
        responses={
            200: SkillSynonymSerializer(many=True),
            401: "Неавторизованный доступ"
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Создать новый синоним умения",
        security=[{'Bearer': []}],
        request_body=SkillSynonymCreateSerializer,
        responses={
            201: SkillSynonymSerializer,
            400: "Ошибка валидации",
            401: "Неавторизованный доступ"
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от действия"""
        if self.action == 'create':
            return SkillSynonymCreateSerializer
        return SkillSynonymSerializer

    def get_queryset(self):
        """Получение queryset с оптимизацией"""
        return self.get_safe_queryset(
            SkillSynonym.objects.select_related('skill')
        )

    @swagger_auto_schema(
        operation_description="Получить синонимы для конкретного умения",
        security=[{'Bearer': []}],
        manual_parameters=[
            openapi.Parameter(
                'skill_id',
                openapi.IN_QUERY,
                description="ID умения",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: SkillSynonymSerializer(many=True),
            400: "Параметр skill_id обязателен",
            401: "Неавторизованный доступ"
        }
    )
    @action(detail=False, methods=['get'])
    def by_skill(self, request):
        """Получить синонимы для конкретного умения"""
        skill_id = request.query_params.get('skill_id')
        if not skill_id:
            return Response(
                {'error': 'Параметр skill_id обязателен'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.get_queryset().filter(skill_id=skill_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class TechnologyViewSet(SwaggerSafeMixin, viewsets.ModelViewSet):
    """
    ViewSet для управления технологиями.
    
    Предоставляет полный CRUD функционал для работы с технологиями,
    включая иерархическую структуру и связи с умениями.
    
    Требует аутентификации. Список и чтение доступны всем аутентифицированным пользователям,
    создание, обновление и удаление требуют прав администратора.
    """
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'parent_tech']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'popularity', 'relevance', 'created_at', 'updated_at']
    ordering = ['-popularity', 'name']

    @swagger_auto_schema(
        operation_description="Получить список технологий",
        security=[{'Bearer': []}],
        responses={
            200: TechnologySerializer(many=True),
            401: "Неавторизованный доступ"
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Создать новую технологию",
        security=[{'Bearer': []}],
        request_body=TechnologyCreateSerializer,
        responses={
            201: TechnologySerializer,
            400: "Ошибка валидации",
            401: "Неавторизованный доступ"
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от действия"""
        if self.action == 'create':
            return TechnologyCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return TechnologyUpdateSerializer
        return TechnologySerializer

    def get_queryset(self):
        """Получение queryset с оптимизацией"""
        return self.get_safe_queryset(
            Technology.objects.select_related('parent_tech').prefetch_related(
                'aliases', 'child_technologies'
            )
        )

    @swagger_auto_schema(
        operation_description="Получить список доступных категорий технологий",
        security=[{'Bearer': []}],
        responses={
            200: TechnologyCategoryChoiceSerializer(many=True),
            401: "Неавторизованный доступ"
        }
    )
    @action(detail=False, methods=['get'])
    def categories(self, request):
        """Получить список доступных категорий технологий"""
        categories = [
            {'value': choice[0], 'label': choice[1]}
            for choice in TechnologyCategory.choices
        ]
        serializer = TechnologyCategoryChoiceSerializer(categories, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Получить самые популярные технологии",
        security=[{'Bearer': []}],
        manual_parameters=[
            openapi.Parameter(
                'limit',
                openapi.IN_QUERY,
                description="Количество технологий для возврата",
                type=openapi.TYPE_INTEGER,
                default=10
            )
        ],
        responses={
            200: TechnologySerializer(many=True),
            401: "Неавторизованный доступ"
        }
    )
    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Получить самые популярные технологии"""
        limit = int(request.query_params.get('limit', 10))
        queryset = self.get_queryset().order_by('-popularity')[:limit]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Получить технологии по категории",
        security=[{'Bearer': []}],
        manual_parameters=[
            openapi.Parameter(
                'category',
                openapi.IN_QUERY,
                description="Категория технологий",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: TechnologySerializer(many=True),
            400: "Параметр category обязателен",
            401: "Неавторизованный доступ"
        }
    )
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Получить технологии по категории"""
        category = request.query_params.get('category')
        if not category:
            return Response(
                {'error': 'Параметр category обязателен'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.get_queryset().filter(category=category)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Получить иерархическую структуру технологий (корневые элементы)",
        security=[{'Bearer': []}],
        responses={
            200: TechnologySerializer(many=True),
            401: "Неавторизованный доступ"
        }
    )
    @action(detail=False, methods=['get'])
    def hierarchy(self, request):
        """Получить иерархическую структуру технологий"""
        queryset = self.get_queryset().filter(parent_tech__isnull=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Получить дочерние технологии для указанной технологии",
        security=[{'Bearer': []}],
        responses={
            200: TechnologySerializer(many=True),
            404: "Технология не найдена",
            401: "Неавторизованный доступ"
        }
    )
    @action(detail=True, methods=['get'])
    def children(self, request, pk=None):
        """Получить дочерние технологии"""
        technology = self.get_object()
        children = technology.child_technologies.all()
        serializer = self.get_serializer(children, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Получить альтернативные названия технологии",
        security=[{'Bearer': []}],
        responses={
            200: TechnologyAliasSerializer(many=True),
            404: "Технология не найдена",
            401: "Неавторизованный доступ"
        }
    )
    @action(detail=True, methods=['get'])
    def aliases(self, request, pk=None):
        """Получить альтернативные названия технологии"""
        technology = self.get_object()
        aliases = technology.aliases.all()
        serializer = TechnologyAliasSerializer(aliases, many=True)
        return Response(serializer.data)


class TechnologyAliasViewSet(SwaggerSafeMixin, viewsets.ModelViewSet):
    """
    ViewSet для управления альтернативными названиями технологий.
    
    Требует аутентификации. Список и чтение доступны всем аутентифицированным пользователям,
    создание, обновление и удаление требуют прав администратора.
    """
    queryset = TechnologyAlias.objects.all()
    serializer_class = TechnologyAliasSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['technology']
    search_fields = ['alias', 'technology__name']
    ordering_fields = ['alias', 'created_at']
    ordering = ['alias']

    @swagger_auto_schema(
        operation_description="Получить список альтернативных названий технологий",
        security=[{'Bearer': []}],
        responses={
            200: TechnologyAliasSerializer(many=True),
            401: "Неавторизованный доступ"
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Создать новое альтернативное название технологии",
        security=[{'Bearer': []}],
        request_body=TechnologyAliasCreateSerializer,
        responses={
            201: TechnologyAliasSerializer,
            400: "Ошибка валидации",
            401: "Неавторизованный доступ"
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от действия"""
        if self.action == 'create':
            return TechnologyAliasCreateSerializer
        return TechnologyAliasSerializer

    def get_queryset(self):
        """Получение queryset с оптимизацией"""
        return self.get_safe_queryset(
            TechnologyAlias.objects.select_related('technology')
        )

    @swagger_auto_schema(
        operation_description="Получить альтернативные названия для конкретной технологии",
        security=[{'Bearer': []}],
        manual_parameters=[
            openapi.Parameter(
                'technology_id',
                openapi.IN_QUERY,
                description="ID технологии",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: TechnologyAliasSerializer(many=True),
            400: "Параметр technology_id обязателен",
            401: "Неавторизованный доступ"
        }
    )
    @action(detail=False, methods=['get'])
    def by_technology(self, request):
        """Получить альтернативные названия для конкретной технологии"""
        technology_id = request.query_params.get('technology_id')
        if not technology_id:
            return Response(
                {'error': 'Параметр technology_id обязателен'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.get_queryset().filter(technology_id=technology_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SkillTechnologyViewSet(SwaggerSafeMixin, viewsets.ModelViewSet):
    """
    ViewSet для управления связями между умениями и технологиями.
    
    Предоставляет функционал для создания и управления связями
    между умениями и технологиями с указанием релевантности.
    
    Требует аутентификации. Список и чтение доступны всем аутентифицированным пользователям,
    создание, обновление и удаление требуют прав администратора.
    """
    queryset = SkillTechnology.objects.all()
    serializer_class = SkillTechnologySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['skill', 'technology']
    search_fields = ['skill__name', 'technology__name']
    ordering_fields = ['relevance', 'usage_frequency', 'created_at', 'updated_at']
    ordering = ['-relevance', '-usage_frequency']

    @swagger_auto_schema(
        operation_description="Получить список связей умение-технология",
        security=[{'Bearer': []}],
        responses={
            200: SkillTechnologySerializer(many=True),
            401: "Неавторизованный доступ"
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Создать новую связь умение-технология",
        security=[{'Bearer': []}],
        request_body=SkillTechnologyCreateSerializer,
        responses={
            201: SkillTechnologySerializer,
            400: "Ошибка валидации",
            401: "Неавторизованный доступ"
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от действия"""
        if self.action == 'create':
            return SkillTechnologyCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return SkillTechnologyUpdateSerializer
        return SkillTechnologySerializer

    def get_queryset(self):
        """Получение queryset с оптимизацией"""
        return self.get_safe_queryset(
            SkillTechnology.objects.select_related('skill', 'technology')
        )

    @swagger_auto_schema(
        operation_description="Получить технологии для конкретного умения",
        security=[{'Bearer': []}],
        manual_parameters=[
            openapi.Parameter(
                'skill_id',
                openapi.IN_QUERY,
                description="ID умения",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: SkillTechnologySerializer(many=True),
            400: "Параметр skill_id обязателен",
            401: "Неавторизованный доступ"
        }
    )
    @action(detail=False, methods=['get'])
    def by_skill(self, request):
        """Получить технологии для конкретного умения"""
        skill_id = request.query_params.get('skill_id')
        if not skill_id:
            return Response(
                {'error': 'Параметр skill_id обязателен'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.get_queryset().filter(skill_id=skill_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Получить умения для конкретной технологии",
        security=[{'Bearer': []}],
        manual_parameters=[
            openapi.Parameter(
                'technology_id',
                openapi.IN_QUERY,
                description="ID технологии",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: SkillTechnologySerializer(many=True),
            400: "Параметр technology_id обязателен",
            401: "Неавторизованный доступ"
        }
    )
    @action(detail=False, methods=['get'])
    def by_technology(self, request):
        """Получить умения для конкретной технологии"""
        technology_id = request.query_params.get('technology_id')
        if not technology_id:
            return Response(
                {'error': 'Параметр technology_id обязателен'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.get_queryset().filter(technology_id=technology_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Получить высокорелевантные связи умение-технология",
        security=[{'Bearer': []}],
        manual_parameters=[
            openapi.Parameter(
                'min_relevance',
                openapi.IN_QUERY,
                description="Минимальная релевантность (0.0-1.0)",
                type=openapi.TYPE_NUMBER,
                default=0.8
            )
        ],
        responses={
            200: SkillTechnologySerializer(many=True),
            401: "Неавторизованный доступ"
        }
    )
    @action(detail=False, methods=['get'])
    def highly_relevant(self, request):
        """Получить высокорелевантные связи"""
        min_relevance = float(request.query_params.get('min_relevance', 0.8))
        queryset = self.get_queryset().filter(relevance__gte=min_relevance)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Получить часто используемые связи умение-технология",
        security=[{'Bearer': []}],
        manual_parameters=[
            openapi.Parameter(
                'min_frequency',
                openapi.IN_QUERY,
                description="Минимальная частота использования",
                type=openapi.TYPE_INTEGER,
                default=10
            )
        ],
        responses={
            200: SkillTechnologySerializer(many=True),
            401: "Неавторизованный доступ"
        }
    )
    @action(detail=False, methods=['get'])
    def frequently_used(self, request):
        """Получить часто используемые связи"""
        min_frequency = int(request.query_params.get('min_frequency', 10))
        queryset = self.get_queryset().filter(usage_frequency__gte=min_frequency)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class TechnologyMaintenanceViewSet(SwaggerSafeMixin, viewsets.ViewSet):
    """
    Вспомогательный ViewSet для массовых операций над технологиями.

    Используется для очистки таблицы технологий и запуска первичной
    инициализации (init_technologies) из UI.
    """

    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(
        operation_description=(
            "Очистить все технологии и связанные с ними данные.\n\n"
            "Удаляются все записи Technology, а также связанные алиасы и связи умение‑технология."
        ),
        security=[{'Bearer': []}],
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'deleted': openapi.Schema(
                        type=openapi.TYPE_INTEGER,
                        description='Количество удалённых технологий',
                    )
                },
            ),
            401: 'Неавторизованный доступ',
            403: 'Недостаточно прав',
        },
    )
    @action(detail=False, methods=['post'])
    def clear(self, request):
        """Полная очистка таблицы технологий."""
        stats = clear_technologies()
        return Response(stats, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description=(
            "Выполнить первичную инициализацию технологий (management‑команда init_technologies).\n\n"
            "По умолчанию выполняется с параметрами clear=True, update=True."
        ),
        security=[{'Bearer': []}],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'clear': openapi.Schema(
                    type=openapi.TYPE_BOOLEAN,
                    default=True,
                    description='Очистить существующие технологии перед инициализацией',
                ),
                'update': openapi.Schema(
                    type=openapi.TYPE_BOOLEAN,
                    default=True,
                    description='Обновлять уже существующие технологии',
                ),
                'dry_run': openapi.Schema(
                    type=openapi.TYPE_BOOLEAN,
                    default=False,
                    description='Режим проверки без применения изменений',
                ),
            },
            required=[],
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'log': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='Текстовый вывод команды init_technologies',
                    )
                },
            ),
            401: 'Неавторизованный доступ',
            403: 'Недостаточно прав',
            500: 'Ошибка при инициализации технологий',
        },
    )
    @action(detail=False, methods=['post'])
    def init(self, request):
        """Запуск первичной инициализации технологий через init_technologies."""
        clear = bool(request.data.get('clear', True))
        update = bool(request.data.get('update', True))
        dry_run = bool(request.data.get('dry_run', False))

        try:
            result = run_init_technologies(clear=clear, update=update, dry_run=dry_run)
        except Exception:
            # Детали ошибки логируются внутри скрипта.
            return Response(
                {'detail': 'Ошибка при инициализации технологий'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(result, status=status.HTTP_200_OK)