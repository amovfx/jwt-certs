import click
import python_jwt as jwt, jwcrypto.jwk as jwk, datetime
import jwt as jsonwt
import json
import os

def write_data(path, data):
    ''' Open "path" for writing, creating any parent directories as needed.
    '''
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w').write(data)


class AsymetricKeyGenerator():

    def __init__(self,size):
        key = jwk.JWK.generate(kty='RSA', size=int(size))
        self.priv_pem = key.export_to_pem(private_key=True, password=None)
        self.pub_pem = key.export_to_pem()

    def dump_pem(self):
        write_data('./keys/priv.pem',self.priv_pem.decode())
        write_data('./keys/pub.pem',self.pub_pem.decode())

    def dump_jwk(self):
        pub_key = jwk.JWK.from_pem(self.pub_pem)
        keys = {"keys": [pub_key.export(as_dict=True)]}
        
        write_data('./jwk/api_secret.jwk',json.dumps(keys, indent=4))

    def dump(self):
        self.dump_pem()
        self.dump_jwk()



@click.command()
@click.argument('size', default='2048')
def make_certs(size):
    Keys = AsymetricKeyGenerator(size)
    Keys.dump()
    


if __name__ == '__main__':
    make_certs()