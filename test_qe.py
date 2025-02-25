import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="module")
def browser():
    driver = webdriver.Chrome()

    file_path = os.path.relpath("QE-index.html", os.getcwd()) # Get relative path, assuming test file is in the same directory
    file_url = f"file:///{os.path.abspath(file_path)}" # Convert to absolute URL
    driver.get(file_url)
    
    yield driver
    driver.quit()

def test_1_login_form(browser):
    """Test 1: Validate login form presence and input functionality."""
    email_input = browser.find_element(By.ID, "inputEmail")
    password_input = browser.find_element(By.ID, "inputPassword")
    login_button = browser.find_element(By.XPATH, "//button[text()='Sign in']")

    assert email_input.is_displayed()
    assert password_input.is_displayed()
    assert login_button.is_displayed()

    email_input.send_keys("test@example.com")
    password_input.send_keys("password123")
    login_button.click()

def test_2_list_items(browser):
    """Test 2: Validate list items and badge values."""
    # Wait to ensure list items are loaded
    WebDriverWait(browser, 2).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#test-2-div .list-group-item"))
    )
    list_items = browser.find_elements(By.CSS_SELECTOR, "#test-2-div .list-group-item")
    assert len(list_items) == 3

    second_item = list_items[1]
    assert "List Item 2" in second_item.text
    badge = second_item.find_element(By.CLASS_NAME, "badge")
    assert badge.text == "6"

def test_3_dropdown(browser):
    """Test 3: Validate dropdown selection."""
    dropdown_button = browser.find_element(By.ID, "dropdownMenuButton")
    assert dropdown_button.text == "Option 1"

    dropdown_button.click() # Open the dropdown first

    option_3 = WebDriverWait(browser, 1).until(
        EC.element_to_be_clickable((By.XPATH, "//a[text()='Option 3']"))
    )
    option_3.click() # Select Option 3

    assert dropdown_button.text == "Option 3"

def test_4_buttons(browser):
    """Test 4: Validate button enable/disable states."""
    buttons = browser.find_elements(By.CSS_SELECTOR, "#test-4-div button")
    assert buttons[0].is_enabled()
    assert not buttons[1].is_enabled()

def test_5_dynamic_button(browser):
    """Test 5: Wait for button, click it, check success message."""
    button = WebDriverWait(browser, 12).until(
        EC.visibility_of_element_located((By.ID, "test5-button"))
    )

    assert button.is_displayed()
    button.click()

    alert = browser.find_element(By.ID, "test5-alert")
    assert alert.is_displayed()
    assert not button.is_enabled()
    
def test_6_table_lookup(browser):
    """Test 6: Find table cell at (2,2) and assert value."""
    def get_cell_value(row, col):
        return browser.find_element(By.XPATH, f"//table/tbody/tr[{row+1}]/td[{col+1}]").text

    assert get_cell_value(2, 2) == "Ventosanzap"
