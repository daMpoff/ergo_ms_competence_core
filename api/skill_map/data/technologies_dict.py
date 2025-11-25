"""
Базовый словарь технологий для первичной инициализации.

Структура данных для каждой технологии:
{
    'name': 'Название технологии',
    'category': 'Категория из TechnologyCategory',
    'description': 'Описание',
    'aliases': ['Альтернативные', 'названия'],
    'parent': 'Название родительской технологии' (опционально)
}

Категории (TechnologyCategory):
- LANG - Языки программирования
- FRAMEWORK - Фреймворки
- LIBRARY - Библиотеки  
- TOOL - Инструменты
- DB - Базы данных
- PLATFORM - Платформы
- PROTOCOL - Протоколы
- SERVICE - Сервисы
"""

from .languages import PROGRAMMING_LANGUAGES
from .frameworks_backend import BACKEND_FRAMEWORKS
from .frameworks_frontend import FRONTEND_FRAMEWORKS
from .databases import DATABASES
from .devops import DEVOPS_TOOLS
from .data_science import DATA_SCIENCE_LIBRARIES
from .mobile import MOBILE_DEVELOPMENT
from .testing import TESTING_TOOLS
from .cloud_platforms import CLOUD_PLATFORMS
from .protocols import PROTOCOLS


# ============================================================
# ОБЪЕДИНЕННЫЙ СЛОВАРЬ ВСЕХ ТЕХНОЛОГИЙ
# ============================================================
ALL_TECHNOLOGIES = (
    PROGRAMMING_LANGUAGES +
    BACKEND_FRAMEWORKS +
    FRONTEND_FRAMEWORKS +
    DATABASES +
    DEVOPS_TOOLS +
    DATA_SCIENCE_LIBRARIES +
    MOBILE_DEVELOPMENT +
    TESTING_TOOLS +
    CLOUD_PLATFORMS +
    PROTOCOLS
)


# ============================================================
# СТАТИСТИКА ПО КАТЕГОРИЯМ
# ============================================================
def get_statistics():
    """Возвращает статистику по технологиям."""
    stats = {
        'total': len(ALL_TECHNOLOGIES),
        'by_category': {},
        'by_source': {
            'languages': len(PROGRAMMING_LANGUAGES),
            'backend_frameworks': len(BACKEND_FRAMEWORKS),
            'frontend_frameworks': len(FRONTEND_FRAMEWORKS),
            'databases': len(DATABASES),
            'devops': len(DEVOPS_TOOLS),
            'data_science': len(DATA_SCIENCE_LIBRARIES),
            'mobile': len(MOBILE_DEVELOPMENT),
            'testing': len(TESTING_TOOLS),
            'cloud_platforms': len(CLOUD_PLATFORMS),
            'protocols': len(PROTOCOLS),
        }
    }
    
    for tech in ALL_TECHNOLOGIES:
        category = tech.get('category', 'UNKNOWN')
        stats['by_category'][category] = stats['by_category'].get(category, 0) + 1
    
    return stats


# Для обратной совместимости экспортируем отдельные списки
__all__ = [
    'ALL_TECHNOLOGIES',
    'PROGRAMMING_LANGUAGES',
    'BACKEND_FRAMEWORKS',
    'FRONTEND_FRAMEWORKS', 
    'DATABASES',
    'DEVOPS_TOOLS',
    'DATA_SCIENCE_LIBRARIES',
    'MOBILE_DEVELOPMENT',
    'TESTING_TOOLS',
    'CLOUD_PLATFORMS',
    'PROTOCOLS',
    'get_statistics',
]
