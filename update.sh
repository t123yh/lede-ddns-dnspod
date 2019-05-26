ddnsresult=$(python3 /root/dnspod/main.py $username $password $domain $__IP)
return_code=$?
write_log 7 "DNSPod message: $ddnsresult"
return $?

