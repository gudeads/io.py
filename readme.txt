io.py
==========
- Switch output states on remote devices' input state changes, using HTTP/Json interface


Examples:
==========

Switch Port 1 on epc1202.localnet according to Input 1 on enc2302.localnet
  ./io.py --io enc2302.localnet:1:epc1202.localnet:1

Enable SSL
  ./io.py --io enc2302.localnet:1:epc1202.localnet:1 --ssl enc2302.localnet

Enable HTTP auth
  ./io.py --io enc2302.localnet:1:epc1202.localnet:1 --username enc2302.localnet:admin --password enc2302.localnet:topsecret



Extended Example, with multiple Input->Output entanglements, ssl and HTTP Auth:

  Input 1 switches Output 1
  Input 2 switches Output 2
  Input 3 switches Output 3 and 4

  ./io.py \
    --io enc2302.localnet:1:epc1202.localhost:1 \
    --io enc2302.localnet:2:epc1202.localhost:2 \
    --io enc2302.localnet:3:epc1202.localhost:3 \
    --io enc2302.localnet:3:epc1202.localhost:4 \
    --ssl enc2302.localnet \
    --ssl epc1202.localnet \
    --username enc2302.localnet:admin \
    --password enc2302.localnet:topsecret \
    --username epc1202.localnet:admin \
    --password enc2302.localnet:toppersecret
