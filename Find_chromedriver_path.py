import requests
import zipfile
import os
import platform
import shutil
import subprocess
import re
 
def get_chrome_version():
    try:
        if platform.system() == "Windows":
            process = subprocess.Popen(
                r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version',
                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL,
                shell=True
            )
            output = process.communicate()[0].decode('utf-8', errors="ignore")
            version = re.search(r'version\s+REG_SZ\s+([^\s]+)', output).group(1)
            return version
        elif platform.system() == "Darwin":  # macOS
            process = subprocess.Popen(
                ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--version"],
                stdout=subprocess.PIPE
            )
            version = process.communicate()[0].decode("UTF-8").strip().replace("Google Chrome ", "")
            return version
        elif platform.system() == "Linux":
            process = subprocess.Popen(["google-chrome", "--version"], stdout=subprocess.PIPE)
            version = process.communicate()[0].decode("UTF-8").strip().replace("Google Chrome ", "")
            return version
    except Exception as e:
        print(f"❌ Error detecting Chrome version: {e}")
        return None
 
def get_driver_download_url(chrome_version):
    major_version = chrome_version.split('.')[0]
    response = requests.get("https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json")
    data = response.json()
    for version_info in data["versions"]:
        if version_info["version"].startswith(major_version + "."):
            matching_version = version_info["version"]
            for platform_info in version_info["downloads"]["chromedriver"]:
                system_platform = platform.system()
                arch = platform.machine()
                if system_platform == "Windows" and platform_info["platform"] == "win64":
                    return platform_info["url"], matching_version
                elif system_platform == "Linux" and platform_info["platform"] == "linux64":
                    return platform_info["url"], matching_version
                elif system_platform == "Darwin":
                    if arch == "x86_64" and platform_info["platform"] == "mac-x64":
                        return platform_info["url"], matching_version
                    elif arch == "arm64" and platform_info["platform"] == "mac-arm64":
                        return platform_info["url"], matching_version
    return None, None
 
def download_and_extract_driver(download_url, extract_path="chromedriver"):
    zip_path = "chromedriver.zip"
    print(f"\n🔽 Downloading ChromeDriver from:\n{download_url}")
    r = requests.get(download_url, stream=True)
    with open(zip_path, 'wb') as f:
        shutil.copyfileobj(r.raw, f)
 
    if os.path.exists(extract_path):
        shutil.rmtree(extract_path)
 
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
 
    os.remove(zip_path)
 
    print(f"✅ ChromeDriver extracted to: {os.path.abspath(extract_path)}")
 
    # Find chromedriver binary path recursively
    driver_binary = None
    for root, dirs, files in os.walk(extract_path):
        for file in files:
            if file == "chromedriver" or file == "chromedriver.exe":
                driver_binary = os.path.join(root, file)
                break
        if driver_binary:
            break
 
    if not driver_binary:
        print("⚠️ Could not find chromedriver binary in extracted files.")
        return None
 
    try:
        process = subprocess.Popen([driver_binary, "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, _ = process.communicate()
        driver_version = stdout.decode("utf-8").strip()
        print(f"🧩 ChromeDriver version: {driver_version}")
    except Exception as e:
        print(f"⚠️ Could not determine ChromeDriver binary version: {e}")
        driver_binary = None
 
    return driver_binary
 
def main():
    chrome_version = get_chrome_version()
    if not chrome_version:
        print("❌ Could not detect Chrome version.")
        return None
 
    print(f"\n🌐 Detected Chrome version: {chrome_version}")
    download_url, matched_driver_version = get_driver_download_url(chrome_version)
 
    if not download_url:
        print("❌ Could not find matching ChromeDriver download URL.")
        return None
 
    print(f"📦 Matching ChromeDriver version: {matched_driver_version}")
    driver_path = download_and_extract_driver(download_url)
 
    if driver_path:
        driver_path = os.path.abspath(driver_path)
        print(f"📁 ChromeDriver binary path: {driver_path}")
        # Save the driver path to a file
        with open("chromedriver_path.txt", "w") as f:
            f.write(driver_path)
        print(f"✅ Saved ChromeDriver path to chromedriver_path.txt")
        return driver_path
    return None
 
if __name__ == "__main__":
    main()
