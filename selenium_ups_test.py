from selenium import webdriver
from selenium.webdriver.support.ui import Select
from ups_company_details import ups_username, ups_password, main_office, engineering_subcontractor
# from selenium.webdriver.common.keys import Keys
# import time

# driver = webdriver.Chrome('C:\\Users\\Admin\\Downloads\\chromedriver_win32\\chromedriver.exe')  # path to Chrome webdriver
driver = webdriver.Chrome()  # chromedriver in C:\Windows folder
driver.implicitly_wait(5)  # wait for page to load for 5 secs


def login_to_ups(username, userpass):
    print('\nFiring up UPS...')
    driver.get('https://www.ups.com/uis/create')  # goes to UPS site
    # time.sleep(5)
    print(username + ' is logging into UPS.')  # feeback that user is logging in
    textfield_username = driver.find_element_by_id('userIdInput')  # finds username field and assigns variable to it
    textfield_username.clear()  # clears username field in case there are any values
    textfield_username.send_keys(username)  # puts username into field
    textfield_email = driver.find_element_by_id('passwordInput')  # finds password field
    textfield_email.clear()  # clears password field
    textfield_email.send_keys(userpass)  # puts password into field
    submit_button = driver.find_element_by_id('loginButton')  # finds login button
    submit_button.click()  # clicks login button
    print(username + ' is logged into UPS!')  # feeback for login success


def shipment_origin():
    shipment_origin_input = input('Where is the shipment coming from: ')
    # shipment_origin_input = 'DWE'
    return shipment_origin_input


def select_shipping_destination():
    driver.implicitly_wait(5)  # wait for page to load
    shipping_select = Select(driver.find_element_by_id('select_shipTo'))  # finds the shipping dropdown by id
    # print([option.text for option in shipping_select.options])
    while True:  # allows looping back to input
        shipping_dest = input('\nEnter where this this shipment is going (Enter -list for list of destinations): ')
        if shipping_dest == '-list':
            for option in shipping_select.options:  # loops through values in dropdown (<option> tags)
                print(option.text)  # prints option values text
                continue
                if True:
                    break
        if shipping_dest.lower() not in [option.text.lower() for option in shipping_select.options]:  # loops through text in shipping_select options objects
            if shipping_dest != '-list':
                print('Your chosen destination does not exist in the address book. Please try again.')
                continue
        else:
            print('Filling in address fields...')
            section_title = 'Begin Shipment'  # notify that user is on beginning page
            formatted_title = '\n' + section_title.center(35, '*') + '\n'  # formatting to make heading stand out
            print(formatted_title)
            # contact_name = shipping_contact.values
            shipping_select.select_by_visible_text(shipping_dest)
            shipping_contact = driver.find_element_by_id('shipToContactNameValue')  # finds element with contact name
            contact_name = shipping_contact.get_attribute('value')  # gets value of contact name element
            print(f'\nShipment going to: {shipping_dest} ({contact_name})')  # grabs value from contact name element
            break
    while True:
        # first_reference_input = input('Enter the first reference for this shipment: ')
        textfield_first_shipment_reference = driver.find_element_by_id('reference_value1')
        textfield_first_shipment_reference.clear()
        if len(first_reference_input) > 35:
            print('Only 35 characters are allowed.')
            textfield_first_shipment_reference.clear()
            continue
        else:
            textfield_first_shipment_reference.send_keys(first_reference_input)
            break
    while True:
        # second_reference_input = input('Enter the second reference for this shipment: ')
        textfield_second_shipment_reference = driver.find_element_by_id('reference_value2')
        textfield_second_shipment_reference.clear()
        if len(second_reference_input) > 35:
            print('Only 35 characters are allowed.')
            textfield_second_shipment_reference.clear()
            continue
        else:
            textfield_second_shipment_reference.send_keys(second_reference_input)
            break


def shipment_package_weight():
    select_package_amount = Select(driver.find_element_by_id('packageCount'))
    # number_of_packages = input('Enter amount of packages in this shipment (Maximum is 20): ')
    select_package_amount.select_by_visible_text(number_of_packages)
    # total_shipment_weight = input('Enter the total weight of the packages: ')
    package_weight_field = driver.find_element_by_id('shipmentTotalWeight')
    package_weight_field.clear()
    package_weight_field.send_keys(total_shipment_weight)
    print(f'Amount of packages: {number_of_packages} ')
    print(f'Total weight of packages is: {total_shipment_weight}kg')


def shipment_notify():
    email_notify_check = driver.find_element_by_id('emailNotify')
    email_notify_check.click()
    delivery_confirmation_check = driver.find_element_by_id('shipDeliveryConf')
    delivery_confirmation_check.click()
    print('\nEmail notifications and Confirmation of delivery checked')


def schedule_collection():
    confirm_collection_schedule = driver.find_element_by_id('SchedulePickupOnCallPickupRequest')
    confirm_collection_schedule.click()
    print('UPS Collection Schedule checked')


def goto_next_page():
    next_page_button = driver.find_element_by_class_name('btnArw')
    next_page_button.click()
    print('Moving to next page...')
    driver.implicitly_wait(5)


# def collection_time():
#     shipment_location = shipment_origin()
#     if shipment_location == 'NOW':
#         print(f'Shipment is coming from {shipment_location}')


def collection_time(shipment_location):
    if shipment_location == main_office:
        print(f'Shipment is coming from {shipment_location}')
        latest_collection_hour = Select(driver.find_element_by_id('latestTimeHour'))
        latest_collection_hour.select_by_visible_text('05')
        hour_selected = latest_collection_hour.first_selected_option
        latest_collection_minute = Select(driver.find_element_by_id('latestTimeMin'))
        latest_collection_minute.select_by_visible_text('00')
        minute_selected = latest_collection_minute.first_selected_option
    if shipment_location == engineering_subcontractor:
        print(f'Shipment is coming from {shipment_location}')
        latest_collection_hour = Select(driver.find_element_by_id('latestTimeHour'))
        latest_collection_hour.select_by_visible_text('04')
        hour_selected = latest_collection_hour.first_selected_option
        latest_collection_minute = Select(driver.find_element_by_id('latestTimeMin'))
        latest_collection_minute.select_by_visible_text('30')
        minute_selected = latest_collection_minute.first_selected_option
    print(f'Collection time set to: {hour_selected.text}:{minute_selected.text} P.M')


username_input = ups_username
userpass_input = ups_password


# username_input = input('Enter your username: ')
# userpass_input = input('Enter password: ')

login_to_ups(username_input, userpass_input)

shipment_location = shipment_origin()
# shipping_dest = input('\nEnter where this this shipment is going (Enter -list for list of destinations): ')
# shipping_dest = 'Wheatland'

# first_reference_input = input('Enter the first reference for this shipment: ')
# second_reference_input = input('Enter the second reference for this shipment: ')

first_reference_input = ''
second_reference_input = ''

# number_of_packages = input('Enter amount of packages in this shipment (Maximum is 20): ')
# total_shipment_weight = input('Enter the total weight of the packages: ')

number_of_packages = '2'
total_shipment_weight = '10'

select_shipping_destination()

shipment_package_weight()

shipment_notify()

schedule_collection()

goto_next_page()

collection_time(shipment_location)
