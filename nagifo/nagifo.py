from base64 import urlsafe_b64encode as b64enc
from hashlib import sha1
from  notifo import Notifo
import hmac
import socket
import fcntl
import struct
from os.path import exists

from ConfigParser import SafeConfigParser

if exists('/etc/nagifo.conf'):
    config = SafeConfigParser()
    config.read('/etc/nagifo.conf')

    external_url = config.get('default', 'external_url')
    cmdfile = config.get('default', 'nagios_cmdfile')
    secret_key = config.get('default', 'secret_key')
else:
    config = None



def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


def generate_hash(user, host, desc):
    myip = get_ip_address('eth0')
    return hmac.new(secret_key,
                    ''.join([user, host, desc, myip]), sha1).digest()


def verify_hash(sechash, user, host, desc):
    return sechash == generate_hash(user, host, desc)


def notifo_notify(user, key, ntype, host, state, service_desc, rest):
    title = '%s %s' % (ntype, host)
    msg = '%s - %s, %s' % (state, service_desc, rest)
    
    if config is not None:
        sechash = generate_hash(user, host, service_desc)
        ackurl = 'http://%s/%s' % (external_url, b64enc('/'.join([sechash, user, host,
                                                              service_desc])))
    else:
        ackurl = None
    
    nt = Notifo(user, key)
    nt.send_notification(msg=msg, label='nagios', title=title, uri=ackurl)

