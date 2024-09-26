with Connection('1.1.1.1', user='admin', port='8023', connect_kwargs={'password':'passwd'}) as conn:
    out = conn.run(f'/domain/{domain}/routing/show {context[0]}')