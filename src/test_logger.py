from logger import get_logger


logger = get_logger("test")

logger.info("Logger test started")
logger.warning("This is a warning test")
logger.error("This is an error test")

print("Logging test completed.")