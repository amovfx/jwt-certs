"""Class to create asymetric keys for jwt files.

This class dumps .pem files and .jwt files

    Typical usage:
        from security.generators import AsymetricKeyGenerator

        keys = AsymetricKeyGenerator(2048)
        keys.dump()
"""

import os
import json

from dotenv import dotenv_values
from jwcrypto import jwk

config = dotenv_values(".env")
dir_path = os.path.join(os.getcwd(),'keys')



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
        write_data(f'jwk/{config["JWT_FILE"]}',json.dumps(keys, indent=4))

    def dump(self):
        """
        Export both pem and .jwk.
        """

        self.dump_pem()
        self.dump_jwk()