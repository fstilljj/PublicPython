

# Функция для первого бота
def bot_one():
    exec(open('1.py').read())
# Функция для второго бота
def bot_two():
    exec(open('2.py').read())

if __name__ == '__main__':
	import threading
	import asyncio
	from aiogram import Bot, Dispatcher, types
	from aiogram.contrib.middlewares.logging import LoggingMiddleware
	from aiogram.types import ParseMode
	from aiogram.utils import executor
	# Создание потоков
	thread1 = threading.Thread(target=bot_one)
	thread2 = threading.Thread(target=bot_two)

	# Запуск потоков
	thread1.start()
	thread2.start()

	# Ожидание завершения всех потоков
	thread1.join()
	thread2.join()

	print("Все боты завершили работу")