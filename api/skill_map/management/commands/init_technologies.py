"""
Команда для первичной инициализации технологий в базе данных.

Загружает базовый словарь технологий из technologies_dict.py и создает записи в БД.
"""

import logging
from django.core.management.base import BaseCommand
from django.db import transaction

from modules.competence_core.api.skill_map.models import Technology, TechnologyAlias
from modules.competence_core.api.skill_map.data import ALL_TECHNOLOGIES

logger = logging.getLogger('modules.competence_core.skill_map')


class Command(BaseCommand):
    help = 'Первичная инициализация технологий в базе данных'

    def add_arguments(self, parser):
        parser.add_argument(
            '--update',
            action='store_true',
            help='Обновить существующие технологии (по умолчанию только добавление новых)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Очистить все технологии перед загрузкой (ОСТОРОЖНО!)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Показать что будет сделано, но не применять изменения'
        )

    def handle(self, *args, **options):
        self.stdout.write('=' * 70)
        self.stdout.write(self.style.SUCCESS('Инициализация технологий'))
        self.stdout.write('=' * 70)
        
        dry_run = options.get('dry_run', False)
        update_existing = options.get('update', False)
        clear_all = options.get('clear', False)
        
        if dry_run:
            self.stdout.write(self.style.WARNING('\nРЕЖИМ ПРОВЕРКИ (изменения не будут применены)\n'))
        
        # Статистика
        stats = {
            'created': 0,
            'updated': 0,
            'skipped': 0,
            'deleted': 0,
            'aliases_created': 0,
        }
        
        try:
            with transaction.atomic():
                # Очистка базы (если требуется)
                if clear_all:
                    if dry_run:
                        count = Technology.objects.count()
                        self.stdout.write(
                            self.style.WARNING(f'Будет удалено технологий: {count}')
                        )
                    else:
                        count = Technology.objects.count()
                        Technology.objects.all().delete()
                        stats['deleted'] = count
                        self.stdout.write(
                            self.style.WARNING(f'Удалено технологий: {count}')
                        )
                
                # Словарь для связывания родительских технологий
                tech_registry = {}
                
                # Первый проход: создаем/обновляем технологии без родителей
                self.stdout.write('\nОбработка технологий...\n')
                
                for tech_data in ALL_TECHNOLOGIES:
                    tech_name = tech_data['name']
                    
                    # Пропускаем технологии с родителями на первом проходе
                    if tech_data.get('parent'):
                        continue
                    
                    result = self._process_technology(
                        tech_data, 
                        tech_registry, 
                        update_existing, 
                        dry_run
                    )
                    
                    if result:
                        tech_obj, created, updated, aliases_count = result
                        if created:
                            stats['created'] += 1
                        elif updated:
                            stats['updated'] += 1
                        else:
                            stats['skipped'] += 1
                        stats['aliases_created'] += aliases_count
                
                # Второй проход: создаем технологии с родителями
                for tech_data in ALL_TECHNOLOGIES:
                    if not tech_data.get('parent'):
                        continue
                    
                    result = self._process_technology(
                        tech_data, 
                        tech_registry, 
                        update_existing, 
                        dry_run
                    )
                    
                    if result:
                        tech_obj, created, updated, aliases_count = result
                        if created:
                            stats['created'] += 1
                        elif updated:
                            stats['updated'] += 1
                        else:
                            stats['skipped'] += 1
                        stats['aliases_created'] += aliases_count
                
                # Отменяем транзакцию при dry-run
                if dry_run:
                    transaction.set_rollback(True)
        
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'\nОшибка при инициализации: {e}')
            )
            logger.exception('Ошибка при инициализации технологий')
            return
        
        # Вывод статистики
        self.stdout.write('\n' + '=' * 70)
        self.stdout.write(self.style.SUCCESS('СТАТИСТИКА:'))
        self.stdout.write('=' * 70)
        
        if stats['deleted'] > 0:
            self.stdout.write(f"Удалено технологий: {stats['deleted']}")
        
        self.stdout.write(
            self.style.SUCCESS(f"Создано новых технологий: {stats['created']}")
        )
        
        if update_existing:
            self.stdout.write(
                self.style.WARNING(f"Обновлено технологий: {stats['updated']}")
            )
        
        if stats['skipped'] > 0:
            self.stdout.write(f"Пропущено (уже существуют): {stats['skipped']}")
        
        self.stdout.write(
            self.style.SUCCESS(f"Создано алиасов: {stats['aliases_created']}")
        )
        
        total_in_db = len(tech_registry) if dry_run else Technology.objects.count()
        self.stdout.write(f"\nВсего технологий в базе: {total_in_db}")
        
        self.stdout.write('=' * 70)
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING('\nИзменения не применены (режим проверки)')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('\nИнициализация успешно завершена!')
            )

    def _process_technology(self, tech_data, tech_registry, update_existing, dry_run):
        """
        Обработка одной технологии.
        
        Returns:
            tuple: (tech_obj, created, updated, aliases_count) или None
        """
        tech_name = tech_data['name']
        
        # Проверяем существование
        existing_tech = None
        if not dry_run:
            try:
                existing_tech = Technology.objects.get(name=tech_name)
            except Technology.DoesNotExist:
                pass
        
        created = False
        updated = False
        aliases_count = 0
        # Генерируем метрики, близкие к реальным, детерминированно от данных технологии
        pop_val, rel_val, occ_val = self._calculate_metrics(tech_data)
        
        # Получаем родительскую технологию
        parent_tech = None
        if tech_data.get('parent'):
            parent_name = tech_data['parent']
            if parent_name in tech_registry:
                parent_tech = tech_registry[parent_name]
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Родитель '{parent_name}' для '{tech_name}' не найден"
                    )
                )
        
        if existing_tech:
            if update_existing:
                # Обновляем существующую технологию
                if not dry_run:
                    existing_tech.category = tech_data['category']
                    existing_tech.description = tech_data.get('description', '')
                    existing_tech.parent_tech = parent_tech
                    existing_tech.popularity = pop_val
                    existing_tech.relevance = rel_val
                    existing_tech.occurrence_count = occ_val
                    existing_tech.popularity = pop_val
                    existing_tech.relevance = rel_val
                    existing_tech.occurrence_count = occ_val
                    existing_tech.save()
                
                self.stdout.write(
                    self.style.WARNING(f"  Обновлено: {tech_name}")
                )
                tech_obj = existing_tech
                updated = True
            else:
                # Пропускаем существующую
                self.stdout.write(f"  Пропущено: {tech_name} (уже существует)")
                tech_obj = existing_tech
        else:
            # Создаем новую технологию
            if dry_run:
                self.stdout.write(
                    self.style.SUCCESS(f"  Будет создано: {tech_name}")
                )
                tech_obj = Technology(
                    name=tech_name,
                    category=tech_data['category'],
                    description=tech_data.get('description', ''),
                    parent_tech=parent_tech,
                    popularity=pop_val,
                    relevance=rel_val,
                    occurrence_count=occ_val,
                )
            else:
                tech_obj = Technology.objects.create(
                    name=tech_name,
                    category=tech_data['category'],
                    description=tech_data.get('description', ''),
                    parent_tech=parent_tech,
                    popularity=pop_val,
                    relevance=rel_val,
                    occurrence_count=occ_val,
                )
                self.stdout.write(
                    self.style.SUCCESS(f"  Создано: {tech_name}")
                )
            
            created = True
        
        # Добавляем в реестр
        tech_registry[tech_name] = tech_obj
        
        # Создаем алиасы
        if tech_data.get('aliases') and not dry_run:
            for alias in tech_data['aliases']:
                # Проверяем, не существует ли уже такой алиас
                if not TechnologyAlias.objects.filter(
                    technology=tech_obj, 
                    alias=alias
                ).exists():
                    TechnologyAlias.objects.create(
                        technology=tech_obj,
                        alias=alias
                    )
                    aliases_count += 1
        elif tech_data.get('aliases') and dry_run:
            aliases_count = len(tech_data['aliases'])
        
        return tech_obj, created, updated, aliases_count

    @staticmethod
    def _calculate_metrics(tech_data):
        """
        Детерминированно генерируем метрики, имитируя реалистичные значения.
        Учитываем категорию, наличие алиасов и родителя.
        """
        from zlib import crc32

        name = tech_data['name']
        category = tech_data['category']
        aliases = tech_data.get('aliases') or []
        has_parent = bool(tech_data.get('parent'))

        seed = crc32(f'{name}:{category}'.encode('utf-8')) & 0xffffffff
        alias_bonus = min(8, len(aliases) * 2)  # до +8 за алиасы
        parent_penalty = -3 if has_parent else 0  # дочерним немного ниже базу

        category_base = {
            'FRAMEWORK': 80,
            'LANG': 85,
            'LIBRARY': 72,
            'TOOL': 68,
            'DB': 78,
            'PLATFORM': 74,
            'PROTOCOL': 62,
            'SERVICE': 75,
        }
        base = category_base.get(category, 70)

        # Популярность: база по категории + шум от seed + бонус алиасов + коррекция за родителя
        popularity = base + (seed % 12) - 5 + alias_bonus + parent_penalty
        popularity = max(40, min(98, popularity))

        # Релевантность: от 0.60 до 0.97, чуть выше для одиночных корневых технологий
        relevance = 0.60 + ((seed >> 8) % 30) / 100
        if not has_parent:
            relevance += 0.03
        relevance = round(max(0.55, min(0.97, relevance)), 2)

        # Упоминания: базово завязаны на популярность, с шумом и бонусом алиасов
        occurrence_count = int(popularity * 0.7 + ((seed >> 16) % 20) + alias_bonus * 2)
        occurrence_count = max(5, min(250, occurrence_count))

        return popularity, relevance, occurrence_count

