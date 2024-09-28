# WarehouseAndProduct Project
## Описание проекта
При помощи механизмов Django REST в проекте реализован следующий функционал:
 - Регистрация пользователя по имейлу и паролю с указанием типа поставщик, потребитель
 - Аутентификация пользователя
 - Создание склада
 - Создание товара
 - Поставщик должен иметь возможность поставлять товар на выбранный склад
 - Потребитель должен иметь возможность забирать товар со склада
   
Ограничения:
 - Потребитель не может поставлять товар
 - Поставщик не может получать товар
 - Потребитель не может получить товара больше, чем имеется на складе
## Запуск проекта
### 1. Создание виртуального окружения
Создайте виртуальное окружение для изоляции зависимостей проекта:
```bash
python -m venv venv
```
### 2. Активация виртуального окружения
```bash
venv\Scripts\activate
```
### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```
### 4. Запуск проекта
Для запуска сервера необходимо прописать python manage.py runserver в терминале
