"""Class to create asymetric keys for jwt files.

This class dumps .pem files and .jwt files

    Typical usage:
        from security.generators import AsymetricKeyGenerator

        keys = AsymetricKeyGenerator(2048)
        keys.dump()
"""

import os
import json
import warnings

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


class AsymmetricKeyGenerator():
    """
    Class to generate RSA certs.
    """

    def __init__(self ,size: int) -> None:
        """
        Initialize Key henerator and generate private and public pem
        """
        if (size < 512): 
            warnings.warn(f"Size of {size} is too small, defaulting to 512")
        key = jwk.JWK.generate(kty='RSA', size=max(int(size),512))
        
        self._priv_pem = key.export_to_pem(private_key=True, password=None)
        self._pub_pem = key.export_to_pem()
        
        pub_key = jwk.JWK.from_pem(self._pub_pem)
        self._jwk = {"keys": [pub_key.export(as_dict=True)]}

    def dump_pem(self) -> None:
        """
        Write out private and public pems to relative location of this file.
        """

        write_data('priv.pem',self._priv_pem.decode())
        write_data('pub.pem',self._pub_pem.decode())

    def dump_jwk(self) -> None:
        """
        Export pub_key to .jwk.
        """
        
        file_name = os.path.join("jwk",config["JWT_FILE"])
        write_data(file_name,json.dumps(self._jwk, indent=4))

    def dump(self) -> None:
        """
        Export both pem and .jwk.
        """

        self.dump_pem()
        self.dump_jwk()
        
    def get_priv_key(self) -> bytes:
        """Return byte object of priv key

        Returns:
            bytes: private key
        """
        return self._priv_pem
    
    def get_pub_key(self) -> bytes:
        """Return byte object of pub key

        Returns:
            bytes: public key
        """
        return self._pub_pem
    
    def get_jwk(self) -> dict:
        """Return the jwk dcit.

        Returns:
            dict: full jwk dict
        """
        return self._jwk
        