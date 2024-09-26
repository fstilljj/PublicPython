```Python
  ADMIN_CHAT_ID = '-1002196208423'
  CHANNEL_ID = '-1002159246926'
  spis = []
  textik = f'''Чтобы выложить свой бит\\, необходимо оформить релиз по следующему шаблону\\:

ФОТО КВАДРАТ

\\(Название\\)

*Авторы*\\: 
*Жанр*\\: \\(не больше 2х\\)

*Цена*\\: 
*\\(Free for non\\-profit\\)* или пропуск
*Basic* \\- \\(цена или слово нет\\) 
*Premium* \\- \\(цена или слово нет\\)
*Unlimited* \\- \\(цена или слово нет\\) 
*Exclusive* \\- \\(цена \\/ офферс онли или слово нет\\)

*Контакт\\:* \\@ \\(тг\\)

\\(3\\-4 тэга через хэштеги\\) 
\\[Выделенное жирным должно присутствовать обязательно\\]
\\[Обязательно проверить соответствие критериям в противном случае бит не будет выставлен\\.\\]

*Чтобы вызвать подсказку по заполнению шаблона можно использовать комманду /help*'''

  bot = Bot(token=await ncmain())
  dp = Dispatcher(bot)

  @dp.message_handler(commands=['start'])
  async def send_welcome(message: types.Message):
    await message.answer(text=f'''Привет\\! Я бот для публикации битов канала \\@beat\\_it\\_am\\.
{textik}''', parse_mode='MarkdownV2')
  
  @dp.message_handler(commands=['help'])
  async def send_welcome(message: types.Message):
    await message.reply(textik, parse_mode='MarkdownV2')
  
  @dp.message_handler(chat_id=ADMIN_CHAT_ID) #Ответ админов
  async def reply_to_user(message: types.Message):
    if message.reply_to_message:
      original_message = message.reply_to_message
      user_chat_id = original_message.forward_from.id if original_message.forward_from else original_message.chat.id
      if message.text == 'Да':
        try:
          for i, k in enumerate(spis):
            if original_message.audio['file_unique_id'] == k: #Ответ на аудио
              await bot.forward_message(chat_id=CHANNEL_ID, from_chat_id=user_chat_id, message_id=original_message.message_id)
              spis.pop(i)
        except Exception:
          await bot.forward_message(chat_id=CHANNEL_ID, from_chat_id=ADMIN_CHAT_ID, message_id=original_message.message_id)
          await bot.send_message(chat_id=user_chat_id, text='Ваш бит(ы) были опубликованы.\n\n@beat_it_am')
      else:
        await bot.send_message(chat_id=user_chat_id, text=f'Возникли проблемы, ответ от Администратора:\n\n"{message.text}"')
 
  @dp.message_handler(content_types=['photo']) #Отлов фото
  async def photo(message: types.Message):
    if re.findall(r'Basic -', message.caption) and re.findall(r'Premium -', message.caption) \
    and re.findall(r'Unlimited -', message.caption) and re.findall(r'Exclusive', message.caption) \
    and re.findall(r'Контакт', message.caption) and re.findall(r'Жанр', message.caption):
      await bot.forward_message(chat_id=ADMIN_CHAT_ID, from_chat_id=message.chat.id, message_id=message.message_id)
      await message.reply("Ваш вопрос передан администраторам. Ожидайте ответа.")
    else:
      await message.reply(f'''Запрос отклонен, проверьте все ли поля правильно заполнены.
Для просмотра шаблона заполнения релиза воспользуйтесь командой /help''')

  @dp.message_handler(content_types=['audio']) #Отлов аудио
  async def audio(message: types.Message):
    spis.append(message.audio['file_unique_id'])
    await bot.forward_message(chat_id=ADMIN_CHAT_ID, from_chat_id=message.chat.id, message_id=message.message_id)
    await message.reply("Ваш вопрос передан администраторам. Ожидайте ответа.")

  @dp.message_handler() #Отлов текста
  async def forward_message_to_admin(message: types.Message):
    await bot.forward_message(chat_id=ADMIN_CHAT_ID, from_chat_id=message.chat.id, message_id=message.message_id)
    await message.reply("Ваш вопрос передан администраторам. Ожидайте ответа.")

  while True:
    try:
      await dp.start_polling()
    except Exception as e:
      print(e)
      time.sleep(5)
      continue

if __name__ == '__main__':
  import asyncio, time, re
  from aiogram import Bot, Dispatcher, types
  from nc import ncmain
  asyncio.run(main())

```
