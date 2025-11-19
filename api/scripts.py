"""
Скрипты для работы с компетенциями.

Содержит вспомогательные функции для создания демонстрационных данных,
анализа компетенций и работы с профилями вакансий.
"""

import os
import django

# Настройка Django (для запуска как standalone скрипта)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.config.patterns.development')
django.setup()

from modules.competence_core.api.models import (
    Competence, CompetenceComponent, CompetenceLevel,
    VacancyCompetenceProfile, VacancyCompetence
)
from django.contrib.contenttypes.models import ContentType
from django.db import models


def create_demo_competences():
    """
    Создание демонстрационных компетенций для тестирования.

    Создает базовые компетенции для разных уровней и направлений.
    Примечание: Компоненты компетенций создаются отдельно через API или админку
    после загрузки данных в skill_map модуль.
    """
    print("Создание демонстрационных компетенций...")

    # Создаем компетенции разных уровней
    competences_data = [
        {
            'name': 'Backend разработка на Python',
            'description': 'Компетенция backend-разработчика с использованием Python',
            'level': 'MIDDLE',
            'is_core': True,
            'popularity': 85,
            'relevance': 0.95
        },
        {
            'name': 'Frontend разработка на React',
            'description': 'Компетенция frontend-разработчика с использованием React',
            'level': 'MIDDLE',
            'is_core': True,
            'popularity': 78,
            'relevance': 0.92
        },
        {
            'name': 'Fullstack разработка',
            'description': 'Компетенция fullstack-разработчика',
            'level': 'SENIOR',
            'is_core': True,
            'popularity': 92,
            'relevance': 0.98
        },
        {
            'name': 'Data Science с Python',
            'description': 'Компетенция специалиста по анализу данных',
            'level': 'MIDDLE',
            'is_core': True,
            'popularity': 67,
            'relevance': 0.88
        },
        {
            'name': 'DevOps инженер',
            'description': 'Компетенция DevOps инженера',
            'level': 'SENIOR',
            'is_core': True,
            'popularity': 71,
            'relevance': 0.91
        }
    ]

    created_count = 0
    for comp_data in competences_data:
        competence, created = Competence.objects.get_or_create(
            name=comp_data['name'],
            defaults=comp_data
        )
        if created:
            created_count += 1
            print(f"  Создана: {competence.name}")

    print(f"Создано компетенций: {created_count}")
    print(f"Всего компетенций в базе: {Competence.objects.count()}")
    print("Демонстрационные данные созданы успешно!")
    print("\nДля создания компонентов компетенций используйте API или админку,")
    print("предварительно загрузив данные умений и технологий через skill_map модуль.")


def create_demo_vacancy_profile():
    """
    Создание демонстрационного профиля вакансии.

    Создает профиль для тестовой вакансии и связывает с компетенциями.
    """
    print("Создание демонстрационного профиля вакансии...")

    # Получаем компетенции
    backend_comp = Competence.objects.filter(name__icontains='Backend').first()
    frontend_comp = Competence.objects.filter(name__icontains='Frontend').first()
    fullstack_comp = Competence.objects.filter(name__icontains='Fullstack').first()

    available_competences = [c for c in [backend_comp, frontend_comp, fullstack_comp] if c]
    if not available_competences:
        print("Предупреждение: компетенции не найдены. Сначала создайте демонстрационные компетенции")
        return

    # Создаем профиль вакансии (без реальной вакансии, только для демонстрации)
    profile = VacancyCompetenceProfile.objects.create(
        vacancy_title='Senior Fullstack Python Developer',
        vacancy_source='Demo',
        content_type=None,  # Для демонстрации
        object_id=999  # Фиктивный ID
    )

    # Добавляем компетенции к профилю
    priority = 1
    for competence in available_competences:
        VacancyCompetence.objects.create(
            vacancy_profile=profile,
            competence=competence,
            priority=priority,
            required_level='SENIOR' if priority == 1 else 'MIDDLE',
            is_mandatory=priority <= 2,
            weight=max(0.3, 1.0 - (priority - 1) * 0.2)
        )
        priority += 1

    print(f"Создан профиль вакансии: {profile}")
    print(f"Добавлено компетенций: {profile.competences.count()}")
    print("Демонстрационный профиль создан успешно!")


def cleanup_demo_data():
    """
    Очистка демонстрационных данных.
    """
    print("Очистка демонстрационных данных...")

    # Удаляем в правильном порядке из-за зависимостей
    VacancyCompetence.objects.filter(
        vacancy_profile__vacancy_source='Demo'
    ).delete()

    VacancyCompetenceProfile.objects.filter(vacancy_source='Demo').delete()
    CompetenceComponent.objects.filter(competence__name__icontains='демонстрац').delete()
    Competence.objects.filter(name__icontains='демонстрац').delete()

    print("Демонстрационные данные очищены!")


def show_statistics():
    """
    Вывод статистики по компетенциям.
    """
    print("=" * 60)
    print("СТАТИСТИКА КОМПЕТЕНЦИЙ")
    print("=" * 60)

    total_competences = Competence.objects.count()
    total_components = CompetenceComponent.objects.count()
    total_profiles = VacancyCompetenceProfile.objects.count()
    total_links = VacancyCompetence.objects.count()

    print(f"Всего компетенций: {total_competences}")
    print(f"Всего компонентов: {total_components}")
    print(f"Всего профилей вакансий: {total_profiles}")
    print(f"Всего связей вакансия-компетенция: {total_links}")

    # Статистика по уровням
    level_stats = Competence.objects.values('level').annotate(
        count=models.Count('id')
    ).order_by('-count')

    print(f"\nКомпетенции по уровням:")
    for stat in level_stats:
        level_name = dict(CompetenceLevel.choices).get(stat['level'], stat['level'])
        print(f"  {level_name}: {stat['count']}")

    # Топ компетенций по популярности
    top_competences = Competence.objects.order_by('-popularity')[:5]
    if top_competences:
        print(f"\nТоп-5 компетенций по популярности:")
        for comp in top_competences:
            print(f"  {comp.name}: {comp.popularity} ({comp.get_level_display()})")

    print("=" * 60)


# Демонстрационные функции для вызова из командной строки
if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Использование: python scripts.py <command>")
        print("Доступные команды:")
        print("  create_demo    - создать демонстрационные данные")
        print("  create_profile - создать демо профиль вакансии")
        print("  cleanup        - очистить демо данные")
        print("  stats          - показать статистику")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'create_demo':
        create_demo_competences()
    elif command == 'create_profile':
        create_demo_vacancy_profile()
    elif command == 'cleanup':
        cleanup_demo_data()
    elif command == 'stats':
        show_statistics()
    else:
        print(f"Неизвестная команда: {command}")