async def start(var):
	if var == 1:
		await asyncio.sleep(5)
		print(f'Var == 1')
	else:
		await asyncio.sleep(2)
		print(f'Var == 2')

async def main():
	a = [1, 2]
	task = []
	for i in a:
		task.append(start(i))
	await asyncio.gather(*task)
if __name__ == '__main__':
	import asyncio

	asyncio.run(main())