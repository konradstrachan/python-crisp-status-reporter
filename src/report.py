import requests
import base64

# Simple python implementation of Crisp push status reporter described:
# https://help.crisp.chat/en/article/how-to-setup-the-crisp-status-reporter-library-1koqk09/

url_base = 'https://report.crisp.watch/v1/report/'

# Token is generated in 'Configure your Status Reporter' section of settings page
token = "xx-yy-zz"
authorization_header = "Basic " + base64.b64encode((":" + token).encode()).decode()

# The status reporting request is to be executed at a fixed interval, eg. every minute.
# Once you start reporting every minute, and you've set interval in your request body to 
# eg. 60 seconds, you need to commit to reporting at this interval. If you don't report 
# in time, Crisp Status will mark the node as DEAD.
interval = 30

def ReportReplicaStatus(replica_id, service, node cpu, ram):
    url = url_base + service + '/' + node + '/'
    body = {"replica_id" : replica_id, "interval" : interval, "load" : {"cpu" : cpu,"ram" : ram}}
    headers = {'Authorization': authorization_header}
    r = requests.post(url, headers=headers, json=body)
    return r.status_code == 200

# Node identifiers obtained when creating push nodes 
service = "xx-yy-zz"
node = "xx-yy-zz"

# Report service OK
ReportReplicaStatus("service_xyz", service, node, 0.0, 0.0)

# Report service under load (exact values need to match thresholds set in check)
ReportReplicaStatus("service_xyz", service, node, 9.9, 0.99)

# No way of explicitly marking service as dead
# Not sending an update within the expected interval results
# in Crisp marking the node as dead automatically