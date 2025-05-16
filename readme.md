### Запуск taskiq
taskiq worker app.taskiq_broker.broker:broker -fsd --workers=1

### Генерация стабов для i18n
i18n -dir-ftl app/bot/locales/ru/LC_MESSAGES/ -stub app/bot/locales/stub.pyi