"""
Примеры использования системы технологий для парсинга вакансий.

Этот файл демонстрирует различные способы работы с технологиями
при парсинге и анализе вакансий.
"""

import os
import django

# Настройка Django (для запуска как standalone скрипта)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.config.patterns.development')
django.setup()

from modules.competence_core.api.skill_map.utils import TechnologyFinder
from modules.competence_core.api.skill_map.models import Technology


def example_1_basic_search():
    """Пример 1: Базовый поиск технологий в тексте"""
    print('\n' + '='*70)
    print('ПРИМЕР 1: Базовый поиск технологий')
    print('='*70)
    
    # Создаем поисковик
    finder = TechnologyFinder()
    finder.load_technologies()
    
    # Пример текста вакансии
    vacancy_text = """
    Требуется Python разработчик с опытом работы в Django и Flask.
    Необходимо знание PostgreSQL, Redis и Docker.
    Будет плюсом опыт работы с React и Vue.js.
    """
    
    # Поиск технологий
    found_technologies = finder.find_technologies_in_text(vacancy_text)
    
    print(f'\nТекст вакансии:\n{vacancy_text}')
    print(f'\nНайдено технологий: {len(found_technologies)}')
    
    for item in found_technologies:
        tech = item['technology']
        print(f'  - {tech.name} ({tech.get_category_display()}) - найдено как: "{item["matched_text"]}"')


def example_2_extract_names():
    """Пример 2: Извлечение только названий технологий"""
    print('\n' + '='*70)
    print('ПРИМЕР 2: Извлечение названий')
    print('='*70)
    
    finder = TechnologyFinder()
    finder.load_technologies()
    
    text = "Ищем DevOps инженера: AWS, Kubernetes, Docker, Jenkins, Python"
    
    names = finder.extract_technology_names(text)
    
    print(f'\nТекст: {text}')
    print(f'\nТехнологии: {", ".join(names)}')


def example_3_by_category():
    """Пример 3: Поиск по категориям"""
    print('\n' + '='*70)
    print('ПРИМЕР 3: Поиск по категориям')
    print('='*70)
    
    finder = TechnologyFinder()
    finder.load_technologies()
    
    text = """
    Senior Full Stack Developer
    Backend: Python, Django, FastAPI, PostgreSQL, Redis
    Frontend: React, TypeScript, Next.js
    DevOps: Docker, Kubernetes, AWS
    """
    
    print(f'\nТекст вакансии:\n{text}')
    
    # Поиск по категориям
    categories = {
        'LANG': 'Языки программирования',
        'FRAMEWORK': 'Фреймворки',
        'DB': 'Базы данных',
        'TOOL': 'Инструменты',
        'PLATFORM': 'Платформы'
    }
    
    for cat_code, cat_name in categories.items():
        found = finder.find_technologies_by_category(text, cat_code)
        if found:
            print(f'\n{cat_name}:')
            for item in found:
                print(f'  - {item["technology"].name}')


def example_4_statistics():
    """Пример 4: Статистика по технологиям"""
    print('\n' + '='*70)
    print('ПРИМЕР 4: Статистика')
    print('='*70)
    
    finder = TechnologyFinder()
    finder.load_technologies()
    
    text = """
    Компания ищет разработчика на полный стек:
    
    Backend разработка:
    - Python (Django, FastAPI)
    - Node.js (Express.js)
    - REST API, GraphQL
    
    Frontend разработка:
    - React, TypeScript
    - Next.js, Webpack
    
    Базы данных:
    - PostgreSQL, MongoDB, Redis
    
    DevOps:
    - Docker, Kubernetes
    - AWS, GitLab CI
    """
    
    stats = finder.get_statistics(text)
    
    print(f'\nПроанализирован текст вакансии')
    print(f'\nСтатистика:')
    print(f'  Всего найдено технологий: {stats["total_found"]}')
    print(f'\n  По категориям:')
    
    for category, count in stats['by_category'].items():
        print(f'    - {category}: {count}')


def example_5_integration_with_vacancy():
    """Пример 5: Интеграция с парсером вакансий"""
    print('\n' + '='*70)
    print('ПРИМЕР 5: Интеграция с парсером вакансий')
    print('='*70)
    
    finder = TechnologyFinder()
    finder.load_technologies()
    
    # Имитация данных вакансии из HeadHunter
    vacancy_data = {
        'name': 'Middle Python Developer',
        'description': """
        Мы ищем Python разработчика в команду разработки backend сервисов.
        
        Требования:
        - Опыт разработки на Python 3+ (от 2 лет)
        - Знание Django или FastAPI
        - Опыт работы с PostgreSQL
        - Понимание принципов REST API
        - Опыт работы с Git
        
        Будет плюсом:
        - Опыт работы с Docker и Kubernetes
        - Знание React для понимания frontend
        - Опыт работы с Redis, Celery
        - Знание AWS
        """,
        'key_skills': ['Python', 'Django', 'PostgreSQL', 'Docker', 'REST API']
    }
    
    # Объединяем текст для анализа
    full_text = f"{vacancy_data['name']} {vacancy_data['description']} {' '.join(vacancy_data['key_skills'])}"
    
    # Находим технологии
    technologies = finder.extract_technology_objects(full_text)
    
    print(f'\nВакансия: {vacancy_data["name"]}')
    print(f'\nНайденные технологии ({len(technologies)}):')
    
    for tech in technologies:
        print(f'  - {tech.name} ({tech.get_category_display()})')
    
    # Обновляем счетчики популярности
    tech_ids = [tech.id for tech in technologies]
    finder.update_technology_popularity(tech_ids)
    
    print(f'\nСчетчики популярности обновлены для {len(tech_ids)} технологий')


def example_6_real_world_workflow():
    """Пример 6: Реальный workflow обработки вакансий"""
    print('\n' + '='*70)
    print('ПРИМЕР 6: Реальный workflow')
    print('='*70)
    
    # Инициализация
    finder = TechnologyFinder()
    tech_count = finder.load_technologies()
    print(f'\nЗагружено {tech_count} технологий')
    
    # Список вакансий для обработки
    vacancies = [
        "Python Developer: Django, DRF, PostgreSQL, Docker",
        "Frontend Developer: React, TypeScript, Next.js, Webpack",
        "Full Stack: Python, FastAPI, React, MongoDB, AWS",
        "DevOps Engineer: Kubernetes, Docker, Jenkins, AWS, Terraform",
        "Data Scientist: Python, Pandas, NumPy, TensorFlow, PyTorch"
    ]
    
    print(f'\nОбработка {len(vacancies)} вакансий...\n')
    
    all_technologies = {}  # {tech_name: count}
    
    for i, vacancy_text in enumerate(vacancies, 1):
        print(f'{i}. {vacancy_text}')
        
        # Находим технологии
        found = finder.find_technologies_in_text(vacancy_text)
        
        # Собираем статистику
        for item in found:
            tech_name = item['technology'].name
            all_technologies[tech_name] = all_technologies.get(tech_name, 0) + 1
        
        print(f'   -> Найдено технологий: {len(found)}')
    
    # Статистика
    print(f'\nОбщая статистика:')
    print(f'  Уникальных технологий: {len(all_technologies)}')
    print(f'\n  Топ-5 самых упоминаемых:')
    
    sorted_techs = sorted(all_technologies.items(), key=lambda x: x[1], reverse=True)
    for tech_name, count in sorted_techs[:5]:
        print(f'    {count}x {tech_name}')


# ============================================================
# ЗАПУСК ПРИМЕРОВ
# ============================================================
if __name__ == '__main__':
    print('\n' + '='*70)
    print('ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ СИСТЕМЫ ТЕХНОЛОГИЙ')
    print('='*70)
    
    try:
        example_1_basic_search()
        example_2_extract_names()
        example_3_by_category()
        example_4_statistics()
        example_5_integration_with_vacancy()
        example_6_real_world_workflow()
        
        print('\n' + '='*70)
        print('Все примеры успешно выполнены!')
        print('='*70 + '\n')
        
    except Exception as e:
        print(f'\nОшибка: {e}')
        import traceback
        traceback.print_exc()

