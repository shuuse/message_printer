import os
import requests
import logging
from typing import Optional, List, Dict
from datetime import datetime
from dotenv import load_dotenv
from PIL import ImageDraw, ImageFont, Image
from brother_ql.raster import BrotherQLRaster
from brother_ql.backends.helpers import send
from brother_ql.conversion import convert
import time
import sys
from config import Config


# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MessageMonitor:
    def __init__(self):
        """Initialize the message monitor with API credentials and base URL."""
        self.base_url = Config.get_base_url()
        self.headers = {
            **Config.get_headers(),
            "X-API-Key": os.getenv("API_KEY")
        }


    def get_unread_messages(self) -> Optional[List[Dict]]:
        """
        Fetch unread messages from the API.
        Returns None if the request fails, otherwise returns a list of message dictionaries.
        """
        try:
            response = requests.get(
                f"{self.base_url}/messages/unread",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching unread messages: {str(e)}")
            return None
    

    def print_message(self, message: Dict) -> bool:
        """
        Print a message to the label printer.
        Returns True if successful, False otherwise.
        """
        try:
            sender = message['sender']
            text_message = message['message']
            return self.print_label(sender, text_message)
        except Exception as e:
            logger.error(f"Error processing message for printing: {str(e)}")
            return False


    def print_label(self, sender: str, message: str) -> bool:
        try:
            # Load the heading image
            image = Image.open(self.heading_image_path)

            # Resize the image if necessary
            max_width = 696
            if image.width > max_width:
                ratio = max_width / float(image.width)
                new_height = int(image.height * ratio)
                image = image.resize((max_width, new_height))
                logger.info(f"Heading image resized to: {image.size}")

            # Font configuration
            font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            font_size = 24
            font = ImageFont.truetype(font_path, font_size)

            # Wrap the message text
            def wrap_text(draw, text, font, max_width):
                lines = []
                words = text.split(' ')
                current_line = words[0]
                for word in words[1:]:
                    text_width = draw.textbbox((0, 0), current_line + ' ' + word, font=font)[2]
                    if text_width <= max_width:
                        current_line += ' ' + word
                    else:
                        lines.append(current_line)
                        current_line = word
                lines.append(current_line)
                return lines

            draw = ImageDraw.Draw(image)
            wrapped_message = wrap_text(draw, message, font, max_width - 20)

            # Calculate dynamic additional space based on message length
            base_space = 300  # Base space of 5 cm (~300 pixels)
            additional_space = (len(message) // 50) * 60  # Add 1 cm (~60 pixels) per 50 characters
            canvas_height = image.height + base_space + additional_space

            # Create a new canvas
            canvas = Image.new("RGB", (max_width, canvas_height), "white")
            draw = ImageDraw.Draw(canvas)

            # Paste the heading image
            canvas.paste(image, (0, 0))

            # Add the sender text
            text_y = image.height + 10
            draw.text((10, text_y), f"From: {sender}", font=font, fill="black")

            # Add the wrapped message
            text_y += 40  # Space below the sender text
            for line in wrapped_message:
                draw.text((10, text_y), line, font=font, fill="black")
                text_y += draw.textbbox((0, 0), line, font=font)[3]

            # Convert the canvas to printer instructions
            qlr = BrotherQLRaster(self.model)
            instructions = convert(
                qlr=qlr,
                images=[canvas],
                label='62',
                rotate='0',
                threshold=70.0,
                dither=False,
                compress=False,
                red=False,
                dpi_600=False,
                hq=True,
                cut=True
            )

            # Send the instructions to the printer
            send(instructions, self.printer_identifier)
            logger.info("Label printed successfully")


            # Reset or clear printer buffer if necessary
            time.sleep(1)  # Small delay to allow the printer to process
            logger.info("Printer buffer cleared after printing")
            return True

        except Exception as e:
            logger.error(f"Error printing label: {str(e)}")
            return False

    def mark_message_as_read(self, message_id: str) -> bool:
        """
        Mark a specific message as read.
        Returns True if successful, False otherwise.
        """
        try:
            response = requests.put(
                f"{self.base_url}/messages/{message_id}/read",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            logger.info(f"Message {message_id} marked as read.")
            return True
        except requests.RequestException as e:
            logger.error(f"Error marking message {message_id} as read: {str(e)}")
            return False

    def process_messages(self):
        """Main function to process unread messages."""
        try:
            messages = self.get_unread_messages()
            
            if messages is None:
                logger.error("Failed to fetch messages")
                return
                
            if not messages:
                logger.info("No unread messages found")
                return
                
            logger.info(f"Found {len(messages)} unread messages")
            
            for message in messages:
                # Only mark as read if printing was successful
                if self.print_message(message):
                    if self.mark_message_as_read(message['id']):
                        logger.info(f"Successfully processed message {message['id']}")
                    else:
                        logger.error(f"Failed to mark message {message['id']} as read")
                else:
                    logger.error(f"Failed to print message {message['id']}")

        except Exception as e:
            logger.error(f"Unexpected error in message processing: {str(e)}")

def main():
    # Initialize the message monitor
    monitor = MessageMonitor()
    
    try:
        while True:
            # Process messages periodically
            monitor.process_messages()
            time.sleep(60)  # Wait for 60 seconds before checking again
    except KeyboardInterrupt:
        logger.info("Shutting down message monitor...")
        sys.exit(0)

if __name__ == "__main__":
    main()