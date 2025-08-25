import logging
import os

# Asegura que exista la carpeta de logs
os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# File handler
file_handler = logging.FileHandler("logs/app.log")
file_handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Agrega ambos handlers al logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
