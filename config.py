# config.py

class Config:
    """Application configuration."""
    
    # Cloud service configuration
    CLOUD_SERVICE = {
        'base_url': 'https://message-api-0rws.onrender.com',
        'timeout': 10,  # Request timeout in seconds
        'headers': {
            'Content-Type': 'application/json'
        }
    }
    
    @classmethod
    def get_base_url(cls) -> str:
        """Get the base URL for the cloud service."""
        return cls.CLOUD_SERVICE['base_url']
    
    @classmethod
    def get_timeout(cls) -> int:
        """Get the request timeout value."""
        return cls.CLOUD_SERVICE['timeout']
    
    @classmethod
    def get_headers(cls) -> dict:
        """Get the base headers (excluding API key)."""
        return cls.CLOUD_SERVICE['headers'].copy()