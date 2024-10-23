# Neural Network

Этот проект представляет собой реализацию нейронной сети на языке программирования Python. Проект включает в себя несколько модулей для построения, конфигурирования, логирования и тестирования нейронной сети.

---

## Структура проекта

- `main.py`: Основной модуль для запуска процесса создания и визуализации нейронной сети.
- `neural_network.py`: Модуль, содержащий классы и методы для построения и управления слоями нейронной сети.
- `logging.json`: Конфигурация для системы логирования проекта.
- `configuration.py`: Модуль для загрузки конфигурации логирования из JSON файла.
- `tests.py`: Модуль для выполнения тестов, проверяющих корректность работы системы.

---

## Установка

### Требования
- Python 3.12.7

## Запуск

Для запуска основного процесса создания и визуализации нейронной сети выполните:
```bash
python main.py
```

---

## Описание модулей

### main.py
Основная функция, запускающая процесс создания и визуализации нейронной сети.

### neural_network.py
Этот модуль включает классы `LayerBuilder`, `InputLayer`, `DeepLayer`, `OutputLayer` и `NeuralNetwork`, каждый из которых отвечает за определенные аспекты архитектуры нейронной сети.

### logging.json
JSON файл для конфигурации системы логирования.

### configuration.py
Этот модуль загружает конфигурацию логирования из JSON файла и настраивает логгер.

### tests.py
Содержит набор тестов для проверки функциональности нейронной сети.

---

## Запуск тестов

Для запуска всех тестов выполните:
```bash
python -m unittest discover
```

---

## Контрибуции

Будем рады вашим предложениям и исправлениям. Пожалуйста, создавайте pull request с соответствующим описанием.

---

## Лицензия

Этот проект разрабатывается под лицензией MIT.