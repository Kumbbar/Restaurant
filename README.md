<img alt="Logotype" height="256" src="./docs/food.svg" width="256" align="right"/>

# Restaurant business system
REST API Система для автоматизации основных бизнес процессов ресторанов
<!--Блок информации о репозитории в бейджах-->
![Static Badge](https://img.shields.io/badge/Author-Kumbbar-green)
<a href="https://github.com/Kumbbar/RestaurantUI">![Static Badge](https://img.shields.io/badge/UI-link-red)</a>

## Установка

1. Клонирование репозитория 

```git clone https://github.com/Kumbbar/Restaurant```

2. Создание виртуального окружения

```python3 -m venv venv```

3. Активация виртуального окружения

Linux
```source venv/bin/activate```

Windows
```.\venv\Scripts\activate```

4. Установка зависимостей

```pip install -r requirements.txt```

5. Запуск

```python manage.py runserver```

6. Создание базовых прав (Необходимо при новой БД)

```python manage.py create_base_permissions```

Создает 4 права для доступа к разделам API. 
- Администратор
- Общий ресторанный
- Официант
- Повар

## Вход

Логин - Boss

Пароль - 123

## Поддержка
Если у вас возникли сложности или вопросы по использованию системы, создайте 
[обсуждение](https://github.com/Kumbbar/Restaurant/issues/new) в данном репозитории или напишите в [телеграмм](https://t.me/sudo098).

## Зависимости
Эта программа зависит от интепретатора Python версии 3.12 или выше, PIP 23.2.1 или выше.