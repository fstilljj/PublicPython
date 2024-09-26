for h in zapi.hostinterface.get(filter={"type": 2}): 
    int_id = h['interfaceid'] 
    details = {'version': '2', 'bulk': '1', 'community': 'guit', 'max_repetitions': '10'} 
    zapi.hostinterface.update(interfaceid=int_id, details=details)