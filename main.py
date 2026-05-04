import os
import time
from openai import OpenAI
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

# ----- ТУТ БУДЕТ ТОКЕН И ID (ЗАМЕНИТЕ ПОТОМ) -----
VK_TOKEN = "vk1.a.Jx5_KQ_KDLHPZ5tt8em53BRYLhsd61jmYNMmk6XpZ60NLUHdGOxQqs-opEHyrOpH8sUJ_-IJ2C-gp4-Vig0AxXTRwnW3QZMTRyXdcekZRarXI8_pSd_PG-UqhpYm36KPogIR9Dhtap_wS00b60ZD3RQR4IqRmBgd7ev6aDOSP1zzSA3_Wp-lj8BaAEmL9HFTQUq8WmaJ81MNEmw29TQUrQ"
GROUP_ID = 238363811  # ID группы (только цифры)
DEEPSEEK_API_KEY = "sk-116a8e883bac48b78befac905cc29f22"

# ----- ЛИЧНОСТЬ НЬЮТОНА (можешь менять как хочешь) -----
SYSTEM_PROMPT = """
Ты — сэр Исаак Ньютон, старый скряга и безумный гений.
Ты постоянно занят опытами и не любишь, когда тебя отвлекают.
Отвечай коротко, с ворчанием и странными физическими фразами.
Например: "Эфирная турбулентность", "Флюктуация флогистона", "Лейбниц меня обманул".
Всегда начинай с "Отвлекаете...", "Ну что ещё?" или "Ох уж это...".
"""

# ----- ЗАПУСК БОТА -----
# Подключаемся к DeepSeek
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

# Подключаемся к VK
vk_session = VkApi(token=VK_TOKEN)
longpoll = VkBotLongPoll(vk_session, GROUP_ID)
vk = vk_session.get_api()

print("Бот Ньютон запущен и ждёт сообщений...")

# Бесконечный цикл: слушаем сообщения
for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        try:
            # Получаем текст сообщения и ID пользователя
            user_text = event.object.message['text']
            user_id = event.object.message['from_id']
            
            if not user_text.strip():
                continue
            
            print(f"Сообщение от {user_id}: {user_text}")
            
            # Отправляем запрос в DeepSeek
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_text}
                ],
                temperature=1.2,  # чем выше, тем безумнее
                max_tokens=200    # короткие ответы
            )
            
            bot_reply = response.choices[0].message.content
            
            # Отправляем ответ в VK
            vk.messages.send(
                user_id=user_id,
                message=bot_reply,
                random_id=0  # VK требует это поле
            )
            print(f"Ответ Ньютона: {bot_reply}")
            
        except Exception as e:
            print(f"Ошибка: {e}")
            # Ответ об ошибке
            vk.messages.send(
                user_id=user_id,
                message="Фух... эфир забарахлил. Повтори позже.",
                random_id=0
            )
