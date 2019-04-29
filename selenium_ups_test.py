from selenium import webdriver
from selenium.webdriver.support.ui import Select
from ups_company_details import (ups_username, ups_password, main_office, engineering_subcontractor, my_email, ups_account_email, engineering_subcontractor_email)


driver = webdriver.Chrome()  # chromedriver in C:\Windows folder
driver.implicitly_wait(5)  # wait for page to load for 5 secs

# ############################ START OF FUNCTION DECLARATIONS ###########################


def login_to_ups(username, userpass):
    print('\nFiring up UPS...')
    driver.get('https://www.ups.com/uis/create')  # goes to UPS site
    window_before = driver.window_handles[0]  # gets current window
    window_before_title = driver.title  # names current window
    print(window_before_title)
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
    print(username + ' is logged into UPS!\n')  # feeback for login success


def goto_next_page():
    next_page_button = driver.find_element_by_class_name('btnArw')
    next_page_button.click()
    print('Moving to next page...')
    driver.implicitly_wait(5)


def collection_time(shipment_origin_location):
    latest_collection_hour = Select(driver.find_element_by_id('latestTimeHour'))
    latest_collection_minute = Select(driver.find_element_by_id('latestTimeMin'))
    if shipment_origin_location == main_office:
        latest_collection_hour.select_by_visible_text('05')
        latest_collection_minute.select_by_visible_text('00')
    if shipment_origin_location == engineering_subcontractor:
        latest_collection_hour.select_by_visible_text('04')
        latest_collection_minute.select_by_visible_text('30')
    print(f'Shipment is being collected from: {shipment_origin_location}')
    hour_selected = latest_collection_hour.first_selected_option
    minute_selected = latest_collection_minute.first_selected_option
    print(f'Collection time set to: {hour_selected.text}:{minute_selected.text} P.M')

# ############################ END OF FUNCTION DECLARATIONS ###########################


username_input = ups_username
userpass_input = ups_password

print('######### PLEASE NOTE THAT THIS TOOL IS ONLY FOR DELIVERIES TO EXISTING ADDRESSES, TO ADD NEW ADDRESSES OR SHIP ELSEWHERE PLEASE USE THE UPS WEBSITE #########\n')
login_to_ups(username_input, userpass_input)

shipment_origin_input = input('Where is the shipment coming from (DWE or NOW): ')


shipment_origin_location = shipment_origin_input


# START OF SHIPMENT BOOKING ###

driver.implicitly_wait(5)  # wait for page to load


if shipment_origin_input in engineering_subcontractor:
    edit_ship_from = driver.find_element_by_id('shipFromEdit')
    edit_ship_from.click()
    driver.implicitly_wait(5)  # wait for page load
    ship_from_select = Select(driver.find_element_by_id('select_shipFrom'))  # find selection box in origin edit page
    ship_from_select.select_by_visible_text('Wheatland')  # find option that matches Wheatland
    update_ship_from = driver.find_element_by_name('next')  # update button on shipment origin page, returns user to main address page
    update_ship_from.click()
    driver.implicitly_wait(5)

shipping_select = Select(driver.find_element_by_id('select_shipTo'))  # finds the shipping dropdown by id
while True:  # allows looping back to input
    shipping_dest = input('\nEnter where this this shipment is going (Enter -list for list of destinations): ')
    if shipping_dest == '-list':
        for option in shipping_select.options:  # loops through values in dropdown (<option> tags)
            print(option.text)  # prints option values text
            continue
    if shipping_dest.lower() not in [option.text.lower() for option in shipping_select.options]:  # loops through text in shipping_select options objects
        if shipping_dest != '-list':
            print('Your chosen destination does not exist in the address book. Please try again.')
            continue
    else:
        print('Filling in address fields...')  # notify that fields are about to be filled
        print('\n' + 'Begin Shipment'.center(35, '*') + '\n')  # notify that user is on beginning page and formatting to make heading stand out
        shipping_select.select_by_visible_text(shipping_dest)
        shipping_contact = driver.find_element_by_id('shipToContactNameValue')  # finds element with contact name
        contact_name = shipping_contact.get_attribute('value')  # gets value of contact name element
        print(f'\nShipment going to: {shipping_dest} ({contact_name})')  # grabs value from contact name element
        break
while True:
    first_reference_input = input('Enter the first reference for this shipment: ')
    textfield_first_shipment_reference = driver.find_element_by_id('reference_value1')  # finds first shipment reference field
    textfield_first_shipment_reference.clear()  # clears data in field in case any exists
    if len(first_reference_input) > 35:  # field only allows 35 characters
        print('Only 35 characters are allowed.')
        textfield_first_shipment_reference.clear()  # clears field if character limit exceeded
        continue  # loops back to while True
    else:
        textfield_first_shipment_reference.send_keys(first_reference_input)  # send input if fits in 35 character limit
        break
while True:
    second_reference_input = input('Enter the second reference for this shipment: ')
    textfield_second_shipment_reference = driver.find_element_by_id('reference_value2')
    textfield_second_shipment_reference.clear()
    if len(second_reference_input) > 35:
        print('Only 35 characters are allowed.')
        textfield_second_shipment_reference.clear()
        continue
    else:
        textfield_second_shipment_reference.send_keys(second_reference_input)
        break  # ends loop when second field is filled to move onto next section


while True:
    number_of_packages = int(input('Enter amount of packages in this shipment (Maximum is 20): '))  # convert input string to integer for value check
    if number_of_packages > 20:  # package value dropdown only goes up to 20
        print('Maxium selectable value is 20')
        continue  # loops back to input
    else:
        break

total_shipment_weight = input('Enter the total weight of the packages in kg: ')

select_package_amount = Select(driver.find_element_by_id('packageCount'))
select_package_amount.select_by_visible_text(str(number_of_packages))  # converts integer from input back to string for selection
package_weight_field = driver.find_element_by_id('shipmentTotalWeight')
package_weight_field.clear()  # clear field in case value exists
package_weight_field.send_keys(total_shipment_weight)
print(f'Amount of packages: {str(number_of_packages)}')
print(f'Total weight of packages is: {total_shipment_weight}kg')
email_notify_check = driver.find_element_by_id('emailNotify')
email_notify_check.click()
delivery_confirmation_check = driver.find_element_by_id('shipDeliveryConf')
delivery_confirmation_check.click()
print('\nEmail notifications and Confirmation of delivery checked')

# COLLECTION SCHEDULE
confirm_collection_schedule = driver.find_element_by_id('SchedulePickupOnCallPickupRequest')
confirm_collection_schedule.click()
print('UPS Schedule Collection checked')

goto_next_page()

driver.implicitly_wait(5)
print('\n' + 'Set collection details'.center(35, '*') + '\n')  # formatting to make heading stand out
# Collection time function to set time based on location
collection_time(shipment_origin_location)

first_email_notification_field = driver.find_element_by_name('quantumViewNotify.recipient#1.emailAddress')
if first_email_notification_field.get_attribute('value') == ups_account_email or first_email_notification_field.get_attribute('value') == engineering_subcontractor_email:
    first_email_notification_field.clear()
    first_email_notification_field.send_keys(my_email)
    print(f'First email field changed to: {my_email}')

goto_next_page()

driver.implicitly_wait(5)
print('\n' + 'Review shipment details'.center(35, '*') + '\n')  # formatting to make heading stand out
