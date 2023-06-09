# Loan Qualifier CLI

Loan Qulifier is a Command Line Interface that identifies different loans that are available based on the input criteria of financial information of the applicant - credit score, income, debt, home value and requested loan amount.
The available loans from different Lenders are either written to a file in a path identified by a user input, or dislayed on the screen if the write to file option is not selected. If the file location of the lender requirements is not provided at the input, then the default file under data/daily_rate_sheet.csv is assumed.
---

## Technologies

This project leverages python 3.7.13 with the following packages:

* [fire](https://github.com/google/python-fire) - For the command line interface, help page, and entrypoint.

* [questionary](https://github.com/tmbo/questionary) - For interactive user prompts and dialogs

The Loan Qualifier CLI uses the following data files if a rate sheet file location is not provided at input
* [daily_rate_sheet.csv](loan_qualifier_app/data/daily_rate_sheet.csv)

The output file is named as qualifying_loans.csv and is written to a folder whose name is entered by the user

---

## Installation Guide

Before running the application first install the following dependencies.

```python
  pip install fire
  pip install questionary
```

---

## Usage

To use the loan qualifier application simply clone the repository and run the **app.py** with:

```python
python app.py
```
The first user input appears as

![rate sheet default value illustration](loan_qualifier_app/images/rate_sheet_default.jpg)

The Loan Qualifier CLI prompts for user input of the path where the file should be saved.
The tool output appears as:
![Loan Qualifier CLI save file](loan_qualifier_app/images/qualifying_loans_illustration.jpg)


---

## Contributors

[Sreedhar](j_sreedhar@yahoo.com)

---

## License

MIT
