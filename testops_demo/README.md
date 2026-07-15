# Демо-проект для TestOps

Папка содержит демонстрационный набор тестов для презентации TestOps.
Набор достаточно большой, чтобы быть похожим на настоящий проект, но при этом
остается предсказуемым для живого демо.

## Что показывать

- автоматизированные API, веб- и мобильные проверки в одном запуске;
- 250+ pytest-сценариев с реалистичными русскими названиями и описаниями;
- Allure-метки: epic, feature, story, suite, owner, severity, tags, issue links;
- уникальные pytest-функции для generated-кейсов, чтобы TestOps получал стабильные `fullName` и `testCaseId`;
- без фиктивных `allure.id`: демонстрационные идентификаторы передаются как `external_id`;
- вложения: JSON запросов и ответов, состояние браузера, CSV-метрики;
- разные результаты: passed, failed, broken, skipped ручной кейс и управляемый нестабильный сценарий;
- метки окружения и релиза из переменных запуска.

## Локальный запуск

```bash
python -m pytest testops_demo --alluredir=allure-results --clean-alluredir -p no:cacheprovider
```

Первый запуск намеренно содержит падения. Используйте его, чтобы показать
failed, broken, ручные и нестабильные проверки.

Для повторного запуска, где нестабильные сценарии становятся зелеными:

```bash
TESTOPS_DEMO_RUN=2 python -m pytest testops_demo --alluredir=allure-results --clean-alluredir -p no:cacheprovider
```

В Windows PowerShell:

```powershell
$env:TESTOPS_DEMO_RUN="2"
python -m pytest testops_demo --alluredir=allure-results --clean-alluredir -p no:cacheprovider
```

## GitHub Actions

Тест `test_catalog_search_response_time` имитирует нестабильность и независимо в каждом прогоне
падает с вероятностью 50%. Используйте его для демонстрации flaky-результатов и повторного запуска.

Используйте workflow `TestOps Demo Suite`. Он следует общему стилю проекта:
checkout, настройка Python, установка зависимостей, `allurectl watch` и загрузка
артефакта `allure-results`. Шаг тестов допускает намеренно красные сценарии,
чтобы результаты все равно публиковались в TestOps.

Дополнительные метаданные запуска:

```powershell
$env:TESTOPS_DEMO_ENV="stage"
$env:TESTOPS_DEMO_RELEASE="2026.07-demo"
python -m pytest testops_demo --alluredir=allure-results --clean-alluredir -p no:cacheprovider
```

## Переменные окружения в TestOps

Виджет «Переменные» в обзоре запуска заполняется файлом
`allure-results/environment.properties`. Workflow создает этот файл после pytest
внутри команды `allurectl watch`, поэтому TestOps получает его вместе с
результатами запуска.

В демо туда попадают:

| Переменная | Значение |
| --- | --- |
| Build_number | номер запуска GitHub Actions |
| Commit | SHA коммита |
| Python_version | фактическая версия Python на runner |
| Worker_OS | ОС и kernel runner |
| Environment | стенд запуска |
| Browser | браузер |
| Platform | платформа |
| Release | версия релиза |
| Run_type | тип запуска |
| Branch | ветка |

Маппинг в TestOps нужен отдельно: он связывает переменные из CI с окружениями
тестов, чтобы TestOps мог различать результаты по стенду, браузеру, платформе и
другим условиям запуска.

Рекомендуемый набор для демо:

| Переменная в TestOps | Маппинг в GitHub Actions |
| --- | --- |
| ENV | ENV |
| Browser | BROWSER |
| Platform | PLATFORM |
| Release | RELEASE |
| Run type | RUN_TYPE |
| Branch | BRANCH |

Настройка в TestOps:

1. Администратор инстанса создает переменные в разделе «Администрирование» -> «Окружения».
2. В проекте открыть «Настройки» -> «Окружение».
3. Для каждой переменной добавить маппинг на имя переменной окружения из GitHub Actions.
4. Запустить workflow «Демо-набор TestOps» и указать значения `ENV`, `BROWSER`,
   `PLATFORM`, `RELEASE`, `RUN_TYPE`.

Workflow передает эти значения в процесс `allurectl watch`, поэтому TestOps сможет
прикрепить их к результатам запуска после настройки маппинга.
