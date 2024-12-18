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
    
    # Printer configuration
    PRINTER = {
        'ip': '192.168.1.204',
        'port': 9100,
        'model': 'QL-810W',
        'heading_image_path': 'heading.png'
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
    
    @classmethod
    def get_printer_ip(cls) -> str:
        """Get the printer IP address."""
        return cls.PRINTER['ip']
    
    @classmethod
    def get_printer_port(cls) -> int:
        """Get the printer port number."""
        return cls.PRINTER['port']
    
    @classmethod
    def get_printer_model(cls) -> str:
        """Get the printer model."""
        return cls.PRINTER['model']
    
    @classmethod
    def get_printer_identifier(cls) -> str:
        """Get the formatted printer identifier string."""
        return f'tcp://{cls.get_printer_ip()}:{cls.get_printer_port()}'
    
    @classmethod
    def get_heading_image_path(cls) -> str:
        """Get the path to the heading image."""
        return cls.PRINTER['heading_image_path']