import ipfshttpclient
import time
api = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')
start = time.time()
data_mahoa = open('10MB', 'rb').read()
cid = api.add_str(str(data_mahoa))
done = time.time()
elapsed = done - start
print(elapsed)	