"""Click app that generates RSA public and private pem files and public jwk file.

This app was made for generating certs for nginx. It can be easily extended nad customized.

    Typical shell usage example:
        main.py 2048
        main.py 4096

"""

import os
import json
import click

from jwcrypto import jwk

dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'keys')

def write_data(file_path, data):
    ''' Open "path" for writing, creating any parent directories as needed.
    '''
    file_output = os.path.join(dir_path, file_path)
    os.makedirs(os.path.dirname(file_output), exist_ok=True)
    open(file_output, 'w', encoding='utf8').write(data)


class AsymetricKeyGenerator():
    """
    Class to generate RSA certs.
    """

    def __init__(self,size):
        """
        Initialize Key henerator and generate private and public pem
        """

        key = jwk.JWK.generate(kty='RSA', size=int(size))
        self._priv_pem = key.export_to_pem(private_key=True, password=None)
        self._pub_pem = key.export_to_pem()

    def dump_pem(self):
        """
        Write out private and public pems to relative location of this file.
        """
        write_data('priv.pem',self._priv_pem.decode())
        write_data('pub.pem',self._pub_pem.decode())

    def dump_jwk(self):
        """
        Export pub_key to .jwk.
        """
        pub_key = jwk.JWK.from_pem(self._pub_pem)
        keys = {"keys": [pub_key.export(as_dict=True)]}
        write_data('jwk/api_secret.jwk',json.dumps(keys, indent=4))

    def dump(self):
        """
        Export both pem and .jwk.
        """
        self.dump_pem()
        self.dump_jwk()



@click.command()
@click.argument('size', default='2048')
def make_certs(size):
    """
    Main click command to make and generate certs.
    """
    keys = AsymetricKeyGenerator(size)
    keys.dump()

if __name__ == '__main__':
    # pylint: disable=no-value-for-parameter
    make_certs()
