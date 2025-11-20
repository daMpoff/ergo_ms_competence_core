"""
Дополнительные скрипты для работы с технологиями в модуле skill_map.

Здесь размещаются вспомогательные функции, которые могут вызываться
как из management-команд, так и из REST API.
"""

import io
import logging

from django.core.management import call_command
from django.db import transaction

from modules.competence_core.api.skill_map.models import Technology

logger = logging.getLogger('modules.competence_core.skill_map.scripts')


def clear_technologies():
    """
    Полная очистка таблицы технологий.

    Удаляет все записи Technology. Связанные объекты (алиасы, связи с умениями)
    удаляются каскадно согласно настройкам моделей.

    Returns:
        dict: статистика по удалённым записям.
    """
    with transaction.atomic():
        deleted_count, _details = Technology.objects.all().delete()

    logger.info('Удалено технологий: %s', deleted_count)
    return {'deleted': deleted_count}


def run_init_technologies(*, clear=True, update=True, dry_run=False):
    """
    Обёртка над management-командой init_technologies.

    Args:
        clear (bool): Очистить существующие технологии перед инициализацией.
        update (bool): Обновлять уже существующие записи.
        dry_run (bool): Режим проверки без применения изменений.

    Returns:
        dict: вывод команды (лог) в текстовом виде.
    """
    buffer = io.StringIO()

    logger.info(
        'Запуск init_technologies (clear=%s, update=%s, dry_run=%s)',
        clear,
        update,
        dry_run,
    )

    # stdout перенаправляем в буфер, чтобы при необходимости показать лог в UI.
    call_command(
        'init_technologies',
        clear=clear,
        update=update,
        dry_run=dry_run,
        stdout=buffer,
    )

    output = buffer.getvalue()
    logger.info('init_technologies завершена')

    return {'log': output}