"""Testing for the AsymetricKeyGenerator Object

"""


from security.generators import AsymetricKeyGenerator
from pathlib import Path
        
        
class TestAsymetricKeyGenerator:
    
    keys = AsymetricKeyGenerator(512)
    keys.dump()
    
    def test_dump(self):

        priv_path = Path.cwd() / "keys/priv.pem"
        pub_path = Path.cwd() / "keys/pub.pem"
        assert priv_path.is_file()
        assert pub_path.is_file()
        

