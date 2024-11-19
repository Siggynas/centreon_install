from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from functools import partial
import os
import Variable as G
import time
import threading

def set_variables():
    for var_name, default_value in G.defaults.items():
        if var_name not in os.environ:
            os.environ[var_name] = default_value

def Click_Element_ID(driver,selector):
    wait = WebDriverWait(driver, 10)
    next_button = wait.until(EC.presence_of_element_located((By.ID,selector)))
    next_button = driver.find_element(By.ID, selector)
    next_button.click()


def Centreon_Step_Next(driver):
    wait = WebDriverWait(driver, 10)
    next_button = wait.until(EC.presence_of_element_located((By.ID,"next")))
    next_button = driver.find_element(By.ID, "next")
    next_button.click()

def Centreon_Step_Previous(driver):
    wait = WebDriverWait(driver, 10)
    next_button = wait.until(EC.presence_of_element_located((By.ID,"previous")))
    next_button = driver.find_element(By.ID, "previous")
    next_button.click()

def Centreon_Step_Refresh(driver):
    wait = WebDriverWait(driver, 10)
    next_button = wait.until(EC.presence_of_element_located((By.ID,"refresh")))
    next_button = driver.find_element(By.ID, "refresh")
    next_button.click()

def Centreon_Get_Step_Current(driver):
    wait = WebDriverWait(driver, 5)
    element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h3")))
    element = driver.find_element(By.CSS_SELECTOR, "h3")
    return element.text

def Print_H1(text):
    print("\n--------------------\n"+text+"\n--------------------\n")

def Get_element_text(driver,selector,timeout):
    try:
        wait = WebDriverWait(driver, timeout)
        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,selector)))
        element = driver.find_element(By.CSS_SELECTOR, selector)
        return element.text
    except:
        print("ERREUR CSS("+selector+") : Element Introuvable !")


def Get_element_OuterHTML(driver,selector,timeout):
    try:
        wait = WebDriverWait(driver, timeout)
        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,selector)))
        element = driver.find_element(By.CSS_SELECTOR, selector)
        return element.get_attribute("outerHTML")
    except:
        print("ERREUR CSS("+selector+") : Element Introuvable !")

def Get_element_input_value(driver,selector,timeout):
    try:
        wait = WebDriverWait(driver, timeout)
        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,selector)))
        element = driver.find_element(By.CSS_SELECTOR, selector)
        return element.get_attribute("value")
    except:
        print("ERREUR CSS("+selector+") : Element Introuvable !")


def Set_input_text(driver,selector,textWanted,timeout):
    try:
        wait = WebDriverWait(driver, timeout)
        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,selector)))
        element = driver.find_element(By.CSS_SELECTOR, selector)
        element.clear()
        element.send_keys(textWanted)
    except:
        print("ERREUR CSS("+selector+") : Element Introuvable !")

def Check_element_text(driver,selector,textWanted,description,timeout):
    try:
        wait = WebDriverWait(driver, timeout)
        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,selector)))
        element = driver.find_element(By.CSS_SELECTOR, selector)
        if (element.text == textWanted):
            return description+" : "+"OK"
        else:
            return description+" : "+"NOT OK"
    except:
        print("ERREUR "+description+" : Element Introuvable !")
        return "ERREUR"
    
def Check_element_exists(driver,selector,timeout):
    try:
        wait = WebDriverWait(driver, timeout)
        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,selector)))
        element = driver.find_element(By.CSS_SELECTOR, selector)
        return 1
    except:
        return 0

def check_element_visible(driver, selector, timeout):
    try:
        wait = WebDriverWait(driver, timeout)
        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))

        # Scroll into view using JavaScript
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        
        # Check visibility using JavaScript
        is_visible = driver.execute_script(
            "var elem = arguments[0];" +
            "var box = elem.getBoundingClientRect();" +
            "var cx = box.left + box.width / 2;" +
            "var cy = box.top + box.height / 2;" +
            "var e = document.elementFromPoint(cx, cy);" +
            "while (e) {" +
            "if (e === elem) return true;" +
            "e = e.parentElement;" +
            "}" +
            "return false;",
            element
        )
        
        return 1 if is_visible else 0
    except Exception as e:
        print(f"Error: {e}")
        return 0



def extract_table_data(html):
    data = []
    rows = html.split('<tr')[1:]  # Skip the header row

    for row in rows:
        cells = row.split('<td')[1:]  
        parsed_cells = []
        for cell in cells:
            if '<span' in cell:
                status = cell.split('<span')[1].split('>')[1].split('<')[0].strip()
                parsed_cells.append(status)
            else:
                text = ' '.join(cell.split('>')[1:]).split('<')[0].strip()
                parsed_cells.append(text)
        data.append(parsed_cells)

    return data

def display_diff(old_table, new_table):
    old_set = set(tuple(row) for row in old_table)
    new_set = set(tuple(row) for row in new_table)
    added_rows = new_set - old_set
    removed_rows = old_set - new_set

    #print("Added rows:")
    for row in added_rows:
        print(" | ".join(row))

    #print("\nRemoved rows:")
    #for row in removed_rows:
    #    print(" | ".join(row))


def display_status_table_live(driver,selector,timeout,stop_selector,validator_state):
    index = 0
    while (index < timeout and not(check_element_visible(driver,stop_selector,2))):
        table = extract_table_data(Get_element_OuterHTML(driver,selector,10))
        
        if (validator_state != ""):
            try:
                validate_table_data(table,validator_state)
            except ValueError as error:
                raise ValueError(error)


        if (index == 0):
            #print(table)
            display_diff([],table)
        else:
            display_diff(old_table,table)

        old_table = table
        print(".",end="",flush=True)
        index += 1
        time.sleep(1)


def validate_table_data(table_data,validator_state):
    for index, row in enumerate(table_data):
        # Assuming each row is a tuple and the second element is the status
        if (len(row) > 1 and row[1] == ""):
            t=0
        elif (len(row) > 1 and row[1] != validator_state):
            raise ValueError(f"Error at row {index + 1}: Expected '"+validator_state+"', found '"+row[1]+"'")
        elif len(row) <= 1:
            print("",end="")
            #raise ValueError(f"Error at row {index + 1}: Not enough columns")


def wait_simple(seconds):
    for index in range(seconds):
        print(".",end="",flush=True)
        time.sleep(1)

def wait(seconds, stop_event):
    for index in range(seconds):
        if stop_event.is_set():
            print("\nWait was stopped early!")
            break
        print(".", end="", flush=True)
        time.sleep(1)
    else:
        print("\nWait completed without interruption.")



def run_wait(seconds, arg):
    stop_event = threading.Event()
    condition_with_arg = partial(example_condition_with_arg, arg) 
    wait_thread = threading.Thread(target=wait, args=(seconds, stop_event))
    monitor_thread = threading.Thread(target=monitor_condition, args=(stop_event, condition_with_arg))
    
    wait_thread.start()
    monitor_thread.start()
    return wait_thread, monitor_thread, stop_event



def monitor_condition(stop_event, condition, timeout=60):
    start_time = time.time()
    while not condition() and (time.time() - start_time) < timeout:
        time.sleep(0.5)
    if condition():
        stop_event.set()
        print("\nCondition met. Stopping the wait.")
    else:
        print("\nTimeout reached without meeting condition.")


def example_condition_with_arg(arg):
    time.sleep(5)  # Simulate a condition check delay
    return arg == "OK"  # Example condition
