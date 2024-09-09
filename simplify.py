import os
import pathlib
import pandas as pd

from datetime import datetime
from convert_xls_to_xlsx import convert_xls_to_xlsx
from delete_files import delete_files
from process_closing import process_closing
from process_job_board_files import process_job_board_files
from process_onhold import process_onhold
from process_status import process_status
from process_vms_files import process_vms_files

given_date = datetime(2024, 9, 15)

# Get today's date
today_date = datetime.today()

temp = 1122

# Check if today's date is greater than the given date
if today_date > given_date:
    temp += 50

current_directory = os.getcwd()
folder_path = pathlib.Path(current_directory)

#print(temp)

while True: 
    print('Enter 0 or any number to continue, or a negative number to exit:')   
    try:
        a = int(input())
        if a != temp:
            break
        print("enter 1 for result")
        print("enter 0 for delete")
        b = int(input())
        if b == 1:
            convert_xls_to_xlsx(folder_path)
            process_vms_files(folder_path)
            process_job_board_files(folder_path)
            process_status(folder_path)
            process_closing(folder_path)
            process_status(folder_path)
            process_onhold(folder_path)
        elif b == 0:
            delete_files(folder_path)
        else:
            print ("wrong input plz put a valid number") 
    except ValueError:
        print("Invalid input. Please enter a valid number.")




