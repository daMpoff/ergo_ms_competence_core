"""
Модуль управления компетенциями.

Содержит модели для представления компетенций, их компонентов
и связей с вакансиями в системе анализа профессиональных требований.
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from modules.competence_core.api.skill_map.models import Skill, SkillTechnology


class CompetenceLevel(models.TextChoices):
    """
    Уровни компетенций.
    
    Определяет градацию профессиональных уровней владения компетенциями.
    """
    JUNIOR = 'JUNIOR', 'Junior'
    MIDDLE = 'MIDDLE', 'Middle'
    SENIOR = 'SENIOR', 'Senior'
    EXPERT = 'EXPERT', 'Expert'


class Competence(models.Model):
    """
    Модель компетенции.
    
    Представляет профессиональную компетенцию, которая формируется
    из набора умений и технологий. Компетенции используются для
    описания требований к вакансиям и профилей специалистов.
    
    Attributes:
        name (str): Название компетенции
        description (str): Подробное описание компетенции
        level (str): Уровень компетенции из CompetenceLevel
        popularity (int): Показатель популярности компетенции
        relevance (float): Коэффициент актуальности (0.0-1.0)
        is_core (bool): Является ли компетенция ключевой
        created_at (datetime): Дата создания записи
        updated_at (datetime): Дата последнего обновления
    
    Example:
        >>> comp = Competence.objects.create(
        ...     name='Backend разработка на Python',
        ...     level='MIDDLE',
        ...     is_core=True
        ... )
    """
    
    name = models.CharField(
        max_length=300,
        verbose_name='Название',
        db_index=True,
        help_text='Название компетенции'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание',
        help_text='Подробное описание компетенции и её применения'
    )
    level = models.CharField(
        max_length=10,
        choices=CompetenceLevel.choices,
        blank=True,
        verbose_name='Уровень',
        db_index=True,
        help_text='Профессиональный уровень компетенции'
    )
    popularity = models.IntegerField(
        default=0,
        verbose_name='Популярность',
        db_index=True,
        validators=[MinValueValidator(0)],
        help_text='Показатель популярности компетенции в вакансиях'
    )
    relevance = models.FloatField(
        default=1.0,
        verbose_name='Релевантность',
        db_index=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text='Коэффициент актуальности компетенции (0.0-1.0)'
    )
    is_core = models.BooleanField(
        default=True,
        verbose_name='Ключевая компетенция',
        db_index=True,
        help_text='Является ли компетенция ключевой для профессии'
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
        db_table = 'cc_competence'
        verbose_name = 'Компетенция'
        verbose_name_plural = 'Компетенции'
        ordering = ['-popularity', 'name']
        indexes = [
            models.Index(fields=['-popularity', 'level'], name='cc_comp_pop_level_idx'),
            models.Index(fields=['is_core', '-relevance'], name='cc_comp_core_rel_idx'),
        ]

    def __str__(self):
        level_str = f" ({self.get_level_display()})" if self.level else ""
        return f"{self.name}{level_str}"

    def __repr__(self):
        return f'<Competence: {self.name} [{self.level or "N/A"}]>'


class CompetenceComponent(models.Model):
    """
    Модель компонента компетенции.
    
    Связь между компетенцией и её составляющими элементами.
    Компонент может быть представлен в двух вариантах:
    - Только умение (skill заполнен, skill_technology = NULL)
    - Умение с конкретной технологией (skill и skill_technology заполнены)
    
    Attributes:
        competence (Competence): Компетенция, к которой относится компонент
        skill (Skill): Умение, входящее в компетенцию
        skill_technology (SkillTechnology): Опциональная связка умение-технология
        importance (float): Важность компонента для компетенции (0.0-1.0)
        required_level (str): Требуемый уровень владения
        weight (float): Вес компонента при расчете уровня компетенции
        created_at (datetime): Дата создания записи
        updated_at (datetime): Дата последнего обновления
    
    Example:
        >>> # Компонент: только умение
        >>> CompetenceComponent.objects.create(
        ...     competence=backend_comp,
        ...     skill=python_skill,
        ...     importance=0.9
        ... )
        >>> # Компонент: умение + технология
        >>> skill_tech = SkillTechnology.objects.get(skill=web_dev, technology=django)
        >>> CompetenceComponent.objects.create(
        ...     competence=backend_comp,
        ...     skill=web_dev,
        ...     skill_technology=skill_tech,
        ...     importance=0.95
        ... )
    """
    
    competence = models.ForeignKey(
        Competence,
        on_delete=models.CASCADE,
        related_name='components',
        verbose_name='Компетенция',
        help_text='Компетенция, к которой относится компонент'
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        related_name='competence_components',
        verbose_name='Умение',
        help_text='Базовое умение компонента'
    )
    skill_technology = models.ForeignKey(
        SkillTechnology,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='competence_components',
        verbose_name='Связь умение-технология',
        help_text='Опциональная связка умение-технология для более точного определения компонента'
    )
    importance = models.FloatField(
        default=1.0,
        verbose_name='Важность компонента',
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text='Важность компонента для компетенции (0.0-1.0, где 1.0 - критически важный)'
    )
    required_level = models.CharField(
        max_length=10,
        choices=CompetenceLevel.choices,
        blank=True,
        verbose_name='Требуемый уровень владения',
        help_text='Минимальный уровень владения умением для данной компетенции'
    )
    weight = models.FloatField(
        default=1.0,
        verbose_name='Вес компонента',
        validators=[MinValueValidator(0.0)],
        help_text='Относительный вес при расчете общего уровня компетенции'
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
        db_table = 'cc_competence_component'
        verbose_name = 'Компонент компетенции'
        verbose_name_plural = 'Компоненты компетенций'
        unique_together = [['competence', 'skill', 'skill_technology']]
        ordering = ['-importance', '-weight']
        indexes = [
            models.Index(fields=['competence', '-importance'], name='cc_comp_comp_imp_idx'),
            models.Index(fields=['skill', 'skill_technology'], name='cc_comp_comp_skill_idx'),
            models.Index(fields=['competence', 'skill'], name='cc_comp_comp_cs_idx'),
        ]

    def __str__(self):
        if self.skill_technology:
            return f"{self.competence.name}: {self.skill.name} ({self.skill_technology.technology.name})"
        return f"{self.competence.name}: {self.skill.name}"

    def __repr__(self):
        tech_part = f" + {self.skill_technology.technology.name}" if self.skill_technology else ""
        return f'<CompetenceComponent: {self.competence.name} -> {self.skill.name}{tech_part}>'

    def clean(self):
        """Валидация данных перед сохранением."""
        if self.importance < 0 or self.importance > 1:
            raise ValidationError({
                'importance': 'Важность должна быть в диапазоне от 0 до 1'
            })
        
        if self.weight < 0:
            raise ValidationError({
                'weight': 'Вес не может быть отрицательным'
            })
        
        # Проверка соответствия skill_technology выбранному skill
        if self.skill_technology and self.skill_technology.skill_id != self.skill_id:
            raise ValidationError({
                'skill_technology': 'Связь умение-технология должна соответствовать выбранному умению'
            })


class VacancyCompetenceProfile(models.Model):
    """
    Модель профиля компетенций для вакансии.
    
    Формирует набор компетенций, требуемых для конкретной вакансии.
    Использует GenericForeignKey для возможности связи с различными
    моделями вакансий в системе (HeadHunter, Habr Career, SuperJob и др.).
    
    Attributes:
        content_type (ContentType): Тип модели вакансии
        object_id (int): ID объекта вакансии
        vacancy (Generic): Связь с вакансией через GenericForeignKey
        vacancy_title (str): Название вакансии (кэш)
        vacancy_source (str): Источник вакансии
        created_at (datetime): Дата создания профиля
        updated_at (datetime): Дата последнего обновления
    
    Example:
        >>> from modules.vacancies_parser.headhunter.models import Vacancy
        >>> vacancy = Vacancy.objects.first()
        >>> profile = VacancyCompetenceProfile.objects.create(
        ...     vacancy=vacancy,
        ...     vacancy_title=vacancy.title,
        ...     vacancy_source='HeadHunter'
        ... )
        >>> profile.competences.add(python_backend_comp)
    """
    
    # GenericForeignKey для связи с различными моделями вакансий
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name='Тип вакансии',
        help_text='Модель вакансии (HeadHunter, Habr Career и т.д.)'
    )
    object_id = models.PositiveIntegerField(
        verbose_name='ID вакансии',
        help_text='Идентификатор вакансии'
    )
    vacancy = GenericForeignKey('content_type', 'object_id')
    
    # Кэшированные данные для быстрого доступа
    vacancy_title = models.CharField(
        max_length=500,
        verbose_name='Название вакансии',
        db_index=True,
        help_text='Кэшированное название вакансии для быстрого доступа'
    )
    vacancy_source = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Источник вакансии',
        db_index=True,
        help_text='Источник вакансии (HeadHunter, Habr Career, SuperJob и т.д.)'
    )
    
    # Связь с компетенциями через промежуточную таблицу
    competences = models.ManyToManyField(
        Competence,
        through='VacancyCompetence',
        related_name='vacancy_profiles',
        verbose_name='Компетенции'
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
        db_table = 'cc_vacancy_profile'
        verbose_name = 'Профиль компетенций вакансии'
        verbose_name_plural = 'Профили компетенций вакансий'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['content_type', 'object_id'], name='cc_vac_prof_ct_oid_idx'),
            models.Index(fields=['vacancy_source', '-created_at'], name='cc_vac_prof_src_idx'),
            models.Index(fields=['-created_at'], name='cc_vac_prof_created_idx'),
        ]
        unique_together = [['content_type', 'object_id']]

    def __str__(self):
        source = f" [{self.vacancy_source}]" if self.vacancy_source else ""
        return f"Профиль: {self.vacancy_title}{source}"

    def __repr__(self):
        return f'<VacancyCompetenceProfile: {self.vacancy_title} ({self.competences.count()} компетенций)>'


class VacancyCompetence(models.Model):
    """
    Модель связи вакансии и компетенции (промежуточная таблица).
    
    Связывает профиль вакансии с конкретной компетенцией,
    указывая важность и приоритет компетенции для данной вакансии.
    
    Attributes:
        vacancy_profile (VacancyCompetenceProfile): Профиль вакансии
        competence (Competence): Компетенция
        priority (int): Приоритет компетенции для вакансии
        required_level (str): Требуемый уровень компетенции
        is_mandatory (bool): Является ли компетенция обязательной
        weight (float): Вес компетенции при подборе кандидатов
        created_at (datetime): Дата добавления связи
    
    Example:
        >>> VacancyCompetence.objects.create(
        ...     vacancy_profile=profile,
        ...     competence=python_comp,
        ...     priority=1,
        ...     required_level='MIDDLE',
        ...     is_mandatory=True,
        ...     weight=1.0
        ... )
    """
    
    vacancy_profile = models.ForeignKey(
        VacancyCompetenceProfile,
        on_delete=models.CASCADE,
        related_name='vacancy_competences',
        verbose_name='Профиль вакансии',
        help_text='Профиль компетенций вакансии'
    )
    competence = models.ForeignKey(
        Competence,
        on_delete=models.CASCADE,
        related_name='vacancy_competences',
        verbose_name='Компетенция',
        help_text='Требуемая компетенция'
    )
    priority = models.IntegerField(
        default=0,
        verbose_name='Приоритет',
        db_index=True,
        validators=[MinValueValidator(0)],
        help_text='Приоритет компетенции (чем меньше число, тем выше приоритет)'
    )
    required_level = models.CharField(
        max_length=10,
        choices=CompetenceLevel.choices,
        blank=True,
        verbose_name='Требуемый уровень',
        help_text='Минимальный требуемый уровень компетенции'
    )
    is_mandatory = models.BooleanField(
        default=True,
        verbose_name='Обязательная компетенция',
        db_index=True,
        help_text='Является ли компетенция обязательной для вакансии'
    )
    weight = models.FloatField(
        default=1.0,
        verbose_name='Вес компетенции',
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text='Вес компетенции при подборе и оценке кандидатов (0.0-1.0)'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        db_table = 'cc_vacancy_competence'
        verbose_name = 'Компетенция вакансии'
        verbose_name_plural = 'Компетенции вакансий'
        ordering = ['priority', '-weight']
        unique_together = [['vacancy_profile', 'competence']]
        indexes = [
            models.Index(fields=['vacancy_profile', 'priority'], name='cc_vac_comp_prof_pri_idx'),
            models.Index(fields=['competence', '-weight'], name='cc_vac_comp_comp_w_idx'),
            models.Index(fields=['is_mandatory', 'priority'], name='cc_vac_comp_mand_pri_idx'),
        ]

    def __str__(self):
        mandatory = " (обязательная)" if self.is_mandatory else ""
        level = f" [{self.get_required_level_display()}]" if self.required_level else ""
        return f"{self.vacancy_profile.vacancy_title}: {self.competence.name}{level}{mandatory}"

    def __repr__(self):
        return f'<VacancyCompetence: {self.competence.name} for {self.vacancy_profile.vacancy_title}>'

    def clean(self):
        """Валидация данных перед сохранением."""
        if self.weight < 0 or self.weight > 1:
            raise ValidationError({
                'weight': 'Вес должен быть в диапазоне от 0 до 1'
            })
        
        if self.priority < 0:
            raise ValidationError({
                'priority': 'Приоритет не может быть отрицательным'
            })
