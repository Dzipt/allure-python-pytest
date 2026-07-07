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
