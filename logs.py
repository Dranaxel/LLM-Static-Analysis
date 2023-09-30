from loguru import logger
import sys

logger.remove()
LOGLEVEL = os.environ.get("LOGLEVEL", "INFO").upper()
logger.add(sink=sys.stderr, level=LOGLEVEL)
