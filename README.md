
# Label Printer App

This Python application processes unread messages from an API, prints them on a Brother QL-810W label printer, and marks the messages as read.

## Features
- Fetches unread messages from a specified API.
- Prints messages on a Brother QL-810W label printer.
- Dynamically adjusts label size based on message length.
- Marks messages as read to prevent duplicate processing.

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
- **Printer Settings**: Modify the `self.printer_ip` and `self.model` values in the `MessageMonitor` class for your specific printer setup.
- **API Base URL**: Update the `self.base_url` in the `MessageMonitor` class if your API endpoint changes.

## Notes
- Ensure the `heading.png` file is in the project directory.
- The application processes messages every 60 seconds by default.

## Contributing
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit and push your changes.
4. Submit a pull request.

## License
This project is licensed under the MIT License.