# Проект: сервис YaCut

## О проекте:
### *Проект YaCut — это сервис укорачивания ссылок. Его назначение — ассоциировать длинную пользовательскую ссылку с короткой, которую предлагает сам пользователь или предоставляет сервис.*

## Ключевые возможности сервиса:
### - *генерация коротких ссылок и связь их с исходными длинными ссылками,*
### - *переадресация на исходный адрес при обращении к коротким ссылкам.*

## Используемые технологии:
- ### Python 3.9
- ### Flask 2.0.2
- ### SQLAlchemy 1.4.29
## Инструкции по установке:

### Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:SkaDin/yacut.git
```

```commandline
cd yacut
```

### Cоздать и активировать виртуальное окружение:

```commandline
python3 -m venv venv
```

* ### Если у вас Linux/macOS

    ```commandline
    source venv/bin/activate
    ```

* ### Если у вас windows

    ```commandline
    source venv/scripts/activate
    ```

### Установить зависимости из файла requirements.txt:

```commandline
python3 -m pip install --upgrade pip
```

```commandline
pip install -r requirements.txt
```
## Пример .env-файла который должен быть создан в папке:

 ```
FLASK_APP=yacut
FLASK_ENV=development
DATABASE_URI=sqlite:///db.sqlite3
SECRET_KEY=My_favorite_micro-framework_is_FLASK!
```
## Автор проекта:
# SkaDin(Денис Сушков)