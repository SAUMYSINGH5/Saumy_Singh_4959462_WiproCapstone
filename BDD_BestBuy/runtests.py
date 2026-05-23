import os
import shutil
from datetime import datetime
from utils.logger import LogGen

logger = LogGen.loggen()

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

logger.info("TEST STARTED")

# ── Clean Old Allure Results ──────────────────────────────────
if os.path.exists("reports/allure-results"):
    logger.info("Deleting old allure-results folder")
    shutil.rmtree("reports/allure-results")

# ── Clean Old Allure Report ───────────────────────────────────
if os.path.exists("reports/allure-report"):
    logger.info("Deleting old allure-report folder")
    shutil.rmtree("reports/allure-report")

# ── Run Behave Tests
logger.info("Running BDD Tests with Behave...")
exit_code = os.system(
    "behave features/deal_of_day.feature "
    "--format allure_behave.formatter:AllureFormatter "
    "--outfile reports/allure-results"
)

#  Generate Allure Report
logger.info("Generating Allure Report...")
os.system("allure generate reports/allure-results -o reports/allure-report --clean")

#  Open Allure Report
logger.info("Opening Allure Report in browser...")
os.system("allure open reports/allure-report")

logger.info("=" * 60)
logger.info("AUTOMATION EXECUTION COMPLETED")
logger.info("=" * 60)
