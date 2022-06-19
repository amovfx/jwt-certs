import click
import python_jwt as jwt, jwcrypto.jwk as jwk, datetime
import jwt as jsonwt
import json
import os

def safe_open_w(path):
    ''' Open "path" for writing, creating any parent directories as needed.
    '''
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return open(path, 'w')


class AsymetricKeyGenerator():

    def __init__(self,size):
        key = jwk.JWK.generate(kty='RSA', size=int(size))
        self.priv_pem = key.export_to_pem(private_key=True, password=None)
        self.pub_pem = key.export_to_pem()

    def dump_pem(self):

        safe_open_w('./keys/priv.pem').write(self.priv_pem.decode())
        safe_open_w('./keys/pub.pem').write(self.pub_pem.decode())

    def dump_jwk(self):
        pub_key = jwk.JWK.from_pem(self.pub_pem)
        keys = {"keys": [pub_key.export(as_dict=True)]}
        pub_key = jwk.JWK.from_pem(self.pub_pem)
        safe_open_w('./jwk/api_secret.jwk').write(json.dumps(keys, indent=4))


@click.command()
@click.argument('size', default='2048')
def make_certs(size):
    Keys = AsymetricKeyGenerator(size)
    Keys.dump_pem()
    Keys.dump_jwk()
    


if __name__ == '__main__':
    make_certs()