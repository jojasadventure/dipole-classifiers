# core/log_setup.py
import logging
import sys
from tqdm import tqdm

class TqdmLoggingHandler(logging.Handler):
    """Redirects logging messages to tqdm.write(), which prevents them from messing up progress bars."""
    def __init__(self, level=logging.NOTSET):
        super().__init__(level)

    def emit(self, record):
        try:
            msg = self.format(record)
            tqdm.write(msg, file=sys.stderr)
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            self.handleError(record)

def setup_logging():
    """Configures the root logger to be clean and tqdm-friendly."""
    log = logging.getLogger()
    if log.hasHandlers():
        log.handlers.clear()
    log.setLevel(logging.INFO)
    handler = TqdmLoggingHandler()    
    formatter = logging.Formatter("%(asctime)s - %(message)s", datefmt="%H:%M:%S")
    handler.setFormatter(formatter)
    log.addHandler(handler)