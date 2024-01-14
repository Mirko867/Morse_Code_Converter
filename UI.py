import os
import tkinter as tk
from tkinter import *
from tkinter import Tk
from PyPDF2 import PdfReader
from tkinter import filedialog
from fpdf import FPDF

# ---------------------------- CONSTANTS ------------------------------- #
YELLOW = "#D9EDBF"
ORANGE = "#FFB996"
GREEN = "#FDFFAB"
FONT_NAME = "Courier"
reader = PdfReader("output.pdf")

# ---------------------------- DICTIONARIES ------------------------------- #
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

# ---------------------------- MAIN FUNCTION ------------------------------- #
# Function to encrypt the string according to the morse code chart
def convert(selected_mode):
    global reader
    if selected_mode == "Encode":
        final_morse_code = ''
        for page in reader.pages:
            text = page.extract_text()
            for char in text.upper():
                if char in morse_signs_dict:
                    final_morse_code += morse_signs_dict[char] + ' '
                elif char == ' ':
                    final_morse_code += '/ '
            final_morse_code += '\n'  # Add a newline after processing each page
        text_display.config(state=tk.NORMAL)
        text_display.delete(1.0 , tk.END)
        text_display.insert(tk.END , f"{final_morse_code.strip()}")
        text_display.config(state=tk.DISABLED)
        return final_morse_code.strip()  # Remove trailing spaces
    else:
        text = ''
        for page_num in range(len(reader.pages)):
            page = reader.pages[ page_num ]
            text += page.extract_text()
        initial_morse_code = text.split('  ')
        decoded_text = ''
        for code in initial_morse_code:
            letters = code.split(' ')
            for letter in letters:
                if letter in morse_signs_dict.values():
                    decoded_text += [k for k, v in morse_signs_dict.items() if v == letter][0]
            decoded_text += ' '
        text_display.config(state=tk.NORMAL)
        text_display.delete(1.0 , tk.END)
        text_display.insert(tk.END, f"{decoded_text.strip()}")
        text_display.config(state=tk.DISABLED)
        return decoded_text.strip()

def upload(status_label):
    file_window = tk.Toplevel(main_window)
    file_window.title("Choose your file")
    file_window.config(padx=100, pady=20, bg=YELLOW , highlightthickness=0)

    file_path_var = tk.StringVar()

    def select_file(x = file_window, status_label=status_label):
        global reader
        file_path = filedialog.askopenfilename(title="Select a File")
        if file_path:
            file_path_var.set(file_path)
            reader = PdfReader(file_path)  # Update the PdfReader with the new file
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

def on_close():
    output_file_path = os.path.join(os.getcwd(), "output.pdf")

    # Delete the existing "output.pdf" file
    try:
        os.remove(output_file_path)
    except FileNotFoundError:
        pass  # Ignore if the file doesn't exist

    # Create a new empty "output.pdf" file with a placeholder text
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Please insert your text", ln=True, align='C')
        pdf.output(output_file_path)
    except Exception as e:
        print(f"Error creating empty file: {str(e)}")

    # Close the main window
    main_window.destroy()


# ---------------------------- UI SETUP ------------------------------- #
main_window = Tk()
main_window.title("Morse decoder")
main_window.config(padx=10, pady=10, bg=YELLOW, highlightthickness=0)

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

# Upload Button
upload_button = Button(text="Upload", font= (FONT_NAME, 10, "bold"), height=1, width= 6, bg=ORANGE, command=lambda: upload(status_label))
upload_button.grid(column=0, row= 2)

# Space
label_check = Label(font=(FONT_NAME, 10, "bold"), fg=GREEN, bg=YELLOW)
label_check.grid(column=1, row=3)

# Mode selection
selected_mode = tk.StringVar()

encode = tk.Radiobutton(main_window, text="Encode", variable=selected_mode, value="Encode", bg=YELLOW)
encode.grid(column=0, row=4)

decode = tk.Radiobutton(main_window, text="Decode", variable=selected_mode, value="Decode", bg=YELLOW)
decode.grid(column=1, row=4)

# Space
label_check = Label(font=(FONT_NAME, 10, "bold"), fg=GREEN, bg=YELLOW)
label_check.grid(column=1, row=5)

# Convert button
convert_button = Button(text="Convert", font= (FONT_NAME, 10, "bold"), height=1, width= 7, bg=ORANGE, command=lambda: convert(selected_mode.get()))
convert_button.grid(columnspan=2, row= 7)

# Text widget to display the result
text_display = tk.Text(main_window, wrap=tk.WORD, height=10, width=60)
text_display.grid(columnspan=2, row=6)
text_display.config(state=tk.DISABLED)

main_window.protocol("WM_DELETE_WINDOW", on_close)

main_window.mainloop()