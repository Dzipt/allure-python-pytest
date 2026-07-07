# TestOps demo project

This folder contains a focused demo suite for a TestOps product presentation.
It is intentionally broad enough to look like a real project, while still being
readable and predictable during a live demo.

## What to show

- automated API, UI, and mobile tests in one launch;
- 250+ collected pytest cases across generated regression and curated examples;
- Allure labels: epic, feature, story, suite, owner, severity, tags, issue links;
- attachments: JSON request/response, text browser state, CSV metrics;
- result variety: passed, failed, broken, skipped manual case, and a controlled flaky demo;
- parameterized tests for catalog filters;
- environment and release labels from launch variables.

## Run locally

```bash
python -m pytest testops_demo --alluredir=allure-results --clean-alluredir -p no:cacheprovider
```

The first run intentionally contains failures. Use it to show failed, broken,
manual, and flaky-looking tests.

For a second run where the flaky demo test passes:

```bash
TESTOPS_DEMO_RUN=2 python -m pytest testops_demo --alluredir=allure-results --clean-alluredir -p no:cacheprovider
```

On Windows PowerShell:

```powershell
$env:TESTOPS_DEMO_RUN="2"
python -m pytest testops_demo --alluredir=allure-results --clean-alluredir -p no:cacheprovider
```

## GitHub Actions

Use the `TestOps Demo Suite` workflow. It follows the same project pattern:
checkout, Python setup, dependencies, `allurectl watch`, and an uploaded
`allure-results` artifact. The test step allows intentional red tests so the
workflow can still publish results to TestOps.

Optional launch metadata:

```powershell
$env:TESTOPS_DEMO_ENV="stage"
$env:TESTOPS_DEMO_RELEASE="2026.07-demo"
python -m pytest testops_demo --alluredir=allure-results --clean-alluredir -p no:cacheprovider
```
