# -*- coding: utf-8 -*-
"""Loan Qualifier Application.

This is a command line application to match applicants with qualifying loans.

Example:
    $ python app.py
"""
import sys
import fire
import questionary
from pathlib import Path

from qualifier.utils.fileio import load_csv, save_csv

from qualifier.utils.calculators import (
    calculate_monthly_debt_ratio,
    calculate_loan_to_value_ratio,
)

from qualifier.filters.max_loan_size import filter_max_loan_size
from qualifier.filters.credit_score import filter_credit_score
from qualifier.filters.debt_to_income import filter_debt_to_income
from qualifier.filters.loan_to_value import filter_loan_to_value

#
# the default argument of the csvpath is the daily_rate_sheet.csv
# the default value is displayed to the user when a file path to the rate sheet is not provided at input
#
def load_bank_data(csvpath = 'data/daily_rate_sheet.csv'):
    """Ask for the file path to the latest banking data and load the CSV file.

    Returns:
        The bank data from the data rate sheet CSV file.
    """
    csvpath_input = questionary.text("Enter a file path to a rate-sheet (.csv):").ask()
    #
    # validate the input
    # if the input is not provided by the user, then daily rate sheet provided under the data folder will be used for calculations
    #
    if (len(str(csvpath_input)) > 0):
        csvpath = Path(csvpath_input)
        if not csvpath.exists():
            sys.exit(f"Oops! Can't find this path: {csvpath}")
    else:
        questionary.print("No file path provided. Default file path of data/daily_rate_sheet.csv is assumed")
    # if user did not provide a path, the default list from the daily rate sheet is returned
    return load_csv(csvpath)


def get_applicant_info():
    """Prompt dialog to get the applicant's financial information.

    Returns:
        Returns the applicant's financial information.
    """

    credit_score = questionary.text("What's your credit score?").ask()
    debt = questionary.text("What's your current amount of monthly debt?").ask()
    income = questionary.text("What's your total monthly income?").ask()
    loan_amount = questionary.text("What's your desired loan amount?").ask()
    home_value = questionary.text("What's your home value?").ask()

    # commenting the assignment and combining it with the return statement below
    # credit_score = int(credit_score)
    # debt = float(debt)
    # income = float(income)
    # loan_amount = float(loan_amount)
    # home_value = float(home_value)

    # i returned the values with type cast so as to keep the programming logic concise and readable
    # hope this is ok
    return int(credit_score), float(debt), float(income), float(loan_amount), float(home_value)


def find_qualifying_loans(bank_data, credit_score, debt, income, loan, home_value):
    """Determine which loans the user qualifies for.

    Loan qualification criteria is based on:
        - Credit Score
        - Loan Size
        - Debit to Income ratio (calculated)
        - Loan to Value ratio (calculated)

    Args:
        bank_data (list): A list of bank data.
        credit_score (int): The applicant's current credit score.
        debt (float): The applicant's total monthly debt payments.
        income (float): The applicant's total monthly income.
        loan (float): The total loan amount applied for.
        home_value (float): The estimated home value.

    Returns:
        A list of the banks willing to underwrite the loan.

    """

    # Calculate the monthly debt ratio
    monthly_debt_ratio = calculate_monthly_debt_ratio(debt, income)
    print(f"The monthly debt to income ratio is {monthly_debt_ratio:.02f}")

    # Calculate loan to value ratio
    loan_to_value_ratio = calculate_loan_to_value_ratio(loan, home_value)
    print(f"The loan to value ratio is {loan_to_value_ratio:.02f}.")

    # Run qualification filters
    bank_data_filtered = filter_max_loan_size(loan, bank_data)
    bank_data_filtered = filter_credit_score(credit_score, bank_data_filtered)
    bank_data_filtered = filter_debt_to_income(monthly_debt_ratio, bank_data_filtered)
    bank_data_filtered = filter_loan_to_value(loan_to_value_ratio, bank_data_filtered)

    print(f"Found {len(bank_data_filtered)} qualifying loans")

    return bank_data_filtered


def save_qualifying_loans(qualifying_loans):
    """Saves the qualifying loans to a CSV file.

    Args:
        qualifying_loans (list of lists): The qualifying bank loans.
        bank_data : The header row that needs to be printed in the csv file
    """
    # @TODO: Complete the usability dialog for savings the CSV Files.
    # YOUR CODE HERE!
    # Acceptance Criteria 3:
    # Given that I have a list of qualifying loans, when I’m prompted to save the results, 
    # then I should be able to opt out of saving the file.
    save_to_file_choice = questionary.confirm("Would you like to save the qualifying loans to a CSV file?").ask()
    # Because user can either choose the answer as Y, n or any other, handle the inputs below.
    if(save_to_file_choice == True):
        # Acceptance Criteria 1:
        # Given that I’m using the loan qualifier CLI, when I run the qualifier, 
        # then the tool should prompt the user to save the results as a CSV file
        file_path = Path(questionary.text("Enter a file path to store the qualifying loans CSV file:").ask())
        if not file_path.exists():
            sys.exit(f"Oops! Can't find this path: {file_path}")
        # commenting the hard coded file name as part of the review comment during grading
        # csv_file_name = 'qualifying_loans.csv'
        # taking the name of the file from user input
        csv_file_name = questionary.text("Enter the name of the file where you wish to save the data ").ask()
        csvpath = Path(file_path).joinpath(csv_file_name)
        # because header row was skipped at the time of reading the csv file, the header is being hard coded in this assignment
        save_csv(csvpath, qualifying_loans,["Lender Name", "Loan Maximum", "Loan to Value", "Debt to Income", "Credit Minimum, APR%"])
        questionary.print(f"The qualifying loans are written to the file located at {csvpath}")
    # when there are qualifying loans and the user did not select to save them to a file, display the loans on the screen
    # this fork is written to practice elif condition and was not asked in the assignment
    else:
        # (save_to_file_choice == False):
        print(f"""Your qualifying loans are
                {qualifying_loans}
            """)

def run():
    """The main function for running the script."""

    # Load the latest Bank data
    bank_data = load_bank_data()

    # Get the applicant's information
    credit_score, debt, income, loan_amount, home_value = get_applicant_info()

    # Find qualifying loans
    qualifying_loans = find_qualifying_loans(
        bank_data, credit_score, debt, income, loan_amount, home_value
    )

    if(len(qualifying_loans) > 0):
        # Save qualifying loans
        save_qualifying_loans(qualifying_loans)
    else:
        # Acceptance Criteria 2: 
        # Given that no qualifying loans exist, when prompting a user to save a file, 
        # then the program should notify the user and exit.
        sys.exit(f"""There are no qualifying loans found for 
                     credit score: {credit_score}, 
                     debt: ${debt:,.2f}, 
                     income: ${income:,.2f}, 
                     loan_amount: ${loan_amount:,.2f} and 
                     home value of ${home_value:,.2f} """)

if __name__ == "__main__":
    fire.Fire(run)
