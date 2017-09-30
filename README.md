# DNSPod script for LEDE DDNS custom scripts
Usage (on LEDE):
```sh
opkg install node
# cd to project root
cd /root/lede-ddns-dnspod
npm install
```

In luci-app-ddns:

update\_script: /root/lede-ddns-dnspod/update.sh

username: DNSPod token ID (e.g. 12345)

password: DNSPod token (e.g. 198900e19260817abcd1926081702d54)

And enjoy.
