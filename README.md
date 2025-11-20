# Competence Core Module

**Модуль управления компетенциями и анализа профессиональных требований**

Модуль предоставляет комплексную систему для работы с компетенциями, умениями, технологиями и профилями вакансий в рамках системы анализа рынка труда.

---

## 📋 Содержание

- [Обзор](#обзор)
- [Архитектура](#архитектура)
- [Основные компоненты](#основные-компоненты)
- [Структура данных](#структура-данных)
- [API](#api)
- [Frontend](#frontend)
- [Установка и настройка](#установка-и-настройка)
- [Использование](#использование)
- [Разработка](#разработка)

---

## 🎯 Обзор

Модуль `competence_core` решает задачи:

- **Управление компетенциями** - создание, классификация и анализ профессиональных компетенций
- **Карта технологий (Skill Map)** - ведение справочника технологий, инструментов и платформ
- **Связь умений и технологий** - формирование точных компонентов компетенций
- **Профили вакансий** - анализ и структурирование требований из вакансий
- **Аналитика** - расчет популярности, релевантности и трендов

### Ключевые возможности

✅ Иерархическая структура компетенций  
✅ Автоматический поиск технологий в текстах  
✅ Система синонимов и альтернативных названий  
✅ Интеграция с различными источниками вакансий  
✅ Веб-интерфейс с фильтрацией и визуализацией  
✅ RESTful API для внешних интеграций  

---

## 🏗️ Архитектура

```
competence_core/
├── api/                          # Backend (Django)
│   ├── models.py                 # Модели компетенций и профилей
│   ├── views.py                  # API endpoints
│   ├── serializers.py            # Сериализаторы
│   ├── urls.py                   # Маршруты
│   └── skill_map/                # Подмодуль карты технологий
│       ├── models.py             # Модели умений и технологий
│       ├── views.py              # API для skill map
│       ├── utils/
│       │   └── technology_finder.py  # Поиск технологий в тексте
│       ├── data/
│       │   └── technologies_dict.py  # Справочник технологий
│       └── management/commands/
│           └── init_technologies.py  # Команда инициализации
│
└── client/                       # Frontend (Vue.js)
    ├── pages/                    # Страницы
    │   ├── CompetenceCoreDashboardPage.vue
    │   ├── CompetencesListPage.vue
    │   ├── TechnologiesListPage.vue
    │   ├── VacancyProfilesListPage.vue
    │   └── components/           # Переиспользуемые компоненты
    ├── js/                       # Логика и композаблы
    │   ├── routes.js
    │   ├── endpoints.js
    │   └── use*.js               # Composition API композаблы
    └── scss/                     # Стили
```

---

## 🧩 Основные компоненты

### 1. Компетенции (Competence)

**Модель:** `api/models.py::Competence`

Профессиональная компетенция, сформированная из набора умений и технологий.

**Поля:**
- `name` - название компетенции
- `level` - уровень (Junior/Middle/Senior/Expert)
- `popularity` - показатель популярности
- `relevance` - коэффициент актуальности (0.0-1.0)
- `is_core` - является ли ключевой

**Связи:**
- `components` - компоненты компетенции (умения + технологии)
- `vacancy_profiles` - профили вакансий

### 2. Карта технологий (Skill Map)

**Модули:** `api/skill_map/`

#### Technology (Технологии)
Справочник технологий, инструментов и платформ.

**Категории:**
- `LANG` - Языки программирования
- `FRAMEWORK` - Фреймворки
- `LIBRARY` - Библиотеки
- `DB` - Базы данных
- `PLATFORM` - Платформы
- `PROTOCOL` - Протоколы
- `SERVICE` - Сервисы
- `TOOL` - Инструменты

**Особенности:**
- Иерархическая структура (parent_tech)
- Система альтернативных названий (TechnologyAlias)
- Отслеживание популярности и упоминаний

#### Skill (Умения)
Базовые профессиональные умения.

**Категории:**
- `TECH` - Технические
- `METHOD` - Методические
- `SOFT` - Софт-скиллы
- `DOMAIN` - Предметные

#### SkillTechnology (Связь)
Связь между умением и технологией (например, "Веб-разработка + Django").

### 3. Профили вакансий

**Модель:** `VacancyCompetenceProfile`

Анализ требований вакансии через набор компетенций.

**Особенности:**
- GenericForeignKey для связи с разными источниками вакансий
- Приоритизация компетенций
- Определение обязательных и желаемых навыков

---

## 📊 Структура данных

### Схема связей

```
Competence (Компетенция)
    ↓ (many-to-many через CompetenceComponent)
Skill (Умение) ←→ SkillTechnology ←→ Technology (Технология)
    ↓                                      ↓
SkillSynonym                        TechnologyAlias
(Синонимы)                    (Альтернативные названия)

VacancyCompetenceProfile (Профиль вакансии)
    ↓ (GenericForeignKey)
Vacancy (Любая модель вакансии из других модулей)
    ↓ (many-to-many через VacancyCompetence)
Competence (Компетенция)
```

### Таблицы БД

- `cc_competence` - компетенции
- `cc_competence_component` - компоненты компетенций
- `cc_vacancy_profile` - профили вакансий
- `cc_vacancy_competence` - связь вакансий и компетенций
- `cc_sm_skill` - умения
- `cc_sm_skill_synonym` - синонимы умений
- `cc_sm_technology` - технологии
- `cc_sm_technology_alias` - альтернативные названия технологий
- `cc_sm_skill_technology` - связи умений и технологий

---

## 🔌 API

### Основные endpoints

#### Компетенции
```
GET    /api/competence-core/competences/          # Список компетенций
GET    /api/competence-core/competences/{id}/     # Детали компетенции
POST   /api/competence-core/competences/          # Создание
PUT    /api/competence-core/competences/{id}/     # Обновление
DELETE /api/competence-core/competences/{id}/     # Удаление
```

#### Технологии (Skill Map)
```
GET    /api/competence-core/skill-map/technologies/              # Список технологий
GET    /api/competence-core/skill-map/technologies/{id}/         # Детали
POST   /api/competence-core/skill-map/technologies/              # Создание
GET    /api/competence-core/skill-map/technologies/{id}/aliases/ # Синонимы
POST   /api/competence-core/skill-map/technologies/bulk-clear/   # Очистка всех
POST   /api/competence-core/skill-map/technologies/initialize/   # Инициализация
```

#### Профили вакансий
```
GET    /api/competence-core/vacancy-profiles/     # Список профилей
GET    /api/competence-core/vacancy-profiles/{id}/  # Детали профиля
```

### Параметры фильтрации

**Технологии:**
- `?category=LANG` - по категории
- `?search=python` - текстовый поиск
- `?ordering=-popularity` - сортировка
- `?page_size=50` - размер страницы

**Компетенции:**
- `?level=MIDDLE` - по уровню
- `?is_core=true` - только ключевые
- `?ordering=-relevance` - сортировка

---

## 🖥️ Frontend

### Страницы

#### 1. Dashboard (`CompetenceCoreDashboardPage.vue`)
Панель управления модулем с общей статистикой.

**Маршрут:** `/competence-core/dashboard`

#### 2. Карта технологий (`TechnologiesListPage.vue`)
Интерактивный справочник технологий.

**Маршрут:** `/competence-core/technologies`

**Возможности:**
- Два режима отображения (таблица / карточки)
- Фильтрация по категориям
- Поиск по названию и описанию
- Сортировка (популярность, упоминания, релевантность)
- Просмотр синонимов и дочерних технологий
- Пагинация

**Архитектура компонента:**
```
TechnologiesListPage.vue (228 строк)
├── TechnologyToolbar      # Панель инструментов
├── TechnologyFilters      # Фильтры по категориям
├── TechnologyTableView    # Табличное представление
├── TechnologyCardsView    # Карточное представление
├── TechnologyDetails      # Детали (синонимы + дочерние)
└── TechnologyPagination   # Пагинация
```

#### 3. Компетенции (`CompetencesListPage.vue`)
Список и управление компетенциями.

**Маршрут:** `/competence-core/competences`

#### 4. Профили вакансий (`VacancyProfilesListPage.vue`)
Анализ требований вакансий.

**Маршрут:** `/competence-core/vacancies`

### Композаблы (Composition API)

- `useTechnologies.js` - работа с технологиями
- `useTechnologiesListPage.js` - логика страницы списка
- `useCompetences.js` - работа с компетенциями
- `useVacancyProfiles.js` - работа с профилями вакансий

---

## 🚀 Установка и настройка

### 1. Применение миграций

```bash
# Backend миграции
python manage.py migrate competence_core
python manage.py migrate skill_map
```

### 2. Инициализация технологий

```bash
# Загрузка базового справочника технологий
python manage.py init_technologies

# С очисткой существующих данных
python manage.py init_technologies --clear

# Пробный запуск (без сохранения)
python manage.py init_technologies --dry-run
```

### 3. Настройка маршрутов

Frontend маршруты регистрируются автоматически из `client/js/routes.js`.

---

## 💡 Использование

### Пример 1: Создание компетенции

```python
from modules.competence_core.api.models import Competence, CompetenceComponent
from modules.competence_core.api.skill_map.models import Skill, Technology, SkillTechnology

# Создание компетенции
backend_comp = Competence.objects.create(
    name='Backend разработка на Python',
    level='MIDDLE',
    popularity=95,
    relevance=0.98,
    is_core=True
)

# Добавление компонентов
python_skill = Skill.objects.get(name='Программирование на Python')
django_tech = Technology.objects.get(name='Django')
skill_tech = SkillTechnology.objects.get(skill=python_skill, technology=django_tech)

CompetenceComponent.objects.create(
    competence=backend_comp,
    skill=python_skill,
    skill_technology=skill_tech,
    importance=0.95,
    weight=1.0
)
```

### Пример 2: Поиск технологий в тексте

```python
from modules.competence_core.api.skill_map.utils.technology_finder import TechnologyFinder

finder = TechnologyFinder()
text = "Ищем Python разработчика с опытом Django и PostgreSQL"
found = finder.find_technologies(text)

# Результат: [
#   {'technology': <Technology: Python>, 'category': 'LANG'},
#   {'technology': <Technology: Django>, 'category': 'FRAMEWORK'},
#   {'technology': <Technology: PostgreSQL>, 'category': 'DB'}
# ]
```

### Пример 3: Создание профиля вакансии

```python
from modules.competence_core.api.models import VacancyCompetenceProfile, VacancyCompetence
from modules.vacancies_parser.headhunter.models import Vacancy

vacancy = Vacancy.objects.first()

# Создание профиля
profile = VacancyCompetenceProfile.objects.create(
    vacancy=vacancy,
    vacancy_title=vacancy.title,
    vacancy_source='HeadHunter'
)

# Добавление компетенций
VacancyCompetence.objects.create(
    vacancy_profile=profile,
    competence=backend_comp,
    priority=1,
    required_level='MIDDLE',
    is_mandatory=True,
    weight=1.0
)
```

---

## 👨‍💻 Разработка

### Стандарты кодирования

- **Backend:** Django best practices, type hints, docstrings
- **Frontend:** Vue 3 Composition API, декомпозиция компонентов
- **Максимальный размер файла:** 700 строк
- **Стили:** SCSS, модульная структура
- **Локализация:** русский язык

### Структура компонентов

Каждый крупный Vue компонент должен быть декомпозирован:

```
ComponentPage.vue (главный, < 250 строк)
├── components/
│   ├── ComponentToolbar.vue
│   ├── ComponentFilters.vue
│   └── ComponentDetails.vue
├── js/
│   └── useComponent.js (композабл)
└── scss/
    ├── ComponentPage.scss (главный файл)
    └── components/ (модульные стили)
```

### Тестирование

```bash
# Backend тесты
python manage.py test modules.competence_core

# Конкретный тест
python manage.py test modules.competence_core.api.skill_map.tests
```

### Миграции

```bash
# Создание миграций
python manage.py makemigrations competence_core
python manage.py makemigrations skill_map

# Применение
python manage.py migrate
```


## 📄 Лицензия

Внутренний модуль системы ErgoMS. Все права защищены.

---

## 🤝 Поддержка

При возникновении вопросов или проблем:
1. Проверьте документацию выше
2. Изучите примеры использования
3. Обратитесь к команде разработки

---

**Версия документации:** 1.1.0  
**Дата обновления:** 20.11.2025

