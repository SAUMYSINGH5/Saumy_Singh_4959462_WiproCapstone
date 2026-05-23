import time
import logging
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import allure

from utils.logger import LogGen

logger = LogGen.loggen(__name__)

CHECKOUT_TAG_NAMES = ("checkout",)


# ──────────────────────────────────────────────
# LOG CAPTURE HANDLER
# Captures log records during each scenario so
# they can be attached to the Allure report.
# ──────────────────────────────────────────────

class _ListHandler(logging.Handler):
    """In-memory log handler — collects records for Allure attachment."""
    def __init__(self):
        super().__init__()
        self.records = []

    def emit(self, record):
        self.records.append(self.format(record))

    def flush_text(self) -> str:
        text = "\n".join(self.records)
        self.records.clear()
        return text


# ──────────────────────────────────────────────
# LIFECYCLE HOOKS
# ──────────────────────────────────────────────

def before_all(context):
    logger.info("Starting test run")


def after_all(context):
    logger.info("Test run complete")


def before_scenario(context, scenario):
    logger.info(f"Running: {scenario.name}")

    context.skip_if_delivery_unavailable = any(
        kw in scenario.name.lower() for kw in CHECKOUT_TAG_NAMES
    )
    context.delivery_unavailable_detected = False

    # ── Attach in-memory log handler so we can dump logs to Allure ────
    context._log_handler = _ListHandler()
    context._log_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s",
                          datefmt="%Y-%m-%d %H:%M:%S")
    )
    logging.getLogger().addHandler(context._log_handler)

    # ── Launch browser ────────────────────────────────────────────────
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")

    service = Service(ChromeDriverManager().install())
    context.driver = webdriver.Chrome(service=service, options=chrome_options)
    context.driver.implicitly_wait(10)
    context.wait = WebDriverWait(context.driver, 30)

    logger.info("Browser open")


def after_step(context, step):
    """
    After every step:
    - Attach a screenshot to Allure (always).
    - On step failure, mark screenshot with red label.
    """
    try:
        screenshot = context.driver.get_screenshot_as_png()
        status_label = "PASSED" if step.status == "passed" else "FAILED"
        allure.attach(
            screenshot,
            name=f"{status_label} — {step.name}",
            attachment_type=allure.attachment_type.PNG
        )
    except Exception as e:
        logger.warning(f"Could not attach step screenshot to Allure: {e}")


def after_scenario(context, scenario):
    from datetime import datetime

    # ── 1. Attach full scenario log to Allure ─────────────────────────
    try:
        log_text = context._log_handler.flush_text()
        if log_text:
            allure.attach(
                log_text,
                name="Scenario Log",
                attachment_type=allure.attachment_type.TEXT
            )
        logging.getLogger().removeHandler(context._log_handler)
    except Exception as e:
        logger.warning(f"Could not attach logs to Allure: {e}")

    # ── 2. Save final screenshot to reports/screenshots folder ────────
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name  = scenario.name.replace(" ", "_").replace("/", "-")
    status     = "PASSED" if scenario.status == "passed" else "FAILED"
    screenshot_dir = os.path.join("reports", "screenshots")
    os.makedirs(screenshot_dir, exist_ok=True)
    screenshot_path = os.path.join(
        screenshot_dir, f"{status}_{safe_name}_{timestamp}.png"
    )

    try:
        context.driver.save_screenshot(screenshot_path)
        logger.info(f"Screenshot saved at: {screenshot_path}")

        # Also attach the final screenshot to Allure
        with open(screenshot_path, "rb") as f:
            allure.attach(
                f.read(),
                name=f"Final Screenshot — {status}",
                attachment_type=allure.attachment_type.PNG
            )
    except Exception as e:
        logger.warning(f"Could not save/attach final screenshot: {e}")

    # ── 3. Log pass/fail status ───────────────────────────────────────
    if scenario.status == "failed" and context.delivery_unavailable_detected:
        logger.warning(
            f"SKIP-REASON for '{scenario.name}': geo restriction, not a code defect."
        )
    elif scenario.status == "failed":
        logger.error(f"Failed: {scenario.name}")
    else:
        logger.info(f"Passed: {scenario.name}")

    # ── 4. Quit browser ───────────────────────────────────────────────
    try:
        context.driver.quit()
    except Exception:
        pass
    logger.info("Browser closed")
