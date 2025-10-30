from rest_framework import serializers
from modules.competence_core.api.skill_map.models import (
    Skill, SkillSynonym, Technology, TechnologyAlias, SkillTechnology,
    SkillCategory, TechnologyCategory
)


class SkillSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Skill"""
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    synonyms_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Skill
        ref_name = 'SkillMapSkill'
        fields = [
            'id', 'name', 'category', 'category_display', 'description',
            'frequency', 'relevance', 'created_at', 'updated_at', 'synonyms_count'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_synonyms_count(self, obj):
        """Получить количество синонимов для умения"""
        return obj.synonyms.count()


class SkillCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания умения"""
    
    class Meta:
        model = Skill
        ref_name = 'SkillMapSkillCreate'
        fields = ['name', 'category', 'description', 'frequency', 'relevance']
    
    def validate_name(self, value):
        """Валидация названия умения"""
        if not value or not value.strip():
            raise serializers.ValidationError("Название умения не может быть пустым")
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Название умения должно содержать минимум 2 символа")
        return value.strip()
    
    def validate_relevance(self, value):
        """Валидация релевантности"""
        if value < 0.0 or value > 1.0:
            raise serializers.ValidationError("Релевантность должна быть в диапазоне от 0.0 до 1.0")
        return value
    
    def validate_frequency(self, value):
        """Валидация частоты"""
        if value < 0:
            raise serializers.ValidationError("Частота не может быть отрицательной")
        return value


class SkillUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления умения"""
    
    class Meta:
        model = Skill
        ref_name = 'SkillMapSkillUpdate'
        fields = ['name', 'category', 'description', 'frequency', 'relevance']


class SkillSynonymSerializer(serializers.ModelSerializer):
    """Сериализатор для модели SkillSynonym"""
    skill_name = serializers.CharField(source='skill.name', read_only=True)
    
    class Meta:
        model = SkillSynonym
        ref_name = 'SkillMapSkillSynonym'
        fields = ['id', 'skill', 'skill_name', 'synonym', 'created_at']
        read_only_fields = ['created_at']


class SkillSynonymCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания синонима умения"""
    
    class Meta:
        model = SkillSynonym
        ref_name = 'SkillMapSkillSynonymCreate'
        fields = ['skill', 'synonym']
    
    def validate_synonym(self, value):
        """Валидация синонима"""
        if not value or not value.strip():
            raise serializers.ValidationError("Синоним не может быть пустым")
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Синоним должен содержать минимум 2 символа")
        return value.strip()
    
    def validate(self, attrs):
        """Комплексная валидация"""
        skill = attrs.get('skill')
        synonym = attrs.get('synonym', '').strip()
        
        # Проверка, что синоним не совпадает с названием умения
        if skill and synonym.lower() == skill.name.lower():
            raise serializers.ValidationError({
                'synonym': 'Синоним не должен совпадать с основным названием умения'
            })
        
        # Проверка на существование такого же синонима для другого умения
        existing = SkillSynonym.objects.filter(synonym__iexact=synonym).exclude(skill=skill)
        if existing.exists():
            raise serializers.ValidationError({
                'synonym': f'Синоним "{synonym}" уже используется для другого умения'
            })
        
        return attrs


class TechnologySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Technology"""
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    parent_tech_name = serializers.CharField(source='parent_tech.name', read_only=True)
    aliases_count = serializers.SerializerMethodField()
    child_technologies_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Technology
        ref_name = 'SkillMapTechnology'
        fields = [
            'id', 'name', 'category', 'category_display', 'description',
            'popularity', 'relevance', 'occurrence_count', 'parent_tech',
            'parent_tech_name', 'created_at', 'updated_at', 'aliases_count',
            'child_technologies_count'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_aliases_count(self, obj):
        """Получить количество альтернативных названий"""
        return obj.aliases.count()
    
    def get_child_technologies_count(self, obj):
        """Получить количество дочерних технологий"""
        return obj.child_technologies.count()


class TechnologyCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания технологии"""
    
    class Meta:
        model = Technology
        ref_name = 'SkillMapTechnologyCreate'
        fields = [
            'name', 'category', 'description', 'popularity', 'relevance',
            'occurrence_count', 'parent_tech'
        ]
    
    def validate_name(self, value):
        """Валидация названия технологии"""
        if not value or not value.strip():
            raise serializers.ValidationError("Название технологии не может быть пустым")
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Название технологии должно содержать минимум 2 символа")
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
    
    def validate_occurrence_count(self, value):
        """Валидация количества упоминаний"""
        if value < 0:
            raise serializers.ValidationError("Количество упоминаний не может быть отрицательным")
        return value
    
    def validate(self, attrs):
        """Комплексная валидация"""
        parent_tech = attrs.get('parent_tech')
        
        # Проверка на циклические зависимости
        if parent_tech:
            current = parent_tech
            visited = set()
            while current:
                if current.id in visited:
                    raise serializers.ValidationError({
                        'parent_tech': 'Обнаружена циклическая зависимость в иерархии технологий'
                    })
                visited.add(current.id)
                current = current.parent_tech
        
        return attrs


class TechnologyUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления технологии"""
    
    class Meta:
        model = Technology
        ref_name = 'SkillMapTechnologyUpdate'
        fields = [
            'name', 'category', 'description', 'popularity', 'relevance',
            'occurrence_count', 'parent_tech'
        ]


class TechnologyAliasSerializer(serializers.ModelSerializer):
    """Сериализатор для модели TechnologyAlias"""
    technology_name = serializers.CharField(source='technology.name', read_only=True)
    
    class Meta:
        model = TechnologyAlias
        ref_name = 'SkillMapTechnologyAlias'
        fields = ['id', 'technology', 'technology_name', 'alias', 'created_at']
        read_only_fields = ['created_at']


class TechnologyAliasCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания альтернативного названия технологии"""
    
    class Meta:
        model = TechnologyAlias
        ref_name = 'SkillMapTechnologyAliasCreate'
        fields = ['technology', 'alias']
    
    def validate_alias(self, value):
        """Валидация альтернативного названия"""
        if not value or not value.strip():
            raise serializers.ValidationError("Альтернативное название не может быть пустым")
        if len(value.strip()) < 1:
            raise serializers.ValidationError("Альтернативное название должно содержать минимум 1 символ")
        return value.strip()
    
    def validate(self, attrs):
        """Комплексная валидация"""
        technology = attrs.get('technology')
        alias = attrs.get('alias', '').strip()
        
        # Проверка, что альтернативное название не совпадает с основным
        if technology and alias.lower() == technology.name.lower():
            raise serializers.ValidationError({
                'alias': 'Альтернативное название не должно совпадать с основным названием технологии'
            })
        
        # Проверка на существование такого же алиаса для другой технологии
        existing = TechnologyAlias.objects.filter(alias__iexact=alias).exclude(technology=technology)
        if existing.exists():
            raise serializers.ValidationError({
                'alias': f'Альтернативное название "{alias}" уже используется для другой технологии'
            })
        
        return attrs


class SkillTechnologySerializer(serializers.ModelSerializer):
    """Сериализатор для модели SkillTechnology"""
    skill_name = serializers.CharField(source='skill.name', read_only=True)
    technology_name = serializers.CharField(source='technology.name', read_only=True)
    
    class Meta:
        model = SkillTechnology
        ref_name = 'SkillMapSkillTechnology'
        fields = [
            'id', 'skill', 'skill_name', 'technology', 'technology_name',
            'relevance', 'usage_frequency', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class SkillTechnologyCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания связи умение-технология"""
    
    class Meta:
        model = SkillTechnology
        ref_name = 'SkillMapSkillTechnologyCreate'
        fields = ['skill', 'technology', 'relevance', 'usage_frequency']
    
    def validate_relevance(self, value):
        """Валидация релевантности связи"""
        if value < 0.0 or value > 1.0:
            raise serializers.ValidationError("Релевантность должна быть в диапазоне от 0.0 до 1.0")
        return value
    
    def validate_usage_frequency(self, value):
        """Валидация частоты использования"""
        if value < 0:
            raise serializers.ValidationError("Частота использования не может быть отрицательной")
        return value


class SkillTechnologyUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления связи умение-технология"""
    
    class Meta:
        model = SkillTechnology
        ref_name = 'SkillMapSkillTechnologyUpdate'
        fields = ['relevance', 'usage_frequency']
    
    def validate_relevance(self, value):
        """Валидация релевантности связи"""
        if value < 0.0 or value > 1.0:
            raise serializers.ValidationError("Релевантность должна быть в диапазоне от 0.0 до 1.0")
        return value
    
    def validate_usage_frequency(self, value):
        """Валидация частоты использования"""
        if value < 0:
            raise serializers.ValidationError("Частота использования не может быть отрицательной")
        return value


# Сериализаторы для выбора категорий
class SkillCategoryChoiceSerializer(serializers.Serializer):
    """Сериализатор для выбора категории умения"""
    
    class Meta:
        ref_name = 'SkillMapSkillCategoryChoice'
    
    value = serializers.CharField()
    label = serializers.CharField()


class TechnologyCategoryChoiceSerializer(serializers.Serializer):
    """Сериализатор для выбора категории технологии"""
    
    class Meta:
        ref_name = 'SkillMapTechnologyCategoryChoice'
    
    value = serializers.CharField()
    label = serializers.CharField()