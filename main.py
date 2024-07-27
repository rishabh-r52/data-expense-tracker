import pandas as pd
import csv
from datetime import datetime
from data_entry import get_amount, get_category, get_date, get_description, DATE_format
import matplotlib.pyplot as plt


class CSV:
    CSV_file = 'finance-data.csv'
    COLUMNS = ["date", "amount", "category", "description"]

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_file)
        except FileNotFoundError:
            df = pd.DataFrame(columns=CSV.COLUMNS)
            df.to_csv(cls.CSV_file, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        }
        with open(cls.CSV_file, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=CSV.COLUMNS)
            writer.writerow(new_entry)

        print("New entry added successfully")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_file)
        df['date'] = pd.to_datetime(df['date'], format=DATE_format)
        start_date = datetime.strptime(start_date, DATE_format)
        end_date = datetime.strptime(end_date, DATE_format)

        mask = (df['date'] >= start_date) & (df['date'] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("No transactions found!")
        else:
            print(
                f"\nTransactions from {start_date.strftime(DATE_format)} to {end_date.strftime(DATE_format)}:"
            )
            print(
                filtered_df.to_string(
                    index=False, formatters={'date': lambda x: x.strftime(DATE_format)}
                )
            )

        total_income = filtered_df[filtered_df['category'] == 'Income']['amount'].sum()
        total_expense = filtered_df[filtered_df['category'] == 'Expense']['amount'].sum()

        print("\nSummary:")
        print(f"Total Income: ${total_income:.2f}")
        print(f"Total Expense: ${total_expense:.2f}")
        print(f"Net savings: ${(total_income - total_expense):.2f}")

        return filtered_df


def add():
    CSV.initialize_csv()
    date = get_date("Enter date as dd-mm-yyyy (Default - Today's Date): ", allow_default=True,)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)


def plot_transactions(df):
    df.set_index('date', inplace=True)

    income_df = (
        df[df['category'] == 'Income']
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )
    expense_df = (
        df[df['category'] == 'Expense']
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )

    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df['amount'], label='Income', color='g')
    plt.plot(expense_df.index, expense_df['amount'], label='Expense', color='r')
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income & Expenses over time")
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    while True:
        print("\n----------Menu----------")
        print("1. Add a transaction")
        print("2. View transactions")
        print("3. Exit")
        choice = int(input("Choose an option: "))

        match choice:
            case 1:
                add()
            case 2:
                start_date = get_date("Enter the start date as dd-mm-yyyy: ")
                end_date = get_date("Enter the end date as dd-mm-yyyy: ")
                df = CSV.get_transactions(start_date, end_date)
                if input("Do you wish to see the data plotted in graph (y/n)?").lower() == "y":
                    plot_transactions(df)
            case 3:
                print("Exiting...")
                break
            case _:
                print("Invalid input, try again.")


if __name__ == "__main__":
    main()
