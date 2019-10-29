#!/usr/bin/python3
import ncclient.manager

m = ncclient.manager.connect_ssh(host='10.51.65.190', port=830,
                                 username='lab',
                                 password='lab',
                                 hostkey_verify=False,
                                 timeout=120)
m.create_subscription()

while True:
    print('Waiting for next notification')

    # This will block until a notification is received because
    # we didn't pass a timeout or block=False
    n = m.take_notification()
    print(n.notification_xml)