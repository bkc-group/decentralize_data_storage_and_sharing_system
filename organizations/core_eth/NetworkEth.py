from web3 import Web3


f = open("abi/abi.json", "r")
abi = f.read()



web3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/66092b83a4de4330b7cc5df887e3ae4b'))

# print(web3.toChecksumAddress("0x6b221f7f452203d190d56df8be5c967778522beb"))
contract = web3.eth.contract(address="0x113405659541Cf753597D29A9B595b79Cb7229B8",abi=abi)


address = "0xe4680B5B373b9353AF87De622a6E410E067a25c9"
private_key = "ef0be3ad9cf6ab09b1aaca99e1880546e4ca82e159a590291d0ec67e5929d0cf"

def push_data_to_smartcontract(cid,org_src,org_dest,user_from,user_to):
    
    nonce =  web3.eth.getTransactionCount(address)
    tx_dict = contract.functions.addMetadata(str(cid),str(org_src),str(org_dest),str(user_from),str(user_to)).buildTransaction({
        'from': address,
        'gas': 800000,
        'gasPrice': web3.toWei('200', 'gwei'),
        'nonce': nonce,
        'chainId': 3
    })
    signed_tx =  web3.eth.account.signTransaction(tx_dict, private_key)
    tx_hash =  web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    return (web3.toHex(tx_hash))


# cid = "1"
# org_src = "2"
# org_dest = "3"
# user_from = ""
# user_to = "4"
# push_data_to_smartcontract(cid,org_src,org_dest,user_from,user_to)

# var str = web3.toAscii("0x000000000000000000000000000000000000000000000000000000000000006000000000000000000000000000000000000000000000000000000000000000a000000000000000000000000000000000000000000000000000000000000000e0000000000000000000000000000000000000000000000000000000000000000963616e687475616e310000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000963616e687475616e320000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000963616e687475616e330000000000000000000000000000000000000000000000");
# console.log(str); 





