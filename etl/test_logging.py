
from pathlib import Path
import logging

# Define project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = PROJECT_ROOT / "Reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = REPORTS_DIR / "etl_load.log"

# Configure logging for both file and terminal
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(),
    ],
    force=True,
)

logger = logging.getLogger("AURIXA")


def test_error_logging():
    """Verify that errors and tracebacks are recorded correctly."""
    try:
        # Generate an intentional test error
        raise ValueError("This is an intentional logging test error.")

    except ValueError:
        logger.exception("Expected test error captured successfully.")
        print("PASS: Test error was captured.")

    # Verify the log file exists
    if LOG_FILE.exists() and LOG_FILE.stat().st_size > 0:
        print(f"PASS: Log file created and contains data: {LOG_FILE}")
    else:
        print("FAIL: Log file was not created or is empty.")


if __name__ == "__main__":
    test_error_logging()
