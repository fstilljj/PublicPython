```Python

async def main():
	ADMIN_CHAT_ID = 'bebr'

	bot = Bot(token='secret')
	dp = Dispatcher(bot)

	@dp.message_handler(commands=['start', 'help'])
	async def send_welcome(message: types.Message):
		await message.reply("Привет! Я бот техподдержки. Задайте ваш вопрос, и я передам его администраторам.")
	@dp.message_handler(chat_id=ADMIN_CHAT_ID)
	async def reply_to_user(message: types.Message):
		if message.reply_to_message:
			original_message = message.reply_to_message
			user_chat_id = original_message.forward_from.id if original_message.forward_from else original_message.chat.id
			await bot.send_message(chat_id=user_chat_id, text=message.text)
	@dp.message_handler()
	async def forward_message_to_admin(message: types.Message):
		print(111)
		#await bot.send_chat_action(message.chat.id, ChatActions.TYPING)
		forwarded_message = await bot.forward_message(chat_id=ADMIN_CHAT_ID, from_chat_id=message.chat.id, message_id=message.message_id)
		await message.reply("Ваш вопрос передан администраторам. Ожидайте ответа.")
	
			

	while True:
		try:
			await dp.start_polling()
		except Exception as e:
			print(e)
			time.sleep(5)
if __name__ == '__main__':
	import asyncio, time
	from aiogram import Bot, Dispatcher, types
	asyncio.run(main())
```