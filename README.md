# DNSPod script for LEDE DDNS custom scripts
Usage (on LEDE):
```sh
opkg install python3-pip
pip install requests tldextract
git clone https://github.com/t123yh/lede-ddns-dnspod /root/dnspod
```

In luci-app-ddns:

update\_script: /root/dnspod/update.sh

username: DNSPod token ID (e.g. 12345)

password: DNSPod token (e.g. 198900e19260817abcd1926081702d54)

And enjoy.
