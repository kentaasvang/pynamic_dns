import logging
import settings
logger = logging.getLogger(__name__)
logging.basicConfig(filename=settings.LOG_FILE, encoding="utf-8", level=settings.LOG_LEVEL)

