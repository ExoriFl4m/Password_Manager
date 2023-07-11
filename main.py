from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = [
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
    ]
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    symbols = ["!", "#", "$", "%", "&", "(", ")", "*", "+"]

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)
    password = "".join(password_list)
    password_generated.config(text="Password Copied to Clipboard!")
    pyperclip.copy(password)
    password_entry.delete(0, END)
    password_entry.insert(0, password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    password = password_entry.get()
    email = email_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0 or len(email) == 0:
        messagebox.showinfo(
            title="Error", message="Please make your you haven't left any fields empty."
        )
    else:
        try:
            with open("data.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)

            with open("data.json", "w") as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)
            password_generated.config(text="")


# ---------------------------- Search   ------------------------------- #
def find_password():
    website = website_entry.get()
    if len(website) == 0:
        messagebox.showinfo(
            title="Error",
            message="Please enter the Website to search for the corresponding password.",
        )
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            messagebox.showinfo(
                title="Error",
                message="No Data File found.",
            )
        else:
            if website in data:
                email = data[website]["email"]
                password = data[website]["password"]
                messagebox.showinfo(
                    title=website,
                    message=f"Website: {website}\nEmail: {email}\nPassword: {password}",
                )


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg="white")
window.resizable(width=False, height=False)

canvas = Canvas(width=200, height=200, highlightthickness=0, bg="white")
padlock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=padlock_img)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website:")
website_label.config(bg="white", fg="black")
website_label.grid(column=0, row=1)
user_label = Label(text="Email/Username:")
user_label.config(bg="white", fg="black")
user_label.grid(column=0, row=2)
password_label = Label(text="Password: ")
password_label.config(bg="white", fg="black")
password_label.grid(column=0, row=3)
password_generated = Label(text="")
password_generated.config(bg="white", fg="black")
password_generated.grid(column=1, row=5)

# Entries
website_entry = Entry(width=22)
website_entry.focus()
website_entry.grid(column=1, row=1, columnspan=1)
email_entry = Entry(width=40)
email_entry.insert(0, "")
email_entry.grid(column=1, row=2, columnspan=2)
password_entry = Entry(width=22)
password_entry.grid(column=1, row=3)

# Buttons
add_button = Button(text="Add", highlightbackground="white", width=36, command=save)
add_button.grid(column=1, row=4, columnspan=2)
generate_button = Button(
    text="Generate Password", highlightbackground="white", command=generate_password
)
generate_button.grid(column=2, row=3)
search_button = Button(
    text="search", highlightbackground="white", width=13, command=find_password
)
search_button.grid(column=2, row=1)

window.mainloop()
