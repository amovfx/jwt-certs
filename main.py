"""Click app that generates RSA public and private pem files and public jwk file.

This app was made for generating certs for nginx. It can be easily extended nad customized.

    Typical shell usage example:
        main.py 2048
        main.py 4096

"""


import click
from security.generators import AsymetricKeyGenerator

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
