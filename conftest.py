import os
import shutil
import subprocess
import pytest

# Path ke Allure CLI (pastikan ini sesuai dengan sistem kamu)
ALLURE_CLI_PATH = "C:\\allure-2.32.1\\bin\\allure.bat"


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    """Bersihkan folder Allure sebelum memulai tes"""
    results_dir = "reports/allure-results"

    if os.path.exists(results_dir):
        shutil.rmtree(results_dir)  # Hapus semua file lama
        os.makedirs(results_dir)  # Buat ulang folder kosong
        print("\n🧹 Cleared old Allure results before test run.")


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    """Generate laporan Allure setelah tes selesai"""
    results_dir = "reports/allure-results"
    report_dir = "reports/allure-report"

    if os.path.exists(results_dir) and os.listdir(results_dir):
        try:
            print(f"\n🚀 Running Allure from: {ALLURE_CLI_PATH}")
            subprocess.run(
                [ALLURE_CLI_PATH, "generate", results_dir, "-o", report_dir, "--clean"],
                shell=True,
                check=True,
            )
            print(f"\n✅ Allure report generated at: {report_dir}")
        except FileNotFoundError:
            print("\n❌ ERROR: Allure CLI not found. Please check your installation.")
        except PermissionError:
            print("\n❌ ERROR: Permission Denied! Run VS Code as Administrator.")
        except subprocess.CalledProcessError as e:
            print(f"\n❌ ERROR: Failed to generate Allure report. {e}")
    else:
        print("\n⚠️ No Allure results found, skipping report generation.")
