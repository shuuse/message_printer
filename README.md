# Label Printer App
This Python application processes unread messages from an API, prints them on a Brother QL-810W label printer, and marks the messages as read.

## Features
- Fetches unread messages from a specified API
- Prints messages on a Brother QL-810W label printer
- Dynamically adjusts label size based on message length
- Marks messages as read to prevent duplicate processing
- Centralized configuration management

## Requirements
- Python 3.7+
- Brother QL-810W label printer
- Internet connection for API access

## Setup
1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd label_printer_app
   ```
2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up environment variables**:
   Create a `.env` file in the project root and add your API key:
   ```env
   API_KEY=your-api-key-here
   ```
5. **Run the application**:
   ```bash
   python fetch_and_print.py
   ```

## Configuration
The application uses a centralized configuration system in `config.py`. You can modify the following settings:

### Cloud Service Configuration
```python
CLOUD_SERVICE = {
    'base_url': 'https://message-api-0rws.onrender.com',
    'timeout': 10,  # Request timeout in seconds
    'headers': {
        'Content-Type': 'application/json'
    }
}
```

### Printer Configuration
```python
PRINTER = {
    'ip': '192.168.1.204',
    'port': 9100,
    'model': 'QL-810W',
    'heading_image_path': 'heading.png'
}
```

Update these values in `config.py` to match your environment and requirements.

## Notes
- Ensure the `heading.png` file is in the project directory
- The application processes messages every 60 seconds by default
- Configuration changes should be made in `config.py` rather than modifying the main application code

## Contributing
1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Commit and push your changes
4. Submit a pull request

## License
This project is licensed under the MIT License.
