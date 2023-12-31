import logging
import os
import pandas as pd
from classes.user import User
from functions.imported_transactions import import_transactions
from functions.add_imported_block import add_imported_block
from data_processing.generate_reports import generate_reports
from data_processing.trial_balance import generate_trial_balance
from data_processing.export_bc_to_excel import export_blockchain_to_excel
from functions.add_imported_block import add_imported_block
from classes.blockchain import Blockchain
from functions.imported_transactions import import_transactions


# .+.. (main program logic)


# When you run this code, the logging configuration will be set up, and any subsequent log messages generated by your 
# application using the logging module will be written to the "blockchain.log" file with the specified format and 
# timestamp.
logging.basicConfig(filename='blockchain.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# Predefined dictionary of Accounting Classes and Subclasses
accounting_classes = {
    'Assets': ['Cash', 'Accounts Receivable', 'Inventory'],
    'Liabilities': ['Accounts Payable', 'Loans Payable', 'Accrued Expenses'],
    'Equity': ['Owner\'s Capital', 'Retained Earnings'],
    'Revenue': ['Sales', 'Service Revenue'],
    'Expenses': ['Rent Expense', 'Salaries Expense', 'Utilities Expense']
}

# logging.info('Authorized users initialized')
authorized_users = {"James": User("James")}   # Log that authorized users were initialized
# ledger = Blockchain(authorized_users)
ledger = Blockchain(authorized_users)

# Load the blockchain if a save file exists
if os.path.isfile("blockchain_data.txt"):
    ledger.load_from_file("blockchain_data.txt")
logging.info('Blockchain created')  # Log that the blockchain was created

# If the user wants to import transactions from a file
user_input = input('Do you want to import transactions from a file? (yes/no): ')
if user_input.lower() == 'yes':
    filename = input('Enter the filename: ')
    # Check if '.xlsx' is already in the filename
    filename = filename if filename.endswith('.xlsx') else f"{filename}.xlsx"
    try:
        transactions = import_transactions(filename)
        if transactions:
            sender_name = input('Enter the sender name: ')
            add_imported_block(ledger, transactions, sender_name, filename)
        else:
            print('No transactions found in the file.')
    except FileNotFoundError:
        print('File not found.')
    except Exception as e:
        print(f'Error importing transactions: {str(e)}')


# Commented out by James White
# while True:
#     user_input = input('Do you want to add a new block? (yes/no): ')
#     if user_input.lower() == 'yes':
#         # First transaction
#         print("Enter details for the first transaction:")
#         sender_name1 = input('Enter the sender name: ')
#         accounting_class1, subclass1 = get_accounting_class_subclasses()
#         debit1 = float(input('Enter the debit: '))
#         credit1 = float(input('Enter the credit: '))
#         transaction_detail1 = input('Enter the transaction detail (optional): ')
#         accounting_date1 = input('Enter the accounting date (YYYY-MM-DD) or leave blank for today: ')
#         if accounting_date1:
#             accounting_date1 = pd.to_datetime(accounting_date1).timestamp()

#         # Second transaction
#         print("Enter details for the second transaction:")
#         sender_name2 = input('Enter the sender name: ')
#         accounting_class2, subclass2 = get_accounting_class_subclasses()
#         debit2 = float(input('Enter the debit: '))
#         credit2 = float(input('Enter the credit: '))
#         transaction_detail2 = input('Enter the transaction detail (optional): ')
#         accounting_date2 = input('Enter the accounting date (YYYY-MM-DD) or leave blank for today: ')

#         # Check if the totals of debits and credits are equal
#         if debit1 + debit2 != credit1 + credit2:
#             print("The total debits and credits do not match. Please reenter the transactions.")
#             continue

#         # Create the Transaction objects
#         transaction1 = Transaction(
#             sender=authorized_users[sender_name1],
#             accounting_class=accounting_class1,
#             subclass=subclass1,
#             debit=debit1,
#             credit=credit1,
#             transaction_detail=transaction_detail1,
#             accounting_date=accounting_date1,
#         )
#         transaction2 = Transaction(
#             sender=authorized_users[sender_name2],
#             accounting_class=accounting_class2,
#             subclass=subclass2,
#             debit=debit2,
#             credit=credit2,
#             transaction_detail=transaction_detail2,
#             accounting_date=accounting_date2,
#         )
        
#         # Add the transactions to a new block
#         new_block_number = len(ledger.chain) + 1
#         ledger.add_block([transaction1, transaction2], sender_name1)

#         # If the user wants to import transactions from a file
#         user_input = input('Do you want to import transactions from a file? (yes/no): ')
#         if user_input.lower() == 'yes':
#             filename = input('Enter the filename: ')
#             transactions = import_transactions(filename, new_block_number)
#             if transactions:
#                 sender_name = input('Enter the sender name: ')
#                 ledger.add_block(transactions, sender_name)
#             else:
#                 print('No transactions found in the file.')
#     elif user_input.lower() == 'no':
#         break
#     else:
#         print('Invalid input. Please enter "yes" or "no".')



start_date = end_date = None
start_time = end_time = None

user_input = input('Do you want to generate a Trial Balance report for a specific time period? (yes/no): ')
if user_input.lower() == 'yes':
    start_date = input('Enter the start date (YYYY-MM-DD): ')
    end_date = input('Enter the end date (YYYY-MM-DD): ')
    try:
        start_time = pd.to_datetime(start_date)
        end_time = pd.to_datetime(end_date)
        filename = 'trial_balance_report.xlsx'
        generate_trial_balance(ledger, fiscal_year=(start_time, end_time), filename=filename)
        print(f"Trial Balance report generated successfully. File saved as '{filename}'")
    except ValueError:
        print("Invalid date format. Please enter dates in the format 'YYYY-MM-DD'.")
else:
    print("No Trial Balance report was generated.")

user_input = input('Do you want to generate financial reports for a specific time period? (yes/no): ')
if user_input.lower() == 'yes':
    start_date = input('Enter the start date (YYYY-MM-DD): ')
    end_date = input('Enter the end date (YYYY-MM-DD): ')
    try:
        start_time = pd.to_datetime(start_date)
        end_time = pd.to_datetime(end_date)
        reports_filename = 'financial_statements.xlsx'
        generate_reports(ledger, start_time, end_time, reports_filename)
        print(f"Financial reports generated successfully. File saved as '{reports_filename}'")
    except ValueError:
        print("Invalid date format. Please enter dates in the format 'YYYY-MM-DD'.")
else:
    print("No financial reports were generated.")

export_blockchain_to_excel(ledger, 'blockchain_data.xlsx', fiscal_year=(start_time, end_time))

# Save the blockchain before exiting
ledger.save_to_file("blockchain_data.txt")
logging.info('Blockchain saved to file')  # Log that the blockchain was saved to file