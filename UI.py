import os
import tkinter as tk
from tkinter import *
from tkinter import Tk
from PyPDF2 import PdfReader
from tkinter import filedialog

# ---------------------------- CONSTANTS ------------------------------- #
YELLOW = "#D9EDBF"
ORANGE = "#FFB996"
GREEN = "#FDFFAB"
FONT_NAME = "Courier"
reader = PdfReader("output.pdf")
page = reader.pages[0]
extracted_text = page.extract_text()
morse_sample_message =" / .-  / ... .. -- .--. .-.. .  / .--. -.. ..-.  / ..-. .. .-.. .  /  / - .... .. ...  / .. ...  / .-  / ... -- .- .-.. .-..  / -.. . -- --- -. ... - .-. .- - .. --- -.  / .-.-.- .--. -.. ..-.  / ..-. .. .-.. .  / -....-  /  / .--- ..- ... -  / ..-. --- .-.  / ..- ... .  / .. -.  / - .... .  / ...- .. .-. - ..- .- .-..  / -- . -.-. .... .- -. .. -.-. ...  / - ..- - --- .-. .. .- .-.. ... .-.-.-  / -- --- .-. .  / - . -..- - .-.-.-  / .- -. -..  / -- --- .-. .  /  / - . -..- - .-.-.-  / .- -. -..  / -- --- .-. .  / - . -..- - .-.-.-  / .- -. -..  / -- --- .-. .  / - . -..- - .-.-.-  / .- -. -..  / -- --- .-. .  / - . -..- - .-.-.-  /  / .- -. -..  / -- --- .-. .  / - . -..- - .-.-.-  / .- -. -..  / -- --- .-. .  / - . -..- - .-.-.-  / .- -. -..  / -- --- .-. .  / - . -..- - .-.-.-  / .- -. -..  / -- --- .-. .  / - . -..- - .-.-.-  / .- -. -..  / -- --- .-. .  /  / - . -..- - .-.-.-  / .- -. -..  / -- --- .-. .  / - . -..- - .-.-.-  / -... --- .-. .. -. --. --..--  / --.. --.. --.. --.. --.. .-.-.-  / .- -. -..  / -- --- .-. .  / - . -..- - .-.-.-  / .- -. -..  / -- --- .-. .  / - . -..- - .-.-.-  / .- -. -..  /  / -- --- .-. .  / - . -..- - .-.-.-  / .- -. -..  / -- --- .-. .  / - . -..- - .-.-.-  / .- -. -..  / -- --- .-. .  / - . -..- - .-.-.-  / .- -. -..  / -- --- .-. .  / - . -..- - .-.-.-  / .- -. -..  / -- --- .-. .  / - . -..- - .-.-.-  /  / .- -. -..  / -- --- .-. .  / - . -..- - .-.-.-  / .- -. -..  / -- --- .-. .  / - . -..- - .-.-.-  /  / .- -. -..  / -- --- .-. .  / - . -..- - .-.-.-  / .- -. -..  / -- --- .-. .  / - . -..- - .-.-.-  / .- -. -..  / -- --- .-. .  / - . -..- - .-.-.-  / .- -. -..  / -- --- .-. .  / - . -..- - .-.-.-  / .- -. -..  / -- --- .-. .  /  / - . -..- - .-.-.-  / .- -. -..  / -- --- .-. .  / - . -..- - .-.-.-  / .- -. -..  / -- --- .-. .  / - . -..- - .-.-.-  / . ...- . -.  / -- --- .-. . .-.-.-  / -.-. --- -. - .. -. ..- . -..  / --- -.  / .--. .- --. .  / ..---  / .-.-.- .-.-.- .-.-.-"

# ---------------------------- MAIN FUNCTION ------------------------------- #
morse_signs_dict = { 'A':'.-', 'B':'-...',
            'C':'-.-.', 'D':'-..', 'E':'.', 'È': '..-..-',
            'F':'..-.', 'G':'--.', 'H':'....',
            'I':'..', 'J':'.---', 'K':'-.-',
            'L':'.-..', 'M':'--', 'N':'-.',
            'O':'---', 'P':'.--.', 'Q':'--.-',
            'R':'.-.', 'S':'...', 'T':'-',
            'U':'..-', 'V':'...-', 'W':'.--',
            'X':'-..-', 'Y':'-.--', 'Z':'--..',
            '1':'.----', '2':'..---', '3':'...--',
            '4':'....-', '5':'.....', '6':'-....',
            '7':'--...', '8':'---..', '9':'----.',
            '0':'-----', ', ':'--..--', '.':'.-.-.-',
            '?':'..--..', '/':'-..-.', '-':'-....-',
            '(':'-.--.',
            ')':'-.--.-', ',': '--..--',' ': '/'}
# Function to encrypt the string according to the morse code chart
def encrypt(text=extracted_text):
    morse_code = ''
    for char in text.upper():
        if char in morse_signs_dict:
            morse_code += morse_signs_dict[char] + ' '
        elif char == ' ':
            morse_code += '/ '
    print(morse_code.strip())
    return morse_code.strip()  # Remove trailing spaces

# Function to decrypt the string according to the morse code chart
def decrypt(morse_code=morse_sample_message):
    morse_code = morse_code.split(' ')
    decoded_text = ''
    for code in morse_code:
        for key, value in morse_signs_dict.items():
            if code == value:
                decoded_text += key
        if code == '/':
            decoded_text += ' '
    print(decoded_text.replace('  ', ' '))
    return decoded_text.replace('  ', ' ')

def upload(status_label):
    file_window = tk.Toplevel(main_window)
    file_window.title("Choose your file")
    file_window.config(padx=100, pady=20, bg=YELLOW , highlightthickness=0)

    file_path_var = tk.StringVar()

    def select_file(x = file_window, status_label=status_label):
        file_path = filedialog.askopenfilename(title="Select a File")
        if file_path:
            file_path_var.set(file_path)
            # status_label.config(text="File selected successfully.")
            save_file()
            x.destroy()

    def save_file():
        selected_file_path = file_path_var.get()
        if selected_file_path:
            output_file_path = os.path.join(os.getcwd() , "output.pdf")
            try:
                with open(selected_file_path , 'rb') as source_file:
                    content = source_file.read()
                    with open(output_file_path , 'wb') as destination_file:
                        destination_file.write(content)
                status_label.config(text="File uploaded successfully.")
            except Exception as e:
                status_label.config(text=f"Error saving file: {str(e)}")
        else:
            status_label.config(text="Please select a file first.")

    # GUI Components for the file selection and saving window
    file_label = tk.Label(file_window , text="Select a file.")
    file_label.config(fg=ORANGE, font=("Courier", 12, "bold"), bg=YELLOW , highlightthickness=0)
    file_label.pack(pady=10)

    select_button = tk.Button(file_window , text="Select File" , command=select_file)
    select_button.config(bg=ORANGE)
    select_button.pack(pady=10)

    # save_button = tk.Button(file_window , text="Save File" , command=save_file)
    # save_button.pack(pady=10)


def place_holder():
    print("It is working")


# ---------------------------- UI SETUP ------------------------------- #
main_window = Tk()
main_window.title("Morse decoder")
main_window.config(padx=50, pady=50, bg=YELLOW, highlightthickness=0)

# Canvas
canvas = Canvas(width=230, height=230, bg=YELLOW)
decoder_img = PhotoImage(file="morse_icon.png")
canvas.create_image(115, 115, image=decoder_img)
canvas.grid(columnspan=2, row=1, pady=20, padx=20)

# Label Decoder
label_decoder = Label(text="Decoder", font=(FONT_NAME, 30, "bold"), fg=ORANGE, bg=ORANGE, justify="center")
label_decoder.config(bg=YELLOW, highlightthickness=0)
label_decoder.grid(columnspan=2, row=0)

status_label = Label(text="No file uploaded")
status_label.grid(column=1, row=2)
status_label.config(bg=YELLOW)

# Button
upload_button = Button(text="Upload", font= (FONT_NAME, 10, "bold"), height=1, width= 6, bg=ORANGE, command=lambda: upload(status_label))
upload_button.grid(column=0, row= 2)

decode_button = Button(text="Decode", font= (FONT_NAME, 10, "bold"), height=1, width= 6, bg=ORANGE, command=decrypt)
decode_button.grid(column=0, row= 4)

encode_button = Button(text="Encode", font= (FONT_NAME, 10, "bold"), height=1, width= 6, bg=ORANGE, command=encrypt)
encode_button.grid(column=1, row= 4)

# Space
label_check = Label(font=(FONT_NAME, 10, "bold"), fg=GREEN, bg=YELLOW)
label_check.grid(column=1, row=3)

main_window.mainloop()