import os
import subprocess
from pyrogram import Client, filters
from pyrogram.types import Message

# Встроенные данные
API_ID = 35774222
API_HASH = "5ed53a8e81280a36a571023ebaf63261"

# Инициализация юзербота
app = Client("my_shakal_userbot", api_id=API_ID, api_hash=API_HASH)


@app.on_message(filters.command("lq", prefixes="") & filters.me)
async def shakal_media(client: Client, message: Message):
  # Проверяем, является ли сообщение ответом на другое сообщение
  if not message.reply_to_message:
    await message.edit("Батч, отправь команду `/lq` реплаем на фото или видео!")
    return

  reply = message.reply_to_message

  # Проверяем, есть ли в сообщении фото или видео
  if not reply.photo and not reply.video:
    await message.edit("Дод, это не фото и не видеоность!")
    return

  await message.edit("Шакалю качествоность...")

  # Скачиваем медиафайл
  file_path = await client.download_media(reply)
  output_path = "shakalized_" + os.path.basename(file_path)

  try:
    if reply.photo:
      # Обработка фото через ffmpeg (сильное сжатие JPEG)
      cmd = [
          "ffmpeg",
          "-i",
          file_path,
          "-q:v",
          "35",
          output_path,
      ]
      subprocess.run(cmd, check=True)

      # Отправляем сжатое фото ответом на исходное
      await client.send_photo(
          chat_id=message.chat.id,
          photo=output_path,
          reply_to_message_id=reply.id,
      )

    elif reply.video:
      # Обработка видео через ffmpeg (снижение битрейта и разрешение 240p)
      cmd = [
          "ffmpeg",
          "-i",
          file_path,
          "-vf",
          "scale=-2:240",
          "-b:v",
          "100k",
          "-preset",
          "ultrafast",
          output_path,
      ]
      subprocess.run(cmd, check=True)

      # Отправляем сжатое видео ответом на исходное
      await client.send_video(
          chat_id=message.chat.id,
          video=output_path,
          reply_to_message_id=reply.id,
      )

    # Удаляем сообщение с командой
    await message.delete()

  except Exception as e:
    await message.edit(f"Ошибканость при шакалении: {e}")

  finally:
    # Очищаем временные файлы
    if os.path.exists(file_path):
      os.remove(file_path)
    if os.path.exists(output_path):
      os.remove(output_path)


# Запуск юзербота
if __name__ == "__main__":
  print("Юзербот запущенность!")
  app.run()