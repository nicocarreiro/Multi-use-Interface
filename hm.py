import tkinter as tk

def update_options(new_options):
    menu = option_menu['menu']
    menu.delete(0, 'end')  # Clear existing options
    for option in new_options:
        menu.add_command(label=option, command=lambda value=option: selected_option.set(value))

root = tk.Tk()

# Initial options
options = ['Option 1', 'Option 2', 'Option 3']
selected_option = tk.StringVar(value=options[0])

# Create OptionMenu
option_menu = tk.OptionMenu(root, selected_option, *options)
option_menu.pack()

# Button to update options
update_button = tk.Button(root, text="Update Options", command=lambda: update_options(['New Option 1', 'New Option 2']))
update_button.pack()

root.mainloop()
