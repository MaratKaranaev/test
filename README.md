# Проект хранения карт и ПИН конвертов по системе Smart-Box
Инструкция запуска
1) Клонировать репозиторий
2) Создать venv
3) установить зависимости pip install -r requirements.txt
4) запустить файл hel.py

# Работа с API приложения
Через Postman выполнить запросы к 9000 порту
   - POST 127.0.0.1:9000/smart_box_create (добавление смарт бокса нужной платежной системы)
     - JSON {
                "pay_system": "visa"
            }
   - POST 127.0.0.1:9000/smart_box_add (добавление карты в нужный смарт бокс)
     - JSON {
                "card_number": "41111111111113158",
                "card_embossed_text": "ALEX IVANOV",
                "smart_box": "visa"
            }
  - POST 127.0.0.1:9000/smart_box_extract (извлечение карты из смарт бокса)
    - JSON {
                "card_embossed_text": "ALEX IVANOV",
                "card_number": "41111111111113158",
                "smart_box": "visa"
            }
  - POST 127.0.0.1:9000/smart_box_delete (удаление нужного смарт бокса)
    - JSON {
                "smart_box": "visa"
            }
  - POST 127.0.0.1:9000/find_card (поиск карты в смарт боксах)
    - JSON {
                "card_number": "41111111111113157"
            }
  - GET 127.0.0.1:9000/smart_box (получить содержимое смарт бокса)