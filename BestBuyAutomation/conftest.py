import os
import subprocess
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from utils.logger import LogGen
from utils.screenshot_util import ScreenshotUtil

logger = LogGen.loggen(__name__)


@pytest.fixture(scope="function")
def driver():

    logger.info("Browser starting")

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")

    prefs = {
        "profile.default_content_setting_values.notifications": 2,
        "profile.default_content_settings.popups": 0
    }
    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.implicitly_wait(10)
    driver.get("https://www.bestbuy.com")

    logger.info("Browser ready")

    yield driver

    logger.info("Browser closing")
    print("\nClosing Browser...")
    driver.quit()


def pytest_sessionfinish(session, exitstatus):
    """Automatically generate Allure HTML report after test session ends."""
    allure_results_dir = "reports/allure-results"
    allure_report_dir  = "reports/allure-report"

    os.makedirs(allure_report_dir, exist_ok=True)

    try:
        result = subprocess.run(
            ["allure", "generate", allure_results_dir,
             "--output", allure_report_dir, "--clean"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"\n✅ Allure report generated: {allure_report_dir}/index.html")
        else:
            print(f"\n⚠️  Allure generate error: {result.stderr.strip()}")
    except FileNotFoundError:
        print("\n⚠️  'allure' command not found. "
              "Install Allure CLI and make sure it is on your PATH.")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report  = outcome.get_result()

    if report.when == "call":
        driver = item.funcargs.get("driver")
        if driver:
            if report.failed:
                logger.error(f"FAILED: {item.name}")
                ScreenshotUtil.capture_screenshot(driver, f"FAILED_{item.name}")
            elif report.passed:
                logger.info(f"PASSED: {item.name}")
                ScreenshotUtil.capture_screenshot(driver, f"PASSED_{item.name}")