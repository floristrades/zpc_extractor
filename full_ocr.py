import pytesseract
import datetime
import csv
import os
import pyautogui
import keyboard
import time
import tkinter as tk
from PIL import Image, ImageDraw

def count_csv_rows(pair_tf):
    csv_file_path = os.path.abspath(f"zpc_csv/zpc_{pair_tf}.csv")
    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        row_count = sum(1 for _ in reader) - 1
    return row_count

# Save the timestamp for unique file naming
def get_timestamp():
    return time.strftime("%Y%m%d%H%M%S", time.localtime())

# Save image on home key press
def save_image(event):
    counter()
    #save_ohlc()
    global pair_tf
    hotkey_label.place_forget()
    pair_tf = pair_entry.get()  # Get pair_tf from the input field

    # Capture screenshot
    screenshot = pyautogui.screenshot()
    image = screenshot.copy()

    global csv_file
    csv_file = os.path.join('./zpc_csv', f'zpc_{pair_tf}.csv')

    # Add blue box in the middle
    draw = ImageDraw.Draw(image)
    width, height = image.size
    box_size = 100
    x0 = 54
    y0 = 1258
    x1 = 3037
    y1 = 1310
    top_left = (x0, y0)
    bottom_right = (x1, y1)
    draw.rectangle((top_left, bottom_right), outline="blue", width=3)

    cropped_box = image.crop((x0, y0, x1, y1))

    # Set the path to the Tesseract executable (Update with your path)
    pytesseract.pytesseract.tesseract_cmd = './Tesseract-OCR/tesseract.exe'

    # Perform OCR using pytesseract
    ocr_text = pytesseract.image_to_string(cropped_box)

    # Replace the single quote character with '20'
    ocr_text = ocr_text.replace("‘", "20")

    # Remove leading/trailing whitespace characters
    ocr_text = ocr_text.strip()

    if not ocr_text:
        hotkey_text.set("OCR Result is empty!")
    
    try:
        # Parse ocr_text as a datetime object
        date_format = "%a %d %b %Y %H:%M"
        parsed_date = datetime.datetime.strptime(ocr_text, date_format)

        # Convert parsed_date to Unix time
        unix_time = int(parsed_date.timestamp())

        # Print the OCR result and Unix time in the Tkinter window
        log_text.set(f"Date Time: {ocr_text}\nUnix Time: {unix_time}\n")

        # Save the Unix time and zpc_presence to the CSV file
        csv_file = os.path.join('./zpc_csv', f'zpc_{pair_tf}.csv')

        try:
            with open(csv_file, 'a', newline='') as file:
                writer = csv.writer(file)

                # Write the data row
                writer.writerow([unix_time, 1, parsed_date, pair_tf])
            
            save_label_succes()
        except Exception as e:
            save_label_error()

    except ValueError:
        hotkey_text.set("\nError: Invalid date format!")
        hotkey_label.place(x=70, y=10)
        log_text.set("")
        save_label_error()
        time.sleep(1)
        hotkey_text.set("\nPress home to capture.")
        hotkey_label.place(x=75, y=10)


# Save image on home key press
def save_ohlc(event):
    # Capture screenshot
    screenshot = pyautogui.screenshot()
    image = screenshot.copy()

    # Add blue box in the middle
    draw = ImageDraw.Draw(image)
    width, height = image.size
    box_size = 100
    x0 = 64
    y0 = 68
    x1 = 340
    y1 = 110
    top_left = (x0, y0)
    bottom_right = (x1, y1)
    draw.rectangle((top_left, bottom_right), outline="blue", width=3)

    ohlc_box = image.crop((x0, y0, x1, y1))

    image.open(ohlc_box)

    # Set the path to the Tesseract executable (Update with your path)
    pytesseract.pytesseract.tesseract_cmd = './Tesseract-OCR/tesseract.exe'

    # Perform OCR using pytesseract
    ohlc_text = pytesseract.image_to_string(ohlc_box)

    save_text = tk.StringVar()
    save_label = tk.Label(root, textvariable=save_text, font=("Arial", 11), justify="center", fg=text_color, bg="black")
    save_label.pack(anchor="center")
    save_label.place(x=50, y=80)   
    # Pack the save label with horizontal centering
    save_label.pack(anchor="center", padx=5)
    save_label.place(relx=0.5, y=80, anchor="center")
    save_text.set(f"{ohlc_text}")

    if not ohlc_text:
        hotkey_text.set("OCR Result is empty!")



def save_label_succes():
        save_text = tk.StringVar()
        save_label = tk.Label(root, textvariable=save_text, font=("Arial", 11), justify="center", fg=text_color, bg="black")
        save_label.pack(anchor="center")
        save_label.place(x=50, y=80)   
        # Pack the save label with horizontal centering
        save_label.pack(anchor="center", padx=5)
        save_label.place(relx=0.5, y=80, anchor="center")
        save_text.set(f"Saved to zpc_{pair_tf}.csv successfully!")

        time.sleep(1)
        save_text.set("")

def save_label_error():
        save_text = tk.StringVar()
        save_label = tk.Label(root, textvariable=save_text, font=("Arial", 11), justify="center", fg=text_color, bg="black")
        save_label.pack(anchor="center")
        save_label.place(x=50, y=80)   
        # Pack the save label with horizontal centering
        save_label.pack(anchor="center", padx=5)
        save_label.place(relx=0.5, y=80, anchor="center")
        save_text.set(f"Failed to save to zpc_{pair_tf}.csv!")
        time.sleep(1)
        save_text.set("")
        

def exit_program():
    root.destroy()
    keyboard.unhook_all()

def save_label_fix():
        save_text = tk.StringVar()
        save_label = tk.Label(root, textvariable=save_text, font=("Arial", 11), justify="center", fg=text_color, bg="black")
        save_label.pack(anchor="center")
        save_label.place(x=50, y=80)   
        # Pack the save label with horizontal centering
        save_label.pack(anchor="center", padx=5)
        save_label.place(relx=0.5, y=80, anchor="center")

def start_listening():
    global pair_tf  # Make pair_tf a global variable
    pair_tf = pair_entry.get()  # Get pair_tf from the input field
    global csv_file
    csv_file = os.path.abspath(f"zpc_csv/zpc_{pair_tf}.csv")
    check_csv_file(csv_file)  # Pass csv_file as an argument

    if pair_tf:
        pair_entry.pack_forget()  # Hide the entry widget
        pair_entry.place_forget()  # Hide the entry widget
        input_label.pack_forget()  # Hide the input label
        input_label.place_forget()  # Hide the input label
        home_button.pack_forget()  # Hide the "Start Listening" button
        home_button.place_forget()  # Hide the "Start Listening" button
        csv_label.pack_forget()  # Hide the csv files list
        csv_label.place_forget()  # Hide the csv files list
        csv_file_path = os.path.abspath(f"zpc_csv/zpc_{pair_tf}.csv")
        check_csv_file(csv_file)
        
        root.geometry("360x140+1540+0")
        save_label_fix()
        root.update()  # Refresh the layout
        keyboard.on_press_key("home", lambda event: save_image(event))
        hotkey_text.set("\nPress home to capture.")

        # Create a label to display the saving message with smaller font size
        csv_create_file()
    else:
        hotkey_text.set("Error: Enter pair_tf value!")

def counter():
    rows = count_csv_rows(pair_tf)
    row_text = tk.StringVar()
    row_text.set(f"ZPC's logged: {rows}")  
    counter_label = tk.Label(root, textvariable=row_text, font=("Arial", 9), fg=text_color, bg=f"{text_color_input}")
    counter_label.pack(side=tk.RIGHT, padx=10, pady=10, anchor=tk.SE)
    counter_label.place(x=10, y=112)

# Create the Tkinter window
root = tk.Tk()
root.title("ZPC data scraper")
root.geometry("360x250+1540+0")  # Increase the window size
root.overrideredirect(True)  # Remove the window border
root.wm_attributes("-topmost", True)  # Make the window topmost
root.resizable(False, False)  # Disable window resizing

# Set the window and element colors to black
root.configure(background="black")
input_color = "white"
text_color = "white"
text_color_input = "black"

# Create a label above the input field with larger font size
input_label = tk.Label(root, text="Please input pair_tf", font=("Arial", 14), fg=text_color, bg="black")

# Create an entry widget for user input
pair_entry = tk.Entry(root, font=("Arial", 12), fg=text_color_input, bg=input_color)

# Create a label to display the list of .csv files
csv_label = tk.Label(root, text="No .csv files found", font=("Arial", 12), justify="left", fg="white", bg="black", anchor="center")

# Create a button to start the listening process
home_button = tk.Button(root, text="Start Listening", command=start_listening, fg=text_color_input, bg=input_color)

# Create a label to display the log messages with larger font size
log_text = tk.StringVar()
log_label = tk.Label(root, textvariable=log_text, font=("Arial", 14), justify="center", fg=text_color, bg="black")
hotkey_text = tk.StringVar()
hotkey_label = tk.Label(root, textvariable=hotkey_text, font=("Arial", 14), justify="center", fg=text_color, bg="black")

# Create an exit button
exit_button = tk.Button(root, text="Exit", command=exit_program, fg=text_color_input, bg=input_color)
# Position the exit button at the bottom right corner
exit_button.pack(side=tk.RIGHT, padx=10, pady=10, anchor=tk.SE)

# Pack the widgets
input_label.pack(pady=5, anchor="center")
input_label.place(x=95, y=10)
pair_entry.pack(pady=5, anchor="center")
pair_entry.place(x=85, y=50)
csv_label.pack(padx=5, pady=(0.5, 0.5), anchor="center")
csv_label.place(x=105, y=120)
home_button.pack(pady=6, anchor="center")
home_button.place(x=135, y=85)
log_label.pack(anchor="center")
log_label.place(x=35, y=10)
hotkey_label.place(x=75, y=10)

# Function to update the CSV file list
def update_csv_list():
    csv_files = [f for f in os.listdir('./zpc_csv') if f.endswith(".csv")]
    csv_label_text = "\n".join(csv_files) if csv_files else "No .csv files found"
    if csv_files:
        csv_label.configure(text="\n".join(csv_files))
    else:
        csv_label.configure(text="No .csv files found")

    # Calculate the required window height based on the number of lines in the CSV label
    line_height = 18  # Adjust as needed
    line_count = csv_label_text.count('\n') + 1
    required_height = line_height * line_count + 25

    # Update the window height based on the required height
    window_width = 360
    root.geometry(f"{window_width}x{required_height+120}+1540+0")

def check_csv_file(csv_file):
    file_exists = os.path.isfile(csv_file)
    with open(csv_file, 'w') as file:
        writer = csv.append(file)
        writer.append("\n")

def csv_create_file():
    file_exists = os.path.isfile(csv_file)
    if not file_exists:
        with open(csv_file, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['unix_time', 'zpc_presence', 'parsed_date', 'pair_tf'])

update_csv_list()

root.mainloop()