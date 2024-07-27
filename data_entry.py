from datetime import datetime

DATE_format = "%d-%m-%Y"
CATEGORIES = {"I": "Income", "E": "Expense"}


def get_date(input_prompt, allow_default=False):
    date_input = input(input_prompt)
    if allow_default and not date_input:
        return datetime.today().strftime(DATE_format)

    try:
        valid_date = datetime.strptime(date_input, DATE_format)
        return valid_date.strftime(DATE_format)
    except ValueError:
        print("Invalid date format, Please enter date as dd-mm-yyyy.")
        get_date(input_prompt, allow_default)


def get_amount():
    try:
        amount_input = float(input("Enter the transaction amount: "))
        if amount_input <= 0:
            print("Amount should be greater than zero.")
            raise ValueError
        return amount_input
    except ValueError as e:
        print(e)
        return get_amount()


def get_category():
    category_input = input("Enter 'I' for Income or 'E' for Expense: ").upper()
    if category_input in CATEGORIES:
        return CATEGORIES[category_input]

    print("Invalid category, try again.")
    get_category()


def get_description():
    return input("Enter description(optional): ")
