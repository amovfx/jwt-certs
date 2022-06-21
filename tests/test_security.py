"""Testing for the AsymetricKeyGenerator Object

"""


from security.generators import AsymmetricKeyGenerator, config
from pathlib import Path

        
        
class TestAsymetricKeyGenerator:
    """Test class for Asymetric
    """
    
    keys = AsymmetricKeyGenerator(512)
    keys.dump()
    
    def test_cert_dump(self):

        priv_path = Path.cwd() / "keys/priv.pem"
        pub_path = Path.cwd() / "keys/pub.pem"
        jwk_path = Path.cwd() / f'keys/jwk/{config["JWT_FILE"]}'
        assert priv_path.is_file()
        assert pub_path.is_file()
        assert jwk_path.is_file()
        

