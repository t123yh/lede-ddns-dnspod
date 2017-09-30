var domainNameParser = require("effective-domain-name-parser"),
    dnspodApi = require('dnspod-api'),
    _ = require('lodash');


var param = process.argv.slice(2);
var token = param[0] + ',' + param[1];
var dnspod =  new dnspodApi({
    server: 'dnspod.cn',
    token: token
});

var domainInfo = domainNameParser.parse(param[2]);
var subdomainName = domainInfo.subdomain || '@';
var domainName = domainInfo.sld + "." + domainInfo.tld;

function checkError(result) {
    if (result.status.code !== "1") {
        throw new Error(result.status.message);
    }
}

dnspod.do({
    action: 'Record.List',
    params: {
        domain: domainName,
        sub_domain: subdomainName
    }
}).then(function(recordListData) {
    // console.log(recordListData);
    checkError(recordListData);
    var record = _.head(_.filter(recordListData.records, function(x) { return x.type === "A"; }));
    if (record == null) {
        throw new Error("Domain not found or no matching A record!");
    }
    return dnspod.do({
        action: 'Record.Ddns',
        params: {
            domain: domainName,
            record_id: record.id,
            record_line_id: record.line_id,
        }
    });
}).then(function(result) {
    checkError(result);
    console.log(result.status.message);
    process.exit(0);
}).catch(function (err) {
    console.log(err.toString());
    process.exit(1);
});

