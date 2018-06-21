ddnsresult=$(node /root/dnspod/index.js $username $password $domain $__IP)
write_log 7 "DNSPod message: $ddnsresult"
return $?
