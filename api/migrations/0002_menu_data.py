# -*- coding: utf-8 -*-
"""
Миграция данных: заполнение меню модуля Competence Core.

Порядок элементов определяется последовательностью создания.
"""

from django.db import migrations


def populate_menu(apps, schema_editor):
    """Создаёт элементы меню для модуля Competence Core."""
    from src.core.cms.adp.menu.migration_utils import MenuMigrationHelper

    helper = MenuMigrationHelper(apps, 'modules/competence_core')
    helper.clear_module_items()

    # Корневой элемент (order вычисляется автоматически)
    root = helper.create_group(
        'База знаний',
        'CompetenceCoreHome',
        icon='BriefcaseBusiness',
    )

    # Дочерние элементы — порядок определяется последовательностью
    helper.create_route('Панель управления', 'CompetenceCoreDashboard', parent=root, icon='LayoutDashboard')
    helper.create_route('Технологии', 'CompetenceCoreTechnologies', parent=root, icon='CircuitBoard')
    helper.create_route('Компетенции', 'CompetenceCoreCompetences', parent=root, icon='BadgeCheck')
    helper.create_route('Профили вакансий', 'CompetenceCoreVacancyProfiles', parent=root, icon='BriefcaseBusiness')


def reverse_populate_menu(apps, schema_editor):
    """Удаляет элементы меню модуля."""
    MenuItem = apps.get_model('cms_adp', 'MenuItem')
    MenuItem.objects.filter(module_source='modules/competence_core').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('cms_adp', '0007_populate_core_menu'),
        ('competence_core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            populate_menu,
            reverse_populate_menu,
        ),
    ]
