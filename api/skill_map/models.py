"""
Модуль управления умениями и технологиями.

Содержит модели для представления умений, технологий и связей между ними,
используемых в системе анализа компетенций.
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class SkillCategory(models.TextChoices):
    """
    Категории умений.
    
    Определяет основные типы умений в системе компетенций.
    """
    TECHNICAL = 'TECH', 'Техническое'
    METHODOLOGICAL = 'METHOD', 'Методическое'
    SOFT = 'SOFT', 'Софт-умение'
    DOMAIN = 'DOMAIN', 'Предметное'


class Skill(models.Model):
    """
    Модель умения.
    
    Представляет отдельное умение, которое может быть использовано
    в различных компетенциях. Умения могут иметь синонимы
    и принадлежать к определенной категории.
    
    Attributes:
        name (str): Уникальное название умения
        category (str): Категория умения из SkillCategory
        description (str): Подробное описание умения
        frequency (int): Частота упоминания в вакансиях
        relevance (float): Коэффициент актуальности (0.0-1.0)
        created_at (datetime): Дата создания записи
        updated_at (datetime): Дата последнего обновления
    """
    
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название',
        help_text='Уникальное название умения'
    )
    category = models.CharField(
        max_length=10,
        choices=SkillCategory.choices,
        verbose_name='Категория',
        db_index=True,
        help_text='Категория, к которой относится умение'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание',
        help_text='Подробное описание умения и его применения'
    )
    frequency = models.IntegerField(
        default=0,
        verbose_name='Частота упоминаний',
        db_index=True,
        validators=[MinValueValidator(0)],
        help_text='Количество упоминаний умения в вакансиях'
    )
    relevance = models.FloatField(
        default=1.0,
        verbose_name='Релевантность',
        db_index=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text='Коэффициент актуальности умения (0.0-1.0)'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        db_table = 'cc_sm_skill'
        verbose_name = 'Умение'
        verbose_name_plural = 'Умения'
        ordering = ['-frequency', 'name']
        indexes = [
            models.Index(fields=['-frequency', 'category'], name='cc_skill_freq_cat_idx'),
            models.Index(fields=['category', '-relevance'], name='cc_skill_cat_rel_idx'),
        ]

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<Skill: {self.name} ({self.get_category_display()})>'


class SkillSynonym(models.Model):
    """
    Модель синонимов умения.
    
    Хранит альтернативные названия умений для улучшения
    поиска и сопоставления при парсинге вакансий и анализе текстов.
    
    Attributes:
        skill (Skill): Умение, к которому относится синоним
        synonym (str): Альтернативное название умения
        created_at (datetime): Дата создания записи
    """
    
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        related_name='synonyms',
        verbose_name='Умение',
        help_text='Умение, для которого указан синоним'
    )
    synonym = models.CharField(
        max_length=200,
        verbose_name='Синоним',
        db_index=True,
        help_text='Альтернативное название умения'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        db_table = 'cc_sm_skill_synonym'
        verbose_name = 'Синоним умения'
        verbose_name_plural = 'Синонимы умений'
        unique_together = [['skill', 'synonym']]
        ordering = ['synonym']
        indexes = [
            models.Index(fields=['synonym'], name='cc_skill_syn_idx'),
            models.Index(fields=['skill', 'synonym'], name='cc_skill_syn_skill_idx'),
        ]

    def __str__(self):
        return f"{self.skill.name} → {self.synonym}"

    def __repr__(self):
        return f'<SkillSynonym: {self.synonym} for {self.skill.name}>'


class TechnologyCategory(models.TextChoices):
    """
    Категории технологий.
    
    Определяет основные типы технологий в системе.
    """
    LANGUAGE = 'LANG', 'Язык программирования'
    FRAMEWORK = 'FRAMEWORK', 'Фреймворк'
    LIBRARY = 'LIBRARY', 'Библиотека'
    TOOL = 'TOOL', 'Инструмент'
    DATABASE = 'DB', 'База данных'
    PLATFORM = 'PLATFORM', 'Платформа'
    PROTOCOL = 'PROTOCOL', 'Протокол'
    SERVICE = 'SERVICE', 'Сервис'


class Technology(models.Model):
    """
    Модель технологии.
    
    Представляет конкретную технологию, инструмент или платформу.
    Технологии могут иметь иерархическую структуру через parent_tech.
    
    Attributes:
        name (str): Уникальное название технологии
        category (str): Категория технологии из TechnologyCategory
        description (str): Подробное описание технологии
        popularity (int): Показатель популярности технологии
        relevance (float): Коэффициент актуальности (0.0-1.0)
        occurrence_count (int): Количество упоминаний в вакансиях
        parent_tech (Technology): Родительская технология в иерархии
        created_at (datetime): Дата создания записи
        updated_at (datetime): Дата последнего обновления
    
    Example:
        >>> react = Technology.objects.create(name='React', category='FRAMEWORK')
        >>> nextjs = Technology.objects.create(name='Next.js', category='FRAMEWORK', parent_tech=react)
    """
    
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название',
        help_text='Уникальное название технологии'
    )
    category = models.CharField(
        max_length=15,
        choices=TechnologyCategory.choices,
        verbose_name='Категория',
        db_index=True,
        help_text='Категория технологии'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание',
        help_text='Подробное описание технологии'
    )
    popularity = models.IntegerField(
        default=0,
        verbose_name='Популярность',
        db_index=True,
        validators=[MinValueValidator(0)],
        help_text='Показатель популярности технологии'
    )
    relevance = models.FloatField(
        default=1.0,
        verbose_name='Релевантность',
        db_index=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text='Коэффициент актуальности технологии (0.0-1.0)'
    )
    occurrence_count = models.IntegerField(
        default=0,
        verbose_name='Количество упоминаний',
        validators=[MinValueValidator(0)],
        help_text='Количество упоминаний в вакансиях'
    )
    parent_tech = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='child_technologies',
        verbose_name='Родительская технология',
        help_text='Родительская технология в иерархии (например, React для Next.js)'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        db_table = 'cc_sm_technology'
        verbose_name = 'Технология'
        verbose_name_plural = 'Технологии'
        ordering = ['-popularity', 'name']
        indexes = [
            models.Index(fields=['-popularity', 'category'], name='cc_tech_pop_cat_idx'),
            models.Index(fields=['category', '-relevance'], name='cc_tech_cat_rel_idx'),
        ]

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<Technology: {self.name} ({self.get_category_display()})>'


class TechnologyAlias(models.Model):
    """
    Модель альтернативных названий технологии.
    
    Хранит альтернативные и сокращенные названия технологий
    для улучшения поиска и сопоставления при парсинге и анализе.
    
    Attributes:
        technology (Technology): Технология, к которой относится альтернативное название
        alias (str): Альтернативное или сокращенное название
        created_at (datetime): Дата создания записи
    
    Example:
        >>> js = Technology.objects.get(name='JavaScript')
        >>> TechnologyAlias.objects.create(technology=js, alias='JS')
    """
    
    technology = models.ForeignKey(
        Technology,
        on_delete=models.CASCADE,
        related_name='aliases',
        verbose_name='Технология',
        help_text='Технология, для которой указан альтернативное название'
    )
    alias = models.CharField(
        max_length=200,
        verbose_name='Альтернативное название',
        db_index=True,
        help_text='Альтернативное или сокращенное название технологии'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        db_table = 'cc_sm_technology_alias'
        verbose_name = 'Альтернативное название технологии'
        verbose_name_plural = 'Альтернативные названия технологий'
        unique_together = [['technology', 'alias']]
        ordering = ['alias']
        indexes = [
            models.Index(fields=['alias'], name='cc_tech_alias_idx'),
            models.Index(fields=['technology', 'alias'], name='cc_tech_alias_tech_idx'),
        ]

    def __str__(self):
        return f"{self.technology.name} → {self.alias}"

    def __repr__(self):
        return f'<TechnologyAlias: {self.alias} for {self.technology.name}>'


class SkillTechnology(models.Model):
    """
    Модель связи между умением и технологией.
    
    Представляет комбинацию умения и технологии, например:
    "Разработка веб-приложений" (умение) + "Django" (технология).
    Используется для формирования более точных компетенций.
    
    Attributes:
        skill (Skill): Умение
        technology (Technology): Технология
        relevance (float): Релевантность связи (0.0-1.0)
        usage_frequency (int): Частота совместного использования
        created_at (datetime): Дата создания записи
        updated_at (datetime): Дата последнего обновления
    
    Example:
        >>> web_dev = Skill.objects.get(name='Веб-разработка')
        >>> django = Technology.objects.get(name='Django')
        >>> SkillTechnology.objects.create(skill=web_dev, technology=django, relevance=0.95)
    """
    
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        related_name='skill_technologies',
        verbose_name='Умение',
        help_text='Умение, связанное с технологией'
    )
    technology = models.ForeignKey(
        Technology,
        on_delete=models.CASCADE,
        related_name='technology_skills',
        verbose_name='Технология',
        help_text='Технология, связанная с умением'
    )
    relevance = models.FloatField(
        default=1.0,
        verbose_name='Релевантность связи',
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text='Насколько релевантна данная технология для данного умения (0.0-1.0)'
    )
    usage_frequency = models.IntegerField(
        default=0,
        verbose_name='Частота совместного использования',
        validators=[MinValueValidator(0)],
        help_text='Количество раз, когда умение и технология встречались вместе'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        db_table = 'cc_sm_skill_technology'
        verbose_name = 'Связь умение-технология'
        verbose_name_plural = 'Связи умение-технология'
        unique_together = [['skill', 'technology']]
        ordering = ['-relevance', '-usage_frequency']
        indexes = [
            models.Index(fields=['skill', '-relevance'], name='cc_skill_tech_skill_idx'),
            models.Index(fields=['technology', '-relevance'], name='cc_skill_tech_tech_idx'),
        ]

    def __str__(self):
        return f"{self.skill.name} - {self.technology.name}"

    def __repr__(self):
        return f'<SkillTechnology: {self.skill.name} + {self.technology.name}>'

