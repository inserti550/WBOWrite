from selenium.webdriver.common.by import By
import time
def SelectPencil(driver):
    driver.find_element(By.CSS_SELECTOR, "#toolID-Pencil").click()

def PencilStatus(driver):
    return driver.find_element(By.CSS_SELECTOR, "#toolID-Pencil .tool-name").text.strip()

def SetCursorSize(driver, size):
    driver.execute_script("Tools.setSize(" + str(size) + ")")
    
def SetColor(driver, hex):
    driver.execute_script("Tools.setColor('" + hex + "')")

def Write(driver, x, y, xx, yy,sleep):
    driver.execute_script("Tools.curTool.listeners.press(arguments[0], arguments[1], new Event('mousedown'))", x, y)
    time.sleep(sleep)
    driver.execute_script("Tools.curTool.listeners.release(arguments[0], arguments[1], new Event('mouseup'))", xx, yy)

def RGBToHex(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'