ddnsresult=$(python main.py $username $password $domain $__IP)
write_log 7 "DNSPod message: $ddnsresult"
return $?
