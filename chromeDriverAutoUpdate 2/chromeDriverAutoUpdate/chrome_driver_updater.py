import os
import sys
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def get_chrome_version():
    """Get the installed Chrome version."""
    if sys.platform == "darwin":  # macOS
        chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        version = os.popen(f'"{chrome_path}" --version').read().strip()
        return version.split()[-1]
    elif sys.platform == "win32":  # Windows
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Google\Chrome\BLBeacon")
        version, _ = winreg.QueryValueEx(key, "version")
        return version
    else:  # Linux
        version = os.popen('google-chrome --version').read().strip()
        return version.split()[-1]

def check_and_update_chromedriver():
    """Check Chrome version and update ChromeDriver if needed."""
    try:
        # Get installed Chrome version
        chrome_version = get_chrome_version()
        print(f"Installed Chrome version: {chrome_version}")

        # Get the major version number
        major_version = chrome_version.split('.')[0]

        # Check if ChromeDriver is already installed and up to date
        try:
            options = Options()
            options.add_argument('--headless')
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            driver_version = driver.capabilities['chrome']['chromedriverVersion'].split()[0]
            print(f"Current ChromeDriver version: {driver_version}")
            
            if major_version in driver_version:
                print("ChromeDriver is up to date. No update needed.")
                return False
            else:
                print("ChromeDriver needs to be updated.")
                return True
        except Exception as e:
            print(f"Error checking current ChromeDriver: {e}")
            return True

    except Exception as e:
        print(f"Error: {e}")
        return True

def main():
    """Main function to handle the update process."""
    print("Starting ChromeDriver update check...")
    
    if check_and_update_chromedriver():
        print("Updating ChromeDriver...")
        try:
            # This will automatically download and install the correct version
            service = Service(ChromeDriverManager().install())
            print("ChromeDriver updated successfully!")
        except Exception as e:
            print(f"Error updating ChromeDriver: {e}")
    else:
        print("ChromeDriver is already up to date.")

if __name__ == "__main__":
    main() 