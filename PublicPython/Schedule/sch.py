def mainka():
	print('Hi')
schedule.every().day.at("18:00").do(mainka)
while True:
        schedule.run_pending()
        time.sleep(1)
