import ipfshttpclient
import time
api = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')
start_time = time.time()
plaintext_data = open('10MB', 'rb').read()
cid = api.add_str(str(plaintext_data))
complete_time = time.time()
elapsed = complete_time - start_time
print(elapsed)	