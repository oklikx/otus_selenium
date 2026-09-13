# otus_selenium

Для запуска тестов через докер нужно выполнить следующие действия:

1. установить нужные для докера зависимости(собрать образ): docker build -t prestashop-tests .
2. тесты в хроме: docker run -it --network host tests
3. тесты в firefox: docker run -it --network host tests --browser firefox
4. в хроме можно по анлогии с пунктом 3, заменив firefox на chrome(просто chrome по умолчанию итак)

Для запуска с отчетами allure:

1. docker run -it --network host -v ${PWD}/allure-results:/app/allure-results tests --browser firefox --alluredir=/app/allure-results
2. docker run --rm -v ${PWD}:/app --entrypoint allure tests generate /app/allure-results --output /app/allure-report --clean
3. docker run --rm -v ${PWD}:/app -p 8081:8081 --entrypoint allure tests serve /app/allure-results -h 0.0.0.0 -p 8081

1. docker network create selenoid
2. docker build -t prestashop-tests .
3. проверить конфигурацию selenoid (config/browsers.json)
4. В папке ./ggr должен лежать файл quota.json
5. Поднять всё окружение - docker-compose up -d
6. Дождаться готовности prestashop (должно быть healthy) - docker ps --filter "name=prestashop"
7. Посмотреть результаты тестов - docker-compose logs tests
8. Если нужно запустить тесты повторно - docker-compose up tests
