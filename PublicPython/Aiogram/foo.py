import asyncio, time, netmiko, aioschedule, yadisk, aiofiles, openpyxl
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

class Form(StatesGroup):
	log, mains = State(), State()

async def main():
	bot = Bot(token='TOKEN')
	dp = Dispatcher(bot, storage=MemoryStorage())
	dp.middleware.setup(LoggingMiddleware())
	
	@dp.message_handler(commands=['start'])
	async def send_welcome(message: types.Message):
		await Form.log.set()
		await message.answer("Привет, введи пароль")
	
	@dp.message_handler(state=Form.log)
	async def logging(message: types.Message, state: FSMContext):
		if message['text'] == 'passwd':
			await Form.mains.set()
			await message.answer('Добро пожаловать')
		else:
			await Form.log.set()
			await message.answer('Неверный пароль')

	@dp.message_handler(state=Form.mains)
	async def mains(message: types.Message, state: FSMContext):
		cou, text, text2, sp = 0, '', '', []
		await cl.download("/MR.xlsx", "MR.xlsx")
		wr = openpyxl.load_workbook('MR.xlsx').active
		for i in wr.iter_rows(values_only=True):
			for k in i:
				try:
					if message['text'].lower() in k.lower() and i[2] not in sp:
						sp.append(i[2])
						if len(text) >= 3000:
							text2 += f'{i[0]}\n{i[1]}\n{i[2]}\n{i[3]}\n{i[5]}\n{i[6]}\n{i[7]}\n{i[8]}\n{i[9]}\n{i[10]}\n'
						else:
							text += f'{i[0]}\n{i[1]}\n{i[2]}\n{i[3]}\n{i[5]}\n{i[6]}\n{i[7]}\n{i[8]}\n{i[9]}\n{i[10]}\n'
						cou += 1
				except Exception as err:
					continue
		if text == '':
			text = 'Ничего не найдено'
		if cou == 1:
			if ping(text.split('\n')[3]):
				text += 'Ping удачный'
			else:
				text += 'Ping неудачный'
		await message.answer(text)
		if text2 != '':
			await message.answer(text2)


	while True:
		try:
			cl = yadisk.AsyncClient(token='TOKEN')
			await dp.start_polling()
		except Exception as e:
			print(e)
			time.sleep(5)

if __name__ == '__main__':
	asyncio.run(main())