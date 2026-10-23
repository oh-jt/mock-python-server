import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


def log_event(logger: logging.Logger, event: str, **fields) -> None:
    """Log a structured event as key=value pairs. Never pass secrets or PII as fields."""
    pairs = " ".join(f"{k}={v}" for k, v in fields.items())
    logger.info("%s %s", event, pairs)
