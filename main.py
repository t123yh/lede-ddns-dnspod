import requests
import ipaddress
import sys
import tldextract

APIID = sys.argv[1]
APIToken = sys.argv[2]
Domain = sys.argv[3]
IP = sys.argv[4]


def dnspod_request(name, user_param):
    param = {
        'login_token': '{0},{1}'.format(APIID, APIToken),
        'format': 'json',
        'lang': 'en',
        'error_on_empty': 'yes',
        **user_param
    }
    addr = "https://dnsapi.cn/{0}".format(name)
    r = requests.post(addr, data=param, headers={"User-Agent": "dnspod-py/1.0.0 (t123yh@outlook.com)"}, allow_redirects=False)
    if r.status_code == 200:
        json_result = r.json()
        if json_result["status"]["code"] == "1":
            return r.json()
        else:
            raise RuntimeError(json_result["status"]["message"])
    else:
        raise RuntimeError(r.text)

try:
    domainInfo = tldextract.TLDExtract(suffix_list_urls=None)(Domain)
    subdomainName = domainInfo.subdomain or "@"
    domainName = "{}.{}".format(domainInfo.domain, domainInfo.suffix)

    record_list = list(dnspod_request("Record.List", {'domain': domainName, 'sub_domain': subdomainName})["records"])
    
    if ipaddress.ip_address(IP).version == 4:
        rtype = "A"
    elif ipaddress.ip_address(IP).version == 6:
        rtype = "AAAA"
    else:
        raise Exception("Incorrect IP", IP)

    rl = [a for a in record_list if a["type"] == rtype and a["name"] == subdomainName]
    if len(rl) == 0:
        raise RuntimeError("No matching record")
    record = rl[0]
    update_result = dnspod_request("Record.Modify", {'domain': domainName,
                                                   'record_id': record["id"],
                                                   'sub_domain': subdomainName,
                                                   'record_type': record["type"],
                                                   'record_line_id': record["line_id"],
                                                   'value': IP})
    print("OK: " + update_result["status"]["message"])
    sys.exit(0)
except Exception as ex:
    print("Error: " + str(ex))
    sys.exit(1)
