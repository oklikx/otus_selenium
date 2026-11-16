# otus_selenium

Для запуска тестов через докер нужно выполнить следующие действия:

1. установить нужные для докера зависимости(собрать образ): docker build -t tests .
2. тесты в хроме: docker run -it --network host tests
3. тесты в firefox: docker run -it --network host tests --browser firefox
4. в хроме можно по анлогии с пунктом 3, заменив firefox на chrome(просто chrome по умолчанию итак)

Для запуска с отчетами allure:

1. docker run -it --network host -v ${PWD}/allure-results:/app/allure-results tests --browser firefox --alluredir=/app/allure-results
2. docker run --rm -v ${PWD}:/app --entrypoint allure tests generate /app/allure-results --output /app/allure-report --clean
3. docker run --rm -v ${PWD}:/app -p 8081:8081 --entrypoint allure tests serve /app/allure-results -h 0.0.0.0 -p 8081

## Тесты для MySQL (PyMySQL)

Фреймворк для работы с БД PrestaShop через PyMySQL.

### Структура

- `src/conftest.py` — опции `--db-*` и фикстура `db_connection`.
- `src/lib/db.py` — CRUD-функции для `ps_customer`.
- `src/tests/test_customer_db.py` — 5 тестов (create/update/delete + негативные).

### Запуск

```bash
docker build -t prestashop-tests .
docker run --rm -it --network otus_selenium_prestashop_network prestashop-tests \
  tests/test_customer_db.py \
  --db-host=some-mysql --db-port=3306 --db-name=prestashop \
  --db-user=root --db-password=admin -v
```
