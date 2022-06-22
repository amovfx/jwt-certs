"""Testing for the AsymetricKeyGenerator Object

"""
from pathlib import Path
import json
import pytest
import jwt



from security.generators import AsymmetricKeyGenerator, config     
        
class TestAsymetricKeyGenerator:
    """Test class for Asymetric
    """
    
    keys = AsymmetricKeyGenerator(512)
    
    keys.dump()
    keys_bad = AsymmetricKeyGenerator(512)
    payload = {"Test": "Token"}
    token = jwt.encode(payload=payload, key=keys.get_priv_key(), algorithm="RS256")
    
    def test_cert_dump(self):
        """Test dumping pems and jwk data to disk.
        """

        priv_path = Path.cwd() / "keys/priv.pem"
        pub_path = Path.cwd() / "keys/pub.pem"
        jwk_path = Path.cwd() / f'keys/jwk/{config["JWT_FILE"]}'
        assert priv_path.is_file()
        assert pub_path.is_file()
        assert jwk_path.is_file()
        
        
    def test_encode_decode(self): 
        """Tests encoding and decoding of data
        """
        assert jwt.decode(self.token,
                          self.keys.get_pub_key(),
                          algorithms=["RS256"]) == self.payload
        
    def test_bad_key(self):
        """Tests an inncorrect key
        """
        with pytest.raises(jwt.exceptions.InvalidSignatureError):
            jwt.decode(self.token, self.keys_bad.get_pub_key(), algorithms=["RS256"])
            
    def test_jwt_decode(self):
        """Tests decoding of jwt
        """
        jwk_key = self.keys.get_jwk()['keys'][0]
        pub_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk_key))
        assert jwt.decode(self.token,
                          pub_key,
                          algorithms=["RS256"]) == self.payload
        
        
        
        
        

