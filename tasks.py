# Created 2024-04-12
# Author: Steve Mourad

from robocorp.tasks import task
from robocorp import browser,vault

from RPA.HTTP import HTTP
from RPA.Tables import Tables
from RPA.PDF import PDF

import shutil
from pathlib import Path
@task

# --- CREATE ORDER PROCESS ---
def order_robots_from_RobotSpareBin():
    """
    Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images.
    """

    browser.configure(browser_engine="firefox",slowmo=100,headless = True) # <= Turn headless to 'False' to see what the robot is doing
    open_robot_order_website(browser)
    orders_raw = get_orders()
    orders = get_all_orders_from_csv_file(orders_raw)
    process_orders(orders, browser)
    archive_pdfs_into_zip()

def open_robot_order_website(browser):

    browser.goto("https://robotsparebinindustries.com/#/robot-order")
    
def get_orders():

    http = HTTP()
    return http.download(url="https://robotsparebinindustries.com/orders.csv",overwrite=True)

def get_all_orders_from_csv_file(orders):

    library = Tables()
    orders = library.read_table_from_csv("orders.csv",columns=["Order number","Head","Body","Legs","Address"])
    return orders

def close_modal(browser):

    page = browser.page()
    page.wait_for_selector(".alert-buttons > button:nth-child(1)")
    page.click(selector=".alert-buttons > button:nth-child(1)")

def process_orders(orders, browser):

    for row in orders:
        order_number = row["Order number"]
        close_modal(browser)
        fill_the_form(row,browser)
        submit_order_process(order_number, browser)

def fill_the_form(row, browser):
    page = browser.page()
    # HEAD
    page.select_option("#head",row["Head"])
    # BODY
    page.click("#id-body-" + row["Body"])
    # LEGS
    legs_selector = "input.form-control[type='number']"
    page.fill(legs_selector,row["Legs"])
    # ADDRESS
    page.fill("#address",row["Address"])    

def preview_robot(browser):
    page = browser.page()
    page.click("#preview")

def press_order_button(page):
    order_selector = page.query_selector("#order")
    order_another_selector = page.query_selector("#order-another")

    try:
        if order_selector:
            page.click("#order")
            if(order_selector):
                press_order_button(page)
        elif order_another_selector:
            page.click("#order-another")
        else:
            print("Element does not exist.")
    except Exception as e:
        print(f"An error occurered: {e}")
        
def finish_order(browser):

    page = browser.page()
    order_selector = page.query_selector("#order")
    try:
        if order_selector:
            page.click("#order")
            if(order_selector):
                finish_order(browser)
    
    except Exception as e:
        print(f"An error occurered: {e}")

def go_to_next_order(browser):

    page = browser.page()
    order_another_selector = page.query_selector("#order-another")
    try:
        if order_another_selector:
            page.click("#order-another")
        else:
            print("Element does not exist.")
    except Exception as e:
        print(f"An error occurered: {e}")

def submit_order_process(order_number, browser):
    finish_order(browser)

    pdf = PDF()
    screenshot = screenshot_robot(order_number, browser)
    receipt = store_receipt_as_pdf(pdf, order_number,browser)
    add_screenshot_to_pdf(pdf, receipt, screenshot)
    
    go_to_next_order(browser)

# --- STORE THE ORDER RECEIPT AS PDF FILE ---
def store_receipt_as_pdf(pdf, order_number,browser):
    page = browser.page()
    receipt = page.locator("#parts").inner_html()
    filename = "receipt_order_" + order_number + ".pdf"
    pdf.html_to_pdf(receipt,"output/pdf/" + filename)
    return "output/pdf/" + filename

def screenshot_robot(order_number, browser):

    page = browser.page()
    preview = page.locator("#robot-preview-image")
    filename = "order_robot_"+order_number+".jpeg"
    path_and_filename = "output/screenshots/" + filename
    # Correct usage for capturing an element screenshot
    preview.screenshot(path=path_and_filename)
    return path_and_filename

def add_screenshot_to_pdf(pdf, receipt, screenshot):

    pdf.add_files_to_pdf(files = [receipt, screenshot], target_document = receipt)
    
# ---CREATE A ZIP FILE OF RECEIPT PDF FILES ---
def archive_pdfs_into_zip():

    pdfs_dir = Path("output/pdf/")
    output_dir = Path("output/archive/")
    output_dir.mkdir(parents=True,exist_ok=True)

    archive_path = shutil.make_archive(output_dir / "archived_pdfs","zip",root_dir = pdfs_dir)
    print(f"Archive created at: {archive_path}")