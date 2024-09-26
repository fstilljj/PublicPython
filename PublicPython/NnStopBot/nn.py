if name=='main':
	while True:   
		try:        
			bot.polling(non_stop=True, interval=0)    
		except Exception as e:        
			print(e)        
			time.sleep(5)        
			continue