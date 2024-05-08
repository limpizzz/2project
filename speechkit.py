from config import iam, folder_id
import requests
def speech_to_text(data):
    # указываем параметры запроса
    params = "&".join([
        "topic=general",
        f"folderId={folder_id}",
        "lang=ru-RU"
    ])
    url = f"https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?{params}"
    headers = {
        'Authorization': f'Bearer {iam}',
    }
    response = requests.post(url=url, headers=headers, data=data)
    decoded_data = response.json()
    if decoded_data.get("error_code") is None:
        return True, decoded_data.get("result")
    else:
        return False, "При запросе в SpeechKit возникла ошибка"