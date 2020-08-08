from aiohttp import web
import hashlib
import aiohttp_cors
import time
from aiohttp_route_middleware import UrlDispatcherEx
from eth.NetworkEth import *
from config.config import Org
import requests
from cryptographers.abe import *
import ipfshttpclient
api = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')

abe = init_abe()
(pk,mk) = create_pk_mk_abe(abe)

async def handle(request):

    data = await request.post()
    cid = data['cid']
    org_src = data['org_src']
    org_dest = data['org_dest']
    user_from = data['user_from']
    user_to = data['user_to']


async def push_metadata_to_eth(request):
    start = time.time()
    
    data = await request.post()
    data_mahoa = open('100MB', 'rb').read()

    org_src = "org1"
    org_dest = "org2"
    user_from = "user1"
    user_to = "user2"
  
    policy = '(CANHTUAN and DUY and MANH)'
   

    _encrypt_abe = encrypt_abe(abe,pk,data_mahoa,policy)

    cid = api.add_str(str(_encrypt_abe)) 
    # print(cid)
    
    post_to_eth = push_data_to_smartcontract(cid,org_src,org_dest,user_from,user_to)
    done = time.time()
    elapsed = done - start

    print(elapsed)

    response = {
        "status":200,
        "msg":"success"
    }

    return web.Response(text=json.dumps(response))

async def push_metadata_to_internal(request):
    start = time.time()

    data = await request.post()
   
    data_mahoa = open('100MB', 'rb').read()
   
    user_from = "canhtuan1"
    user_to = "canhtuan2"
    
    url = Org.URL_INTERNAL

    policy = '(CANHTUAN and DUY and MANH)'

    _encrypt_abe = encrypt_abe(abe,pk,data_mahoa,policy)

    cid = api.add_str(str(_encrypt_abe)) 
    myobj = {
        "user_from":user_from,
        "user_to":user_to,
        "cid":cid,
        "time":start
    }

    x = requests.post(url, data = myobj)

    response = {
        "status":200,
        "msg":str("aa")
    }

    return web.Response(text=json.dumps(response))
   

async def push_metadata_to_internalEcc(request):
    start = time.time()

    data = await request.post()
   
    data_mahoa = open('100MB', 'rb').read()
    user_from = "canhtuan1"
    user_to = "canhtuan2"
    url = Org.URL_INTERNAL
    policy = '(CANHTUAN and DUY and MANH)'

    _encrypt_abe = encrypt_abe(abe,pk,data_mahoa,policy)

    cid = api.add_str(str(_encrypt_abe)) 
    myobj = {
        "user_from":user_from,
        "user_to":user_to,
        "cid":cid,
        "time":start
    }

    x = requests.post(url, data = myobj)

    response = {
        "status":200,
        "msg":str("aa")
    }

    return web.Response(text=json.dumps(response))
   


async def queryInMetaData(request):
    data = await request.post()
    key = data['key']

    url_query_internal = Org.QUERY_INTERNAL + key
    print(url_query_internal)
    x = requests.get(url_query_internal)

async def queryExMetaData(request):
    data = await request.post()

    key = data['key']

    url_query_internal = Org.QUERY_EXTERNAL + key
    print(url_query_internal)
    x = requests.get(url_query_internal)

app = web.Application(router=UrlDispatcherEx(),client_max_size=1024**2*10)
cors = aiohttp_cors.setup(app)
cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
        allow_credentials=True,
        expose_headers="*",
        allow_headers="*",
    )
})


app.router.add_post('/handle',handle)

app.router.add_post('/push_metadata_to_eth',push_metadata_to_eth)
app.router.add_post('/push_metadata_to_internal',push_metadata_to_internal)
app.router.add_post('/push_metadata_to_internal_ecc',push_metadata_to_internalEcc)
app.router.add_post('/query_internal_metadata',queryInMetaData)
app.router.add_post('/query_external_metadata',queryExMetaData)
for route in list(app.router.routes()):
    cors.add(route)

web.run_app(app, port=9000)

