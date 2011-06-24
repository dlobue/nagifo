from flask import Flask
from nagext import NagExt
from nagifo import port, cmdfile, verify_hash, config
from base64 import urlsafe_b64decode as b64dec
app = Flask(__name__)

if config.has_option('default', 'debug'):
    app.debug = config.getboolean('default', 'debug')


ngext = NagExt(cmdfile)

@app.route('/<data>')
def root(data):
    ddata = b64dec(str(data))
    sechash, user, host, desc = ddata.split('/')
    if verify_hash(sechash, user, host, desc):
        ngext.acknowledge_svc_problem(host, desc, 0, 1, 0, user,
                                  'acknowledgement sent from phone')
        return "acknowledged!"
    return "what are you trying to pull?"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)

