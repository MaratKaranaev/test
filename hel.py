from flask import Flask, request, jsonify

app = Flask(__name__)
app.smartBoxes = {}

app.payment_systems = ['visa', 'master', 'world']


def is_valid_card(card_number):
    return True


@app.route('/smart_box_create', methods=['POST'])
def smart_box_create():
    pay_system = request.json.get("pay_system")

    if pay_system in app.smartBoxes:
        return jsonify({"error": "Уже существует смарт бокс для данной платежной системы"})

    existing_smart_boxes = filter(lambda x: x == pay_system, app.smartBoxes.keys())
    if list(existing_smart_boxes):
        return jsonify({"error": "Уже существует смарт бокс для данной платежной системы"})

    app.smartBoxes[pay_system] = []

    return jsonify({"status": "Смарт бокс успешно создан для платежной системы " + pay_system})


@app.route('/payment_systems', methods=['GET'])
def payment_systems():
    valid_payment_systems = list(filter(lambda x: x in app.payment_systems, app.smartBoxes.keys()))
    return jsonify({'payment_systems': valid_payment_systems})



@app.route('/smart_box', methods=['GET'])
def smart_box():
    non_empty_smart_boxes = {key: value for key, value in app.smartBoxes.items() if value}
    return jsonify({"smart_box": non_empty_smart_boxes})



@app.route('/smart_box_add', methods=['POST'])
def smart_box_add():
    card_number = request.json.get("card_number")
    card_embossed_text = request.json.get("card_embossed_text")
    smart_box = request.json.get("smart_box")

    if not is_valid_card(card_number):
        return jsonify({"error": "Неправильный номер карты"})

    if len(app.smartBoxes[smart_box]) >= 10:
        return jsonify({"error": "Достигнут лимит карт в смарт боксе"})

    if any(card['num'] == card_number for card in app.smartBoxes[smart_box]):
        return jsonify({"error": "Карта уже присутствует в смарт боксе"})

    card = {"num": card_number, "emboss": card_embossed_text}
    app.smartBoxes[smart_box].append(card)

    return jsonify({"status": "Карта успешно добавлена в смарт бокс"})



@app.route('/smart_box_extract', methods=['POST'])
def smart_box_extract():
    smart_box = request.json.get("smart_box")
    card_number = request.json.get("card_number")

    if smart_box not in app.smartBoxes:
        return jsonify({"error": "Смарт бокс не найден"})

    if not is_valid_card(card_number):
        return jsonify({"error": "Неверный номер карты"})

    cards = app.smartBoxes[smart_box]
    extracted_cards = list(filter(lambda x: x["num"] == card_number, cards))
    if len(extracted_cards) > 0:
        position = cards.index(extracted_cards[0])
        del app.smartBoxes[smart_box][position]

        if len(app.smartBoxes[smart_box]) == 9:
            return jsonify({"status": "Количество карт в смарт боксе не превышает 9"})

        return jsonify({
            "card": card_number,
            "box": smart_box,
            "position": position + 1,
        })
    else:
        return jsonify({"error": "Карта не найдена в смарт боксе"})



@app.route('/smart_box_delete', methods=['POST'])
def smart_box_delete():
    smart_box = request.json.get("smart_box")

    if smart_box not in app.smartBoxes:
        return jsonify({"error": "Ошибка: Смарт бокс не найден"})

    if len(app.smartBoxes[smart_box]) > 0:
        return jsonify({"error": "Ошибка: Нельзя удалить смарт бокс, в котором есть карты"})

    app.smartBoxes = dict(filter(lambda x: x[0] != smart_box, app.smartBoxes.items()))

    return jsonify({"status": "Смарт бокс успешно удален"})



@app.route('/find_card', methods=['POST'])
def find_card():
    card_number = request.json.get("card_number")
    matching_cards = [(box, position + 1) for box, cards in app.smartBoxes.items() for position, card in enumerate(cards) if card["num"] == card_number]
    matching_cards = list(filter(lambda x: x[1]["num"] == card_number, enumerate(app.smartBoxes)))
    if matching_cards:
        formatted_matches = "\n".join([f"Box: {box}, Position: {position}" for box, position in matching_cards])
        return jsonify({
            "card": card_number,
            "matches": formatted_matches
        })
    else:
        return jsonify({"status": "Карта не найдена"})


if __name__ == '__main__':
    app.run(debug=True, port=9000)
