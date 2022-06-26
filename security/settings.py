from pydantic import BaseSettings, Field, SecretStr

class Settings(BaseSettings):
    pub_key_path: str = Field(..., env="PUBLIC_KEY_PATH")
    priv_key_path: str = Field(..., env="PRIVATE_KEY_PATH")
    jwk_path: str = Field(..., env="PUB_JWK_PATH")
    key_size: int = Field(..., env="KEY_SIZE")
    
    class Config:
        env_prefix = ""
        case_sensitive = False
        env_file = '.env'
        env_file_encoding = 'utf-8'
        
settings = Settings()