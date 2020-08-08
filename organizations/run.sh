#!/bin/bash


# #!/bin/bash
# # My first script

echo "Hello TranCanhTuan!"

# expr 1 \+ 3

kill $(lsof -t -i:5001) &
sleep 5
kill $(lsof -t -i:8000) &
# # kill $(lsof -t -i:9000) &
# # ipfs daemon &
# sleep 5 &
# echo "canhtuan"
# # node `pwd`"/microservice/worker.js"	&
# # node `pwd`"/fabic/server_fabic.js" &
# # python3 `pwd`"/server.py" &
# # echo "Start Success | Fail"