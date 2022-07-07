from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


# remove unnecessary characters and use only first and last name
def clean_name(i):
    c = i.text.replace('•', '').replace(',', '').strip().split(' ')
    if len(c) >= 3:
        c = c[0:2]

    return c


# selenium action chain to put text into an entered element. clears already present text. can choose whether to hit
# enter (defaults true)
def enter_text_in_field(text, elem, driver, enter=True):
    actions = ActionChains(driver)
    actions.double_click(elem)
    actions.send_keys_to_element(elem, text)
    if enter:
        actions.send_keys_to_element(elem, Keys.ENTER)
    actions.perform()
