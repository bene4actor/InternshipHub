```markdown
# InternshipHub

Проект для управления документами.

## Настройка

### 1. Клонирование репозитория

Сначала клонируйте репозиторий на свою локальную машину:

```bash
git clone <repository-url>
cd InternshipHub
```

### 2. Изменение переменных окружения

Перед запуском проекта нужно настроить переменные окружения для Django и PostgreSQL.

- Настройки **Django** находятся в файле `.envs.local.django`.
- Настройки **PostgreSQL** находятся в файле `.envs.local.postgres`.

Откройте эти файлы и настройте параметры согласно вашей локальной конфигурации. Например:

- Установите URL базы данных в `.envs.local.django`.
- Измените имя пользователя, пароль и название базы данных в `.envs.local.postgres`.

### 3. Запуск контейнеров Docker

После настройки переменных окружения, вы можете собрать и запустить контейнеры:

```bash
docker-compose -f my_local.yml up --build
```

Эта команда соберет образы (если нужно) и запустит контейнеры для Django, PostgreSQL, Redis, Celery и Flower.

### 4. Доступ к приложению

- Приложение Django: [http://localhost:8000](http://localhost:8000)
- Flower (мониторинг Celery): [http://localhost:5555](http://localhost:5555)

### 5. Создание суперпользователя

После того, как контейнеры будут запущены, создайте суперпользователя для доступа к административной панели Django:

```bash
docker-compose -f my_local.yml exec django python manage.py createsuperuser
```

### 6. Опционально: Запуск Celery Worker

Если вы хотите запустить фоновую обработку задач с помощью Celery, выполните команду:

```bash
docker-compose -f my_local.yml exec celeryworker celery -A config.celery_app worker -l info
```

### 7. Опционально: Запуск Celery Beat

Для запуска периодических задач с Celery Beat выполните команду:

```bash
docker-compose -f my_local.yml exec celerybeat celery -A config.celery_app beat
```

## Развертывание

Для развертывания в продакшн-среде следуйте [документации по Docker для Cookiecutter Django](https://cookiecutter-django.readthedocs.io/en/latest/3-deployment/deployment-with-docker.html) для правильной настройки и конфигурации.

## Лицензия

MIT License. Подробнее см. в [LICENSE](LICENSE).
```
