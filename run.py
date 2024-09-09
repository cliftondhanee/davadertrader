import time

import requests

LUNO_API_URL = "https://api.luno.com/api/1/ticker?pair=XBTZAR"
TELEGRAM_KEY = "bot524090948:AAEbfTvRyQeFHphouFF-JW_Mgnqwpek5s40"
TELEGRAM_URL = f"https://api.telegram.org/{TELEGRAM_KEY}/sendMessage"
PERCENTAGE_THRESHOLD = 1

def telegram_alert(chat_ids, msg):
    for chat_id in chat_ids:
        response = requests.post(
            url=TELEGRAM_URL,
            data={"chat_id": chat_id, "text": msg},
        ).json()
    return response


def get_bitcoin_price():
    response = requests.get(LUNO_API_URL)
    data = response.json()
    return float(data["last_trade"])


def calculate_percentage_change(old_value, new_value):
    if old_value == 0:
        return 0
    return ((old_value - new_value) / old_value) * 100


def predict_next_value(current_value, percentage_change):
    return current_value * (1 - percentage_change / 100)


def main():
    previous_value = None

    while True:
        current_value = get_bitcoin_price()

        if previous_value is not None:
            percentage_change = calculate_percentage_change(
                previous_value, current_value
            )

            if percentage_change >= PERCENTAGE_THRESHOLD:
                predicted_value = predict_next_value(current_value, percentage_change)
                msg = f"""
                {percentage_change}% price drop detected.

                Current Price: R{current_value}
                Predicted price: R{predicted_value}
                """
                telegram_alert([485240048], msg)

        previous_value = current_value
        time.sleep(5)


if __name__ == "__main__":
    main()
