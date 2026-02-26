"""
Logging module for Xynx-13
Tracks encryption/decryption operations without external dependencies
"""

import logging
import os
from datetime import datetime

LOG_FILE = "xynx13.log"

def get_logger(name="Xynx-13"):
    """
    Create and configure a logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Avoid adding multiple handlers if logger already configured
    if not logger.handlers:
        # File handler
        file_handler = logging.FileHandler(LOG_FILE)
        file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)
        
        # Console handler (optional - for debugging)
        console_handler = logging.StreamHandler()
        console_format = logging.Formatter('%(levelname)s: %(message)s')
        console_handler.setFormatter(console_format)
        logger.addHandler(console_handler)
    
    return logger

def log_operation(operation, status, details=""):
    """
    Quick function to log operations
    """
    logger = get_logger()
    if status == "success":
        logger.info(f"{operation} - {details}")
    elif status == "error":
        logger.error(f"{operation} failed - {details}")
    elif status == "warning":
        logger.warning(f"{operation} - {details}")
