import tkinter as tk
import datetime

# commands/functions
def quit(event=None):
    root.destroy()

# TAKE NOTE THIS DOES NOT CLOSE THE FILE
def get_starting_balance(file):
    starting_balance = file.read()
    if starting_balance:
        return float(starting_balance)
    else:
        return 0.0


def add_funds(event=None):
    added_funds = funds_entry.get()
    laundry_balance_file = open('laundry_balance.txt', 'r+')
    starting_balance = get_starting_balance(laundry_balance_file)
    new_balance = round(float(starting_balance) + float(added_funds), 2)
    
    laundry_balance_file.seek(0)
    laundry_balance_file.truncate()
    laundry_balance_file.write(str(new_balance))
    
    laundry_balance_file.close()
    
    funds_entry.delete(0, tk.END)
    
    # add to history
    
    history = open('history.txt', 'r+')
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    new_entry = f'{timestamp}: Added ${added_funds}.\n'
    
    existing_history = history.readlines()
    history.seek(0)
    
    history.write(new_entry)
    history.writelines(existing_history)
    history.close()
    
    update_history()
    show_current_balance()

def payLoad():
    laundry_balance_file = open('laundry_balance.txt', 'r+')
    wash = 2.20
    dry = 2.00
    load = wash + dry
    
    starting_balance = get_starting_balance(laundry_balance_file)
    new_balance = round(starting_balance - load, 2)
    
    
    laundry_balance_file.seek(0)
    laundry_balance_file.truncate()
    laundry_balance_file.write(str(new_balance))
    laundry_balance_file.close()
    
    history = open('history.txt', 'r+')
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    new_entry = f'{timestamp}: Paid ${load}.\n'
    
    existing_history = history.readlines()
    history.seek(0)
    
    history.write(new_entry)
    history.writelines(existing_history)
    history.close()
    
    update_history()
    show_current_balance()

def show_current_balance():
    laundry_balance_file = open('laundry_balance.txt', 'r')
    current_balance = get_starting_balance(laundry_balance_file)
    laundry_balance_file.close()
    
    balance_text.config(text=f'Current balance: {current_balance}')


def update_history():
    history_file = open('history.txt', 'r')
    history = history_file.readlines()
    history_file.close()
    
    history_text.delete(0, tk.END)
    history_text.insert(tk.END, *history)

# window

root = tk.Tk()
root.title('Laundry Manager')
root.geometry('400x350')

# frames

display_balance = tk.Frame(root)
display_balance.pack(pady=15)

funds_text = tk.Frame(root)
funds_text.pack()

payload_text = tk.Frame(root)
payload_text.pack()

history_frame = tk.Frame(root)
history_frame.pack(expand=True, fill='both')

# labels, entries, buttons

funds_label = tk.Label(funds_text, text='Insert Funds:')
funds_label.pack(side='left')

funds_entry = tk.Entry(funds_text, width=10, justify='center')
funds_entry.pack(side='left', padx=5)

add_funds_button = tk.Button(funds_text, text='Add', padx=5, relief='raised', command=add_funds)
add_funds_button.pack(side='left')

balance_text = tk.Label(display_balance, text='Current balance: ', font='timesnewroman')
balance_text.pack(side='left')

history_label = tk.Label(history_frame, justify='left', text='History', font='timesnewroman')
history_label.pack()

scrollbar = tk.Scrollbar(history_frame)
scrollbar.pack(side='right', fill='y', pady=10)

history_text = tk.Listbox(history_frame, justify='left', selectmode='none', yscrollcommand=scrollbar.set)
history_text.pack(expand=True, fill='both', padx=10, pady=10)

root.bind('<Return>', add_funds)
root.bind('<Escape>', quit)

wash_button = tk.Button(payload_text, text='Add load [-$4.20]', padx=5, command=payLoad)
wash_button.pack(side='right', padx=10, pady=15)

show_current_balance()
update_history()

scrollbar.config(command=history_text.yview)

root.mainloop()

