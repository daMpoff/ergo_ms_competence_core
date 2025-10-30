"""
Утилита для поиска технологий в текстах.

Используется для парсинга вакансий и автоматического определения
упомянутых технологий.
"""

import re
import logging
from typing import List, Dict, Set, Tuple
from django.db.models import Q

from modules.competence_core.api.skill_map.models import Technology, TechnologyAlias

logger = logging.getLogger('modules.competence_core.skill_map')


class TechnologyFinder:
    """
    Класс для поиска и извлечения технологий из текста.
    
    Использует базу данных технологий и их алиасов для поиска
    упоминаний в описаниях вакансий, резюме и других текстах.
    
    Example:
        >>> finder = TechnologyFinder()
        >>> finder.load_technologies()
        >>> text = "Требуется разработчик на Python, Django и React"
        >>> found = finder.find_technologies_in_text(text)
        >>> print(found)
        [
            {'technology': <Technology: Python>, 'matched_text': 'Python', 'positions': [(30, 36)]},
            {'technology': <Technology: Django>, 'matched_text': 'Django', 'positions': [(38, 44)]},
            {'technology': <Technology: React>, 'matched_text': 'React', 'positions': [(47, 52)]}
        ]
    """
    
    def __init__(self):
        """Инициализация поисковика технологий."""
        self.technologies = {}  # {tech_id: Technology object}
        self.search_patterns = []  # [(pattern, tech_id), ...]
        self.loaded = False
    
    def load_technologies(self, force_reload=False):
        """
        Загрузка технологий из базы данных.
        
        Args:
            force_reload (bool): Принудительно перезагрузить данные
        
        Returns:
            int: Количество загруженных технологий
        """
        if self.loaded and not force_reload:
            logger.debug('Технологии уже загружены')
            return len(self.technologies)
        
        logger.info('Загрузка технологий из базы данных...')
        
        self.technologies = {}
        self.search_patterns = []
        
        # Загружаем все технологии с алиасами
        technologies = Technology.objects.prefetch_related('aliases').all()
        
        for tech in technologies:
            self.technologies[tech.id] = tech
            
            # Добавляем основное название
            pattern = self._create_pattern(tech.name)
            self.search_patterns.append((pattern, tech.id, tech.name))
            
            # Добавляем алиасы
            for alias_obj in tech.aliases.all():
                alias_pattern = self._create_pattern(alias_obj.alias)
                self.search_patterns.append((alias_pattern, tech.id, alias_obj.alias))
        
        # Сортируем по длине паттерна (от длинных к коротким)
        # Это позволяет сначала находить более специфичные совпадения
        self.search_patterns.sort(key=lambda x: len(x[2]), reverse=True)
        
        self.loaded = True
        
        logger.info(f'Загружено {len(self.technologies)} технологий, '
                   f'{len(self.search_patterns)} поисковых паттернов')
        
        return len(self.technologies)
    
    def _create_pattern(self, text):
        """
        Создание регулярного выражения для поиска технологии.
        
        Args:
            text (str): Название технологии или алиас
        
        Returns:
            re.Pattern: Скомпилированное регулярное выражение
        """
        # Экранируем специальные символы
        escaped = re.escape(text)
        
        # Создаем паттерн с границами слов
        # \b не работает с некоторыми символами типа +, #, поэтому используем более гибкий подход
        pattern = r'(?<![a-zA-Z0-9_])' + escaped + r'(?![a-zA-Z0-9_])'
        
        return re.compile(pattern, re.IGNORECASE)
    
    def find_technologies_in_text(self, text: str, 
                                   return_positions: bool = False,
                                   deduplicate: bool = True) -> List[Dict]:
        """
        Поиск технологий в тексте.
        
        Args:
            text (str): Текст для анализа
            return_positions (bool): Возвращать ли позиции найденных технологий
            deduplicate (bool): Убирать ли дубликаты технологий
        
        Returns:
            List[Dict]: Список найденных технологий с информацией
            
        Example:
            >>> finder.find_technologies_in_text("Python, Django, React")
            [
                {
                    'technology': <Technology: Python>,
                    'matched_text': 'Python',
                    'positions': [(0, 6)]  # если return_positions=True
                },
                ...
            ]
        """
        if not self.loaded:
            self.load_technologies()
        
        if not text:
            return []
        
        found_technologies = {}  # {tech_id: {'technology': obj, 'matches': [...]}}
        
        # Поиск по всем паттернам
        for pattern, tech_id, original_text in self.search_patterns:
            matches = pattern.finditer(text)
            
            for match in matches:
                if tech_id not in found_technologies:
                    found_technologies[tech_id] = {
                        'technology': self.technologies[tech_id],
                        'matched_texts': set(),
                        'positions': []
                    }
                
                found_technologies[tech_id]['matched_texts'].add(match.group())
                
                if return_positions:
                    found_technologies[tech_id]['positions'].append(
                        (match.start(), match.end())
                    )
        
        # Формируем результат
        result = []
        for tech_id, data in found_technologies.items():
            item = {
                'technology': data['technology'],
                'matched_text': ', '.join(sorted(data['matched_texts'])),
            }
            
            if return_positions:
                item['positions'] = data['positions']
            
            result.append(item)
        
        # Сортируем по популярности технологии
        result.sort(key=lambda x: x['technology'].popularity, reverse=True)
        
        return result
    
    def extract_technology_names(self, text: str) -> List[str]:
        """
        Извлечение только названий технологий из текста.
        
        Args:
            text (str): Текст для анализа
        
        Returns:
            List[str]: Список названий найденных технологий
        """
        found = self.find_technologies_in_text(text)
        return [item['technology'].name for item in found]
    
    def extract_technology_objects(self, text: str) -> List[Technology]:
        """
        Извлечение объектов технологий из текста.
        
        Args:
            text (str): Текст для анализа
        
        Returns:
            List[Technology]: Список объектов Technology
        """
        found = self.find_technologies_in_text(text)
        return [item['technology'] for item in found]
    
    def find_technologies_by_category(self, text: str, category: str) -> List[Dict]:
        """
        Поиск технологий определенной категории в тексте.
        
        Args:
            text (str): Текст для анализа
            category (str): Категория из TechnologyCategory
        
        Returns:
            List[Dict]: Список найденных технологий указанной категории
        """
        all_found = self.find_technologies_in_text(text)
        return [
            item for item in all_found 
            if item['technology'].category == category
        ]
    
    def get_statistics(self, text: str) -> Dict:
        """
        Получение статистики по найденным технологиям.
        
        Args:
            text (str): Текст для анализа
        
        Returns:
            Dict: Статистика по категориям
            
        Example:
            {
                'total_found': 5,
                'by_category': {
                    'LANG': 2,
                    'FRAMEWORK': 2,
                    'DB': 1
                },
                'technologies': [...]
            }
        """
        found = self.find_technologies_in_text(text)
        
        stats = {
            'total_found': len(found),
            'by_category': {},
            'technologies': found
        }
        
        for item in found:
            category = item['technology'].category
            stats['by_category'][category] = stats['by_category'].get(category, 0) + 1
        
        return stats
    
    def update_technology_popularity(self, technology_ids: List[int]):
        """
        Обновление счетчиков популярности для найденных технологий.
        
        Args:
            technology_ids (List[int]): Список ID технологий для обновления
        """
        if not technology_ids:
            return
        
        # Обновляем счетчики occurrence_count
        technologies = Technology.objects.filter(id__in=technology_ids)
        
        for tech in technologies:
            tech.occurrence_count += 1
            tech.save(update_fields=['occurrence_count'])
        
        logger.debug(f'Обновлены счетчики популярности для {len(technology_ids)} технологий')


# Глобальный экземпляр для использования в других модулях
_global_finder = None


def get_technology_finder() -> TechnologyFinder:
    """
    Получение глобального экземпляра TechnologyFinder.
    
    Returns:
        TechnologyFinder: Глобальный экземпляр поисковика
    """
    global _global_finder
    
    if _global_finder is None:
        _global_finder = TechnologyFinder()
        _global_finder.load_technologies()
    
    return _global_finder

