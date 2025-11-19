from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType

from modules.competence_core.api.models import (
    Competence, CompetenceComponent, CompetenceLevel,
    VacancyCompetenceProfile, VacancyCompetence
)


class CompetenceSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Competence"""
    level_display = serializers.CharField(source='get_level_display', read_only=True)
    components_count = serializers.SerializerMethodField()

    class Meta:
        model = Competence
        ref_name = 'Competence'
        fields = [
            'id', 'name', 'description', 'level', 'level_display', 'popularity',
            'relevance', 'is_core', 'components_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_components_count(self, obj):
        """Получить количество компонентов компетенции"""
        return obj.components.count()


class CompetenceCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания компетенции"""

    class Meta:
        model = Competence
        ref_name = 'CompetenceCreate'
        fields = ['name', 'description', 'level', 'popularity', 'relevance', 'is_core']

    def validate_name(self, value):
        """Валидация названия компетенции"""
        if not value or not value.strip():
            raise serializers.ValidationError("Название компетенции не может быть пустым")
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Название компетенции должно содержать минимум 2 символа")
        return value.strip()

    def validate_relevance(self, value):
        """Валидация релевантности"""
        if value < 0.0 or value > 1.0:
            raise serializers.ValidationError("Релевантность должна быть в диапазоне от 0.0 до 1.0")
        return value

    def validate_popularity(self, value):
        """Валидация популярности"""
        if value < 0:
            raise serializers.ValidationError("Популярность не может быть отрицательной")
        return value


class CompetenceUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления компетенции"""

    class Meta:
        model = Competence
        ref_name = 'CompetenceUpdate'
        fields = ['name', 'description', 'level', 'popularity', 'relevance', 'is_core']


class CompetenceComponentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели CompetenceComponent"""
    competence_name = serializers.CharField(source='competence.name', read_only=True)
    skill_name = serializers.CharField(source='skill.name', read_only=True)
    skill_category = serializers.CharField(source='skill.category', read_only=True)
    skill_technology_info = serializers.SerializerMethodField()
    required_level_display = serializers.CharField(source='get_required_level_display', read_only=True)

    class Meta:
        model = CompetenceComponent
        ref_name = 'CompetenceComponent'
        fields = [
            'id', 'competence', 'competence_name', 'skill', 'skill_name',
            'skill_category', 'skill_technology', 'skill_technology_info',
            'importance', 'required_level', 'required_level_display',
            'weight', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_skill_technology_info(self, obj):
        """Получить информацию о связи умение-технология"""
        if obj.skill_technology:
            return {
                'id': obj.skill_technology.id,
                'technology_name': obj.skill_technology.technology.name,
                'technology_category': obj.skill_technology.technology.category,
                'usage_frequency': obj.skill_technology.usage_frequency,
                'relevance': obj.skill_technology.relevance
            }
        return None


class CompetenceComponentCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания компонента компетенции"""

    class Meta:
        model = CompetenceComponent
        ref_name = 'CompetenceComponentCreate'
        fields = [
            'competence', 'skill', 'skill_technology', 'importance',
            'required_level', 'weight'
        ]

    def validate_importance(self, value):
        """Валидация важности"""
        if value < 0.0 or value > 1.0:
            raise serializers.ValidationError("Важность должна быть в диапазоне от 0.0 до 1.0")
        return value

    def validate_weight(self, value):
        """Валидация веса"""
        if value < 0.0:
            raise serializers.ValidationError("Вес не может быть отрицательным")
        return value

    def validate(self, attrs):
        """Комплексная валидация"""
        skill = attrs.get('skill')
        skill_technology = attrs.get('skill_technology')

        # Если указана связь умение-технология, проверить соответствие умения
        if skill_technology and skill and skill_technology.skill_id != skill.id:
            raise serializers.ValidationError({
                'skill_technology': 'Связь умение-технология должна соответствовать выбранному умению'
            })

        return attrs


class CompetenceComponentUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления компонента компетенции"""

    class Meta:
        model = CompetenceComponent
        ref_name = 'CompetenceComponentUpdate'
        fields = ['importance', 'required_level', 'weight']


class VacancyCompetenceProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для модели VacancyCompetenceProfile"""
    vacancy_info = serializers.SerializerMethodField()
    competences_count = serializers.SerializerMethodField()

    class Meta:
        model = VacancyCompetenceProfile
        ref_name = 'VacancyCompetenceProfile'
        fields = [
            'id', 'content_type', 'object_id', 'vacancy_title', 'vacancy_source',
            'vacancy_info', 'competences_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_vacancy_info(self, obj):
        """Получить информацию о вакансии"""
        try:
            vacancy = obj.vacancy
            if vacancy:
                return {
                    'id': obj.object_id,
                    'title': vacancy.title if hasattr(vacancy, 'title') else obj.vacancy_title,
                    'company': getattr(vacancy, 'company_name', None),
                    'source': obj.vacancy_source
                }
        except Exception:
            pass
        return None

    def get_competences_count(self, obj):
        """Получить количество компетенций в профиле"""
        return obj.competences.count()


class VacancyCompetenceProfileCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания профиля компетенций вакансии"""

    class Meta:
        model = VacancyCompetenceProfile
        ref_name = 'VacancyCompetenceProfileCreate'
        fields = ['content_type', 'object_id', 'vacancy_title', 'vacancy_source']

    def validate_content_type(self, value):
        """Валидация типа контента"""
        # Проверить, что указанный content_type существует
        if not ContentType.objects.filter(pk=value.id).exists():
            raise serializers.ValidationError("Указанный тип контента не существует")
        return value

    def validate(self, attrs):
        """Комплексная валидация"""
        content_type = attrs.get('content_type')
        object_id = attrs.get('object_id')

        # Проверить уникальность профиля для данной вакансии
        if content_type and object_id:
            if VacancyCompetenceProfile.objects.filter(
                content_type=content_type,
                object_id=object_id
            ).exists():
                raise serializers.ValidationError("Профиль для данной вакансии уже существует")

        # Проверить существование объекта вакансии
        try:
            vacancy_obj = content_type.get_object_for_this_type(pk=object_id)
            if not vacancy_obj:
                raise serializers.ValidationError("Указанная вакансия не существует")
        except Exception:
            raise serializers.ValidationError("Указанная вакансия не существует")

        return attrs


class VacancyCompetenceSerializer(serializers.ModelSerializer):
    """Сериализатор для модели VacancyCompetence"""
    competence_name = serializers.CharField(source='competence.name', read_only=True)
    competence_level = serializers.CharField(source='competence.level', read_only=True)
    vacancy_title = serializers.CharField(source='vacancy_profile.vacancy_title', read_only=True)
    required_level_display = serializers.CharField(source='get_required_level_display', read_only=True)

    class Meta:
        model = VacancyCompetence
        ref_name = 'VacancyCompetence'
        fields = [
            'id', 'vacancy_profile', 'competence', 'competence_name',
            'competence_level', 'vacancy_title', 'priority', 'required_level',
            'required_level_display', 'is_mandatory', 'weight', 'created_at'
        ]
        read_only_fields = ['created_at']


class VacancyCompetenceCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания связи вакансия-компетенция"""

    class Meta:
        model = VacancyCompetence
        ref_name = 'VacancyCompetenceCreate'
        fields = [
            'vacancy_profile', 'competence', 'priority', 'required_level',
            'is_mandatory', 'weight'
        ]

    def validate_priority(self, value):
        """Валидация приоритета"""
        if value < 0:
            raise serializers.ValidationError("Приоритет не может быть отрицательным")
        return value

    def validate_weight(self, value):
        """Валидация веса"""
        if value < 0.0 or value > 1.0:
            raise serializers.ValidationError("Вес должен быть в диапазоне от 0.0 до 1.0")
        return value

    def validate(self, attrs):
        """Комплексная валидация"""
        vacancy_profile = attrs.get('vacancy_profile')
        competence = attrs.get('competence')

        # Проверить уникальность связи
        if vacancy_profile and competence:
            if VacancyCompetence.objects.filter(
                vacancy_profile=vacancy_profile,
                competence=competence
            ).exists():
                raise serializers.ValidationError("Данная компетенция уже добавлена к профилю вакансии")

        return attrs


class VacancyCompetenceUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления связи вакансия-компетенция"""

    class Meta:
        model = VacancyCompetence
        ref_name = 'VacancyCompetenceUpdate'
        fields = ['priority', 'required_level', 'is_mandatory', 'weight']


# Сериализаторы для выбора категорий
class CompetenceLevelChoiceSerializer(serializers.Serializer):
    """Сериализатор для выбора уровня компетенции"""

    class Meta:
        ref_name = 'CompetenceLevelChoice'

    value = serializers.CharField()
    label = serializers.CharField()


class CompetenceDetailSerializer(serializers.ModelSerializer):
    """Расширенный сериализатор компетенции с компонентами"""
    level_display = serializers.CharField(source='get_level_display', read_only=True)
    components = serializers.SerializerMethodField()
    components_count = serializers.SerializerMethodField()

    class Meta:
        model = Competence
        ref_name = 'CompetenceDetail'
        fields = [
            'id', 'name', 'description', 'level', 'level_display', 'popularity',
            'relevance', 'is_core', 'components', 'components_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_components(self, obj):
        """Получить компоненты компетенции с полной информацией"""
        components = obj.components.select_related(
            'skill', 'skill_technology__technology'
        ).all()
        return CompetenceComponentSerializer(components, many=True).data

    def get_components_count(self, obj):
        """Получить количество компонентов компетенции"""
        return obj.components.count()


class VacancyCompetenceProfileDetailSerializer(serializers.ModelSerializer):
    """Расширенный сериализатор профиля вакансии с компетенциями"""
    vacancy_info = serializers.SerializerMethodField()
    competences = serializers.SerializerMethodField()
    competences_count = serializers.SerializerMethodField()

    class Meta:
        model = VacancyCompetenceProfile
        ref_name = 'VacancyCompetenceProfileDetail'
        fields = [
            'id', 'content_type', 'object_id', 'vacancy_title', 'vacancy_source',
            'vacancy_info', 'competences', 'competences_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_vacancy_info(self, obj):
        """Получить информацию о вакансии"""
        try:
            vacancy = obj.vacancy
            if vacancy:
                return {
                    'id': obj.object_id,
                    'title': vacancy.title if hasattr(vacancy, 'title') else obj.vacancy_title,
                    'company': getattr(vacancy, 'company_name', None),
                    'source': obj.vacancy_source,
                    'url': getattr(vacancy, 'url', None),
                    'city': getattr(vacancy, 'city', None)
                }
        except Exception:
            pass
        return {
            'id': obj.object_id,
            'title': obj.vacancy_title,
            'source': obj.vacancy_source
        }

    def get_competences(self, obj):
        """Получить список компетенций с их весами"""
        vacancy_competences = obj.vacancy_competences.select_related(
            'competence'
        ).order_by('priority', '-weight')

        return VacancyCompetenceSerializer(vacancy_competences, many=True).data

    def get_competences_count(self, obj):
        """Получить количество компетенций в профиле"""
        return obj.competences.count()