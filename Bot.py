import asyncio
import os
from telethon import TelegramClient, events
import vk_api
from vk_api.upload import VkUpload

# === НАСТРОЙКИ ===
# Telegram
TG_API_ID = '28069584'
TG_API_HASH = '976d680c16829f43bc34753c3cb47dbc'
TG_SESSION = 'tg_session'  # имя файла сессии
TG_CHANNEL = 'pitereventru'  # username или id канала (например, 'mychannel' или -1001234567890)

# VK
VK_TOKEN = 'vk1.a.Xh-NmFsQzbMlR77O9v-WlrrcARGpQ8hAf_NsHuqfJXH70gd6pHnudXeZZWNmtxJKjyPkfCmoofSU7cvmxdCNAqiX5oqfj_AQtS05XhKi8JWE3HsfUwhCEFCY3-iC_4h-VbZTwUB_61OY9efXx38UFER8hqsJ8YzmecLWeR7ZiJocgOdthglL1YnioLEbPrfVY_cwTUHWx6W2JIV-ow_0xQ'
VK_GROUP_ID = 147979499  # id группы (без минуса)

# === КОНЕЦ НАСТРОЕК ===

# Инициализация VK
vk_session = vk_api.VkApi(token=VK_TOKEN)
vk = vk_session.get_api()
upload = VkUpload(vk_session)

# Инициализация Telegram
client = TelegramClient(TG_SESSION, TG_API_ID, TG_API_HASH)

async def main():
    @client.on(events.NewMessage(chats=TG_CHANNEL))
    async def handler(event):
        message = event.message
        text = message.text or ''
        photos = []
        # Сохраняем фото, если есть
        if message.photo:
            file_path = await message.download_media()
            photos.append(file_path)
        # Публикуем в VK
        attachments = []
        for photo_path in photos:
            photo = upload.photo_wall(photo_path, group_id=VK_GROUP_ID)[0]
            attachments.append(f"photo{photo['owner_id']}_{photo['id']}")
            os.remove(photo_path)  # удаляем локальный файл
        vk.wall.post(owner_id=-VK_GROUP_ID, message=text, attachments=','.join(attachments))
        print('Опубликовано в VK:', text)

    await client.start()
    print('Бот запущен!')
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main()) 
