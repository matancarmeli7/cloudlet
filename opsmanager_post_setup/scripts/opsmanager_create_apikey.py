import time
import json
import argparse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

def main():
    # Variables init
    parser = argparse.ArgumentParser(description='Initial config of opsmanager keys')
    parser.add_argument('--url', help='ops manager url', type=str, required=True)
    parser.add_argument('--chromedriverpath', help='path of chrome driver', default="/usr/local/bin/chromedriver", type=str, required=False)
    parser.add_argument('--user', help='ops manager username', type=str, required=True)
    parser.add_argument('--password', help='ops manager password', type=str, required=True)
    parser.add_argument('--orgname', help='organization name to create', type=str, default="cloudlet", required=False)
    parser.add_argument('--desc', help='api token description', type=str, default="cloudlet", required=False)
    parser.add_argument('--whitelistip', help='whitelist ip - which ips can use the apikey', type=str, default="10.130.0.0/23", required=False)
    args = parser.parse_args()

    OPSMANAGER_URL = args.url
    CHROMEDRIVER_PATH = args.chromedriverpath
    USERNAME = args.user
    PASSWORD = args.password
    ORG_NAME = args.orgname
    APIKEY_DESCRIPTION = args.desc
    WHITELIST_IP = args.whitelistip

    # Initial setup
    results_dict = {}
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=options)
    wait = WebDriverWait(driver,10)
    driver.get(OPSMANAGER_URL)

    # 1. Login page
    username_input = driver.find_element_by_xpath("//input[@placeholder='Username']")
    password_input = driver.find_element_by_xpath("//input[@placeholder='Password']")
    login_button = driver.find_element_by_xpath("//button[@name='login']")

    username_input.send_keys(USERNAME)
    password_input.send_keys(PASSWORD)
    login_button.click()
    
    wait.until(EC.title_is('Organizations'))

    # 2. Getting to account settings to create organization
    user_dropdown = driver.find_element_by_partial_link_text(USERNAME)
    user_dropdown.click()
    organizations_link = driver.find_element_by_link_text("Organizations")
    organizations_link.click()
    wait.until(EC.title_is('Organizations | MongoDB Cloud Services'))

    # 3. Create new organization
    new_org_button = driver.find_element_by_xpath("//a[@class='button button-is-primary button-is-right-aligned button-is-xs organizations-actions-button']")
    new_org_button.click()
    wait.until(EC.title_is('Create Organization | MongoDB Cloud Services'))

    organization_name_input = driver.find_element_by_xpath("//input[@placeholder='Organization Name']")
    organization_name_input.send_keys(ORG_NAME)
    next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@name='next']")))
    next_button.click()
    crate_org_button = driver.find_element_by_xpath("//button[@name='next']")
    crate_org_button.click()
    wait.until(EC.title_is('Projects | Cloud: MongoDB Cloud'))
    
    results_dict["orgId"] = driver.current_url.split('/')[-2]

    # 4. Create API key
    access_link = driver.find_element_by_xpath("//span[text()='Access']")
    access_link.click()
    wait.until(EC.title_is('Access Management | Cloud: MongoDB Cloud'))

    apikeys_link = driver.find_element_by_link_text("API Keys")
    apikeys_link.click()
    time.sleep(1)

    create_apikey_button = driver.find_element_by_link_text("Create API Key")
    create_apikey_button.click()
    wait.until(EC.title_is('Create API Key | Cloud: MongoDB Cloud'))

    apikey_desc = driver.find_element_by_xpath("//input[@placeholder='Short Description']")
    apikey_desc.send_keys(APIKEY_DESCRIPTION)

    roles_dropdown_closed = driver.find_element_by_xpath("//div[@class='button button-is-full button-is-fluid-height permissions-dropdown-content']")
    roles_dropdown_closed.click()

    org_owner_checkbox = driver.find_element_by_xpath("//input[@name='ORG_OWNER']")
    org_owner_checkbox.click()

    roles_dropdown_open = driver.find_element_by_xpath("//div[@class='button button-is-full button-is-fluid-height permissions-dropdown-content button button-is-full permissions-dropdown-content-is-open']")
    roles_dropdown_open.click()

    results_dict["api_publickey"] = driver.find_element_by_xpath("//div[@class='create-apiuser-public-key']").text.lower()

    next_button = driver.find_element_by_xpath("//button[text()='Next']")
    next_button.click()

    time.sleep(1)

    results_dict["api_privatekey"] = driver.find_element_by_xpath("//span[@class='copy-command-text']").text.lower()

    whitelist_button = driver.find_element_by_xpath("//button[text()='Add Whitelist Entry']")
    whitelist_button.click()
    time.sleep(0.2)

    whitelist_ip_input = driver.find_element_by_xpath("//input[@placeholder='Enter IP Address or CIDR Notation']")
    whitelist_ip_input.send_keys(WHITELIST_IP)
    save_button = driver.find_element_by_xpath("//button[text()='Save']")
    save_button.click()
    time.sleep(1)

    done_button = driver.find_element_by_xpath("//button[text()='Done']")
    done_button.click()

    # Summary
    print(json.dumps(results_dict))
    driver.close()

if __name__ == "__main__":
    main()
