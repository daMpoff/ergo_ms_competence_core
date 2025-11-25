"""
Модуль данных для первичной инициализации skill_map.

Содержит справочники технологий, разбитые по категориям:
- languages.py - Языки программирования
- frameworks_backend.py - Backend фреймворки
- frameworks_frontend.py - Frontend фреймворки
- databases.py - Базы данных
- devops.py - DevOps инструменты
- data_science.py - Data Science и ML
- mobile.py - Мобильная разработка
- testing.py - Тестирование
- cloud_platforms.py - Облачные платформы
- protocols.py - Протоколы и очереди сообщений
"""

from .technologies_dict import (
    ALL_TECHNOLOGIES,
    PROGRAMMING_LANGUAGES,
    BACKEND_FRAMEWORKS,
    FRONTEND_FRAMEWORKS,
    DATABASES,
    DEVOPS_TOOLS,
    DATA_SCIENCE_LIBRARIES,
    MOBILE_DEVELOPMENT,
    TESTING_TOOLS,
    CLOUD_PLATFORMS,
    PROTOCOLS,
    get_statistics,
)

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
