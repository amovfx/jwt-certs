"""Testing for the AsymetricKeyGenerator Object

"""


from security.generators import AsymmetricKeyGenerator, config
from pathlib import Path
import jwt
import pytest
        
        
class TestAsymetricKeyGenerator:
    """Test class for Asymetric
    """
    
    keys = AsymmetricKeyGenerator(512)
    
    keys.dump()
    keys_bad = AsymmetricKeyGenerator(512)
    payload = {"Test": "Token"}
    token = jwt.encode(payload=payload, key=keys.get_priv_key(), algorithm="RS256")
    
    def test_cert_dump(self):

        priv_path = Path.cwd() / "keys/priv.pem"
        pub_path = Path.cwd() / "keys/pub.pem"
        jwk_path = Path.cwd() / f'keys/jwk/{config["JWT_FILE"]}'
        assert priv_path.is_file()
        assert pub_path.is_file()
        assert jwk_path.is_file()
        
        
    def test_encode_decode(self): 
        token = jwt.encode(payload=self.payload, key=self.keys.get_priv_key(), algorithm="RS256")
        assert jwt.decode(token, self.keys.get_pub_key(), algorithms=["RS256"]) == self.payload
        
    def test_bad_key(self):
        with pytest.raises(jwt.exceptions.InvalidSignatureError):
            jwt.decode(self.token, self.keys_bad.get_pub_key(), algorithms=["RS256"])
        
        
        
        
        

