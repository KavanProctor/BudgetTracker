import sqlite3
import datetime

conn = sqlite3.connect("expenses.db")
cur = conn.cursor()

while True:
    print('Select An option: ')
    print('1. Enter a new expense')
    print('2. view Expense report')

    choice = int(input())
    if choice == 1:
        print('please provide us with the information about this expense: ')
        date = input("What date did this expense occur on (DD-MM-YYYY): ")
        description = input("Give a description of the expense: ")

        #let the user choose from existing categories or create a new one
        cur.execute("SELECT DISTINCT category FROM expenses")

        categories = cur.fetchall() #gets all the categories from execute
        print("Select a category by number or create a new one")
        for idx, category in enumerate(categories):
            print(f"{idx+1}. {category[0]}")
        print(f" {len(categories)+ 1}. Create a new category")

        category_choice = int(input())
        if category_choice == len(categories) + 1:
            category = input("enter the new category name: ")
        else:
            category = [category_choice - 1][0]


        price = input("What was the total price of this expense: ")

        cur.execute("INSERT INTO expenses(Date, description, category, price) VALUES(?,?,?,?)", (date, description, category, price))

        conn.commit()

    elif choice == 2:
        print('Select one of the following options:')
        print('1. View Expense report: ')
        print('2. View monthly expense report by category: ')

        choice_2 = int(input())
        if choice_2 == 1:
            cur.execute("SELECT * FROM expenses")
            rows = cur.fetchall()
            for row in rows:
                print(row)
        if choice_2 == 2:
            month = input("Enter the month you would like to view (MM): ")
            year = input("Enter the year you would like to view (YYYY): ")
            cur.execute("""SELECT category, SUM(price) FROM expenses 
                WHERE strftime('%m', Date) = ? AND strftime('%Y', Date) = ?
                GROUP BY category""",(month,year))
            expenses = cur.fetchall()
            for expense in expenses:
                print(f"Category: {expense[0]}, Total: {expense[1]}")#not printing will need to work on
                
        else:
            exit()
    else:
        exit()

    repeat = input("Would you like to add more (y/n): ")
    if repeat.lower() != 'y':
        break

conn.close()