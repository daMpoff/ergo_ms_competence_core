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
"""

# ============================================================
# ЯЗЫКИ ПРОГРАММИРОВАНИЯ
# ============================================================
PROGRAMMING_LANGUAGES = [
    {
        'name': 'Python',
        'category': 'LANG',
        'description': 'Высокоуровневый язык программирования общего назначения',
        'aliases': ['python', 'py', 'Python3', 'python3'],
    },
    {
        'name': 'JavaScript',
        'category': 'LANG',
        'description': 'Язык программирования для веб-разработки',
        'aliases': ['javascript', 'js', 'JS', 'ECMAScript'],
    },
    {
        'name': 'TypeScript',
        'category': 'LANG',
        'description': 'Типизированное расширение JavaScript',
        'aliases': ['typescript', 'ts', 'TS'],
        'parent': 'JavaScript',
    },
    {
        'name': 'Java',
        'category': 'LANG',
        'description': 'Объектно-ориентированный язык программирования',
        'aliases': ['java', 'Java SE', 'Java EE'],
    },
    {
        'name': 'C#',
        'category': 'LANG',
        'description': 'Язык программирования от Microsoft',
        'aliases': ['csharp', 'C Sharp', 'c#', 'C-Sharp'],
    },
    {
        'name': 'C++',
        'category': 'LANG',
        'description': 'Компилируемый язык программирования общего назначения',
        'aliases': ['cpp', 'c++', 'C plus plus', 'cplusplus'],
    },
    {
        'name': 'C',
        'category': 'LANG',
        'description': 'Процедурный язык программирования',
        'aliases': ['c', 'C language'],
    },
    {
        'name': 'Go',
        'category': 'LANG',
        'description': 'Язык программирования от Google',
        'aliases': ['golang', 'Go lang', 'go'],
    },
    {
        'name': 'Rust',
        'category': 'LANG',
        'description': 'Системный язык программирования',
        'aliases': ['rust', 'rust-lang'],
    },
    {
        'name': 'PHP',
        'category': 'LANG',
        'description': 'Язык программирования для веб-разработки',
        'aliases': ['php', 'PHP7', 'PHP8'],
    },
    {
        'name': 'Ruby',
        'category': 'LANG',
        'description': 'Динамический язык программирования',
        'aliases': ['ruby', 'Ruby lang'],
    },
    {
        'name': 'Swift',
        'category': 'LANG',
        'description': 'Язык программирования для iOS/macOS',
        'aliases': ['swift', 'Swift lang'],
    },
    {
        'name': 'Kotlin',
        'category': 'LANG',
        'description': 'Современный язык программирования для JVM',
        'aliases': ['kotlin', 'Kotlin lang'],
    },
    {
        'name': 'R',
        'category': 'LANG',
        'description': 'Язык программирования для статистики и анализа данных',
        'aliases': ['R lang', 'r'],
    },
    {
        'name': 'Scala',
        'category': 'LANG',
        'description': 'Функциональный и объектно-ориентированный язык для JVM',
        'aliases': ['scala'],
    },
]

# ============================================================
# ФРЕЙМВОРКИ И БИБЛИОТЕКИ - BACKEND
# ============================================================
BACKEND_FRAMEWORKS = [
    {
        'name': 'Django',
        'category': 'FRAMEWORK',
        'description': 'Высокоуровневый веб-фреймворк на Python',
        'aliases': ['django', 'Django Framework'],
        'parent': 'Python',
    },
    {
        'name': 'Django REST Framework',
        'category': 'FRAMEWORK',
        'description': 'Инструмент для создания REST API на Django',
        'aliases': ['DRF', 'django-rest-framework', 'djangorestframework'],
        'parent': 'Django',
    },
    {
        'name': 'Flask',
        'category': 'FRAMEWORK',
        'description': 'Микрофреймворк для веб-разработки на Python',
        'aliases': ['flask', 'Flask Framework'],
        'parent': 'Python',
    },
    {
        'name': 'FastAPI',
        'category': 'FRAMEWORK',
        'description': 'Современный быстрый веб-фреймворк на Python',
        'aliases': ['fastapi', 'Fast API'],
        'parent': 'Python',
    },
    {
        'name': 'Spring',
        'category': 'FRAMEWORK',
        'description': 'Фреймворк для enterprise-приложений на Java',
        'aliases': ['spring', 'Spring Framework', 'Spring Boot'],
        'parent': 'Java',
    },
    {
        'name': 'Express.js',
        'category': 'FRAMEWORK',
        'description': 'Минималистичный веб-фреймворк для Node.js',
        'aliases': ['express', 'expressjs', 'Express'],
        'parent': 'JavaScript',
    },
    {
        'name': 'Node.js',
        'category': 'PLATFORM',
        'description': 'JavaScript-среда выполнения на стороне сервера',
        'aliases': ['nodejs', 'node', 'Node'],
        'parent': 'JavaScript',
    },
    {
        'name': 'ASP.NET',
        'category': 'FRAMEWORK',
        'description': 'Веб-фреймворк от Microsoft',
        'aliases': ['aspnet', 'asp.net', 'ASP.NET Core'],
        'parent': 'C#',
    },
    {
        'name': 'Laravel',
        'category': 'FRAMEWORK',
        'description': 'PHP-фреймворк для веб-разработки',
        'aliases': ['laravel', 'Laravel Framework'],
        'parent': 'PHP',
    },
    {
        'name': 'Ruby on Rails',
        'category': 'FRAMEWORK',
        'description': 'Веб-фреймворк на Ruby',
        'aliases': ['rails', 'RoR', 'Ruby Rails'],
        'parent': 'Ruby',
    },
]

# ============================================================
# ФРЕЙМВОРКИ И БИБЛИОТЕКИ - FRONTEND
# ============================================================
FRONTEND_FRAMEWORKS = [
    {
        'name': 'React',
        'category': 'FRAMEWORK',
        'description': 'JavaScript-библиотека для создания пользовательских интерфейсов',
        'aliases': ['react', 'reactjs', 'React.js'],
        'parent': 'JavaScript',
    },
    {
        'name': 'Next.js',
        'category': 'FRAMEWORK',
        'description': 'React-фреймворк для production',
        'aliases': ['nextjs', 'next', 'Next'],
        'parent': 'React',
    },
    {
        'name': 'Vue.js',
        'category': 'FRAMEWORK',
        'description': 'Прогрессивный JavaScript-фреймворк',
        'aliases': ['vue', 'vuejs', 'Vue'],
        'parent': 'JavaScript',
    },
    {
        'name': 'Nuxt.js',
        'category': 'FRAMEWORK',
        'description': 'Vue-фреймворк для production',
        'aliases': ['nuxt', 'nuxtjs', 'Nuxt'],
        'parent': 'Vue.js',
    },
    {
        'name': 'Angular',
        'category': 'FRAMEWORK',
        'description': 'Платформа для создания веб-приложений',
        'aliases': ['angular', 'angularjs', 'Angular2+'],
        'parent': 'TypeScript',
    },
    {
        'name': 'Svelte',
        'category': 'FRAMEWORK',
        'description': 'Компилируемый JavaScript-фреймворк',
        'aliases': ['svelte', 'sveltejs'],
        'parent': 'JavaScript',
    },
    {
        'name': 'jQuery',
        'category': 'LIBRARY',
        'description': 'JavaScript-библиотека для работы с DOM',
        'aliases': ['jquery', 'JQuery'],
        'parent': 'JavaScript',
    },
]

# ============================================================
# БАЗЫ ДАННЫХ
# ============================================================
DATABASES = [
    {
        'name': 'PostgreSQL',
        'category': 'DB',
        'description': 'Объектно-реляционная система управления базами данных',
        'aliases': ['postgres', 'postgresql', 'psql', 'Postgres'],
    },
    {
        'name': 'MySQL',
        'category': 'DB',
        'description': 'Реляционная система управления базами данных',
        'aliases': ['mysql', 'My SQL'],
    },
    {
        'name': 'MongoDB',
        'category': 'DB',
        'description': 'Документо-ориентированная NoSQL база данных',
        'aliases': ['mongodb', 'mongo', 'Mongo DB'],
    },
    {
        'name': 'Redis',
        'category': 'DB',
        'description': 'Хранилище структур данных в памяти',
        'aliases': ['redis', 'Redis DB'],
    },
    {
        'name': 'Microsoft SQL Server',
        'category': 'DB',
        'description': 'Система управления реляционными базами данных от Microsoft',
        'aliases': ['mssql', 'MS SQL', 'SQL Server', 'MSSQL'],
    },
    {
        'name': 'Oracle Database',
        'category': 'DB',
        'description': 'Объектно-реляционная СУБД от Oracle',
        'aliases': ['oracle', 'Oracle DB', 'OracleDB'],
    },
    {
        'name': 'SQLite',
        'category': 'DB',
        'description': 'Встраиваемая реляционная база данных',
        'aliases': ['sqlite', 'sqlite3'],
    },
    {
        'name': 'Elasticsearch',
        'category': 'DB',
        'description': 'Поисковая и аналитическая система',
        'aliases': ['elasticsearch', 'elastic', 'ES'],
    },
    {
        'name': 'Cassandra',
        'category': 'DB',
        'description': 'Распределенная NoSQL база данных',
        'aliases': ['cassandra', 'Apache Cassandra'],
    },
    {
        'name': 'ClickHouse',
        'category': 'DB',
        'description': 'Колоночная СУБД для аналитики',
        'aliases': ['clickhouse', 'ClickHouse DB'],
    },
]

# ============================================================
# ИНСТРУМЕНТЫ РАЗРАБОТКИ
# ============================================================
DEV_TOOLS = [
    {
        'name': 'Git',
        'category': 'TOOL',
        'description': 'Распределенная система контроля версий',
        'aliases': ['git', 'Git VCS'],
    },
    {
        'name': 'Docker',
        'category': 'TOOL',
        'description': 'Платформа для контейнеризации приложений',
        'aliases': ['docker', 'Docker Engine'],
    },
    {
        'name': 'Kubernetes',
        'category': 'TOOL',
        'description': 'Система оркестрации контейнеров',
        'aliases': ['kubernetes', 'k8s', 'K8s'],
    },
    {
        'name': 'Jenkins',
        'category': 'TOOL',
        'description': 'Сервер автоматизации для CI/CD',
        'aliases': ['jenkins', 'Jenkins CI'],
    },
    {
        'name': 'GitLab CI',
        'category': 'TOOL',
        'description': 'Инструмент для непрерывной интеграции',
        'aliases': ['gitlab-ci', 'GitLab CI/CD', 'gitlab'],
    },
    {
        'name': 'Nginx',
        'category': 'TOOL',
        'description': 'Веб-сервер и обратный прокси-сервер',
        'aliases': ['nginx', 'NGINX'],
    },
    {
        'name': 'Apache',
        'category': 'TOOL',
        'description': 'HTTP-сервер',
        'aliases': ['apache', 'Apache HTTP Server', 'httpd'],
    },
    {
        'name': 'Webpack',
        'category': 'TOOL',
        'description': 'Сборщик модулей для JavaScript',
        'aliases': ['webpack'],
    },
    {
        'name': 'Vite',
        'category': 'TOOL',
        'description': 'Инструмент сборки для фронтенда',
        'aliases': ['vite', 'vitejs'],
    },
]

# ============================================================
# БИБЛИОТЕКИ ДЛЯ DATA SCIENCE И ML
# ============================================================
DATA_SCIENCE_LIBRARIES = [
    {
        'name': 'NumPy',
        'category': 'LIBRARY',
        'description': 'Библиотека для работы с многомерными массивами',
        'aliases': ['numpy', 'np'],
        'parent': 'Python',
    },
    {
        'name': 'Pandas',
        'category': 'LIBRARY',
        'description': 'Библиотека для анализа и обработки данных',
        'aliases': ['pandas', 'pd'],
        'parent': 'Python',
    },
    {
        'name': 'Scikit-learn',
        'category': 'LIBRARY',
        'description': 'Библиотека машинного обучения',
        'aliases': ['sklearn', 'scikit-learn', 'scikit learn'],
        'parent': 'Python',
    },
    {
        'name': 'TensorFlow',
        'category': 'FRAMEWORK',
        'description': 'Платформа для машинного обучения',
        'aliases': ['tensorflow', 'tf', 'TF'],
        'parent': 'Python',
    },
    {
        'name': 'PyTorch',
        'category': 'FRAMEWORK',
        'description': 'Библиотека машинного обучения',
        'aliases': ['pytorch', 'torch'],
        'parent': 'Python',
    },
    {
        'name': 'Keras',
        'category': 'FRAMEWORK',
        'description': 'Высокоуровневый API для нейронных сетей',
        'aliases': ['keras'],
        'parent': 'Python',
    },
    {
        'name': 'Matplotlib',
        'category': 'LIBRARY',
        'description': 'Библиотека для визуализации данных',
        'aliases': ['matplotlib', 'mpl'],
        'parent': 'Python',
    },
    {
        'name': 'Seaborn',
        'category': 'LIBRARY',
        'description': 'Библиотека для статистической визуализации',
        'aliases': ['seaborn', 'sns'],
        'parent': 'Python',
    },
]

# ============================================================
# ОБЛАЧНЫЕ ПЛАТФОРМЫ И СЕРВИСЫ
# ============================================================
CLOUD_PLATFORMS = [
    {
        'name': 'AWS',
        'category': 'PLATFORM',
        'description': 'Amazon Web Services - облачная платформа',
        'aliases': ['aws', 'Amazon Web Services', 'amazon aws'],
    },
    {
        'name': 'Google Cloud',
        'category': 'PLATFORM',
        'description': 'Облачная платформа от Google',
        'aliases': ['gcp', 'Google Cloud Platform', 'GCP'],
    },
    {
        'name': 'Microsoft Azure',
        'category': 'PLATFORM',
        'description': 'Облачная платформа от Microsoft',
        'aliases': ['azure', 'Azure', 'MS Azure'],
    },
    {
        'name': 'Heroku',
        'category': 'PLATFORM',
        'description': 'Облачная платформа как сервис',
        'aliases': ['heroku'],
    },
]

# ============================================================
# ПРОТОКОЛЫ И API
# ============================================================
PROTOCOLS = [
    {
        'name': 'REST',
        'category': 'PROTOCOL',
        'description': 'Архитектурный стиль для API',
        'aliases': ['rest', 'REST API', 'RESTful'],
    },
    {
        'name': 'GraphQL',
        'category': 'PROTOCOL',
        'description': 'Язык запросов для API',
        'aliases': ['graphql', 'GraphQL API'],
    },
    {
        'name': 'gRPC',
        'category': 'PROTOCOL',
        'description': 'Высокопроизводительный RPC-фреймворк',
        'aliases': ['grpc', 'gRPC'],
    },
    {
        'name': 'WebSocket',
        'category': 'PROTOCOL',
        'description': 'Протокол для двусторонней связи',
        'aliases': ['websocket', 'ws', 'WebSockets'],
    },
]

# ============================================================
# ОБЪЕДИНЕННЫЙ СЛОВАРЬ
# ============================================================
ALL_TECHNOLOGIES = (
    PROGRAMMING_LANGUAGES +
    BACKEND_FRAMEWORKS +
    FRONTEND_FRAMEWORKS +
    DATABASES +
    DEV_TOOLS +
    DATA_SCIENCE_LIBRARIES +
    CLOUD_PLATFORMS +
    PROTOCOLS
)

