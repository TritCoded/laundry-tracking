import datetime

def open_balance_file(mode='r+'):
    return open('laundry_balance.txt', mode)

def open_history_file(mode='a'):
    return open('history.txt', mode)

def read_balance(file_open):
    balance_str = file_open.read()
    if balance_str:
        return float(balance_str)
    else:
        return 0.0

def add_funds(file_open):
    file_open.seek(0)
    balance = read_balance(file_open)
    add_bool = input('Would you like to add funds (Y/N)?:\n').lower()
    if add_bool == 'y':
        additional_balance = float(input('How much money are you adding?:\n'))
        new_balance = balance + additional_balance
        file_open.seek(0)   
        file_open.truncate()   
        file_open.write(str(new_balance))   
        print(f'Your new balance is:\n${new_balance}')
        
        with open_history_file() as history_file:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            history_file.write(f"{timestamp}: Added ${additional_balance}.\n")
    else:
        print(f'Your balance is:\n{balance}')

def remove_funds(file_open):
    loads = int(input('How many loads of laundry?:\n'))
    if loads > 0:
        file_open.seek(0)
        balance = read_balance(file_open)
        print(balance)
        cost = 4.20 * loads
        new_balance = balance - cost
        file_open.seek(0)   
        file_open.truncate()   
        file_open.write(str(new_balance))   
        print(f'Your new balance is:\n{new_balance}')
        
        with open_history_file() as history_file:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            history_file.write(f"{timestamp}: Removed {cost} for {loads} loads of laundry\n")
    else:
        print("No loads entered.")

def main():
    with open_balance_file() as file_open:
        print("Balance:", read_balance(file_open))
        add_funds(file_open)
        remove_funds(file_open)

if __name__ == "__main__":
    main()
