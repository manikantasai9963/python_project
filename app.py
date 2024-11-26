from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror, askyesno
from tkinter import filedialog as fd
import qrcode
import cv2
from PIL import ImageTk, Image


# Function to open the QR Code Generator-Detector window after login
def open_main_window():
    # Close the login window
    login_window.destroy()

    # Create the main window
    window = Tk()
    window.title('QR Code Generator-Detector')

    # Set dimensions and position of the window
    window.geometry('500x480+440+180')
    window.resizable(height=False, width=False)
    window.configure(bg='#e0e0e0')  # Light gray background for the window

    """Styles for the widgets, labels, entries, and buttons"""
    # Consistent style for all labels
    label_style = ttk.Style()
    label_style.configure('TLabel', foreground='#000000', font=('Arial', 12, 'bold'))

    # Consistent style for all entries
    entry_style = ttk.Style()
    entry_style.configure('TEntry', font=('Arial', 14), foreground='#000000')

    # Consistent style for all buttons (White background, Black text, uniform border thickness)
    button_style = ttk.Style()
    button_style.configure('TButton', foreground='#000000', background='#ffffff', font=('Arial', 12, 'bold'),
                           borderwidth=2, relief='raised')
    button_style.map('TButton', background=[('active', '#f0f0f0')])  # Slightly darker when active

    # Creating the Notebook widget
    tab_control = ttk.Notebook(window)
    first_tab = ttk.Frame(tab_control)
    second_tab = ttk.Frame(tab_control)

    # Adding the two tabs to the Notebook
    tab_control.add(first_tab, text='QR Code Generator')
    tab_control.add(second_tab, text='QR Code Detector')
    tab_control.pack(expand=1, fill="both")

    # Creating canvases for the tabs
    first_canvas = Canvas(first_tab, width=500, height=480, bg='#e0e0e0', highlightthickness=0)
    second_canvas = Canvas(second_tab, width=500, height=480, bg='#e0e0e0', highlightthickness=0)
    first_canvas.pack()
    second_canvas.pack()

    # Load background image from the specified path
    background_image = Image.open("C:/Users/HP/OneDrive/Pictures/Screenshots/Screenshot 2024-11-05 114422.png").resize(
        (500, 480), Image.LANCZOS)

    bg_img = ImageTk.PhotoImage(background_image)
    first_canvas.create_image(0, 0, anchor=NW, image=bg_img)
    second_canvas.create_image(0, 0, anchor=NW, image=bg_img)

    """Widgets for the first tab"""
    image_label1 = Label(first_tab, bg='#e0e0e0')
    first_canvas.create_window(250, 150, window=image_label1)

    qrdata_label = ttk.Label(first_tab, text='QR Code Data', style='TLabel')
    data_entry = ttk.Entry(first_tab, width=40, style='TEntry')
    first_canvas.create_window(250, 280, window=qrdata_label)
    first_canvas.create_window(250, 310, window=data_entry)

    filename_label = ttk.Label(first_tab, text='Filename', style='TLabel')
    filename_entry = ttk.Entry(first_tab, width=40, style='TEntry')
    first_canvas.create_window(250, 340, window=filename_label)
    first_canvas.create_window(250, 370, window=filename_entry)

    # Ensure Reset button is styled correctly, even when initially disabled
    reset_button = ttk.Button(first_tab, text='Reset', style='TButton', state=DISABLED)
    generate_button = ttk.Button(first_tab, text='Generate QR Code', style='TButton')
    first_canvas.create_window(150, 410, window=reset_button)
    first_canvas.create_window(350, 410, window=generate_button)

    """Widgets for the second tab"""
    image_label2 = Label(second_tab, bg='#e0e0e0')
    data_label = ttk.Label(second_tab, style='TLabel')
    second_canvas.create_window(250, 150, window=image_label2)
    second_canvas.create_window(250, 300, window=data_label)

    file_entry = ttk.Entry(second_tab, width=40, style='TEntry')
    browse_button = ttk.Button(second_tab, text='Browse', style='TButton')
    second_canvas.create_window(200, 350, window=file_entry)
    second_canvas.create_window(430, 350, window=browse_button)

    detect_button = ttk.Button(second_tab, text='Detect QR Code', style='TButton')
    second_canvas.create_window(250, 410, window=detect_button)

    # Function to close the window
    def close_window():
        if askyesno(title='Close QR Code Generator-Detector', message='Are you sure you want to close the application?'):
            window.destroy()

    window.protocol('WM_DELETE_WINDOW', close_window)

    # Function for generating the QR Code
    def generate_qrcode():
        qrcode_data = data_entry.get()
        qrcode_name = filename_entry.get()

        if qrcode_name == '':
            showerror(title='Error', message='Filename cannot be empty.')
        else:
            if askyesno(title='Confirmation', message=f'Do you want to create a QR Code with the provided information?'):
                try:
                    qr = qrcode.QRCode(version=1, box_size=6, border=4)
                    qr.add_data(qrcode_data)
                    qr.make(fit=True)
                    name = qrcode_name + '.png'
                    qrcode_image = qr.make_image(fill_color='black', back_color='white')
                    qrcode_image.save(name)

                    # Loading image in Tkinter-compatible format
                    img = ImageTk.PhotoImage(Image.open(name))  # No global variable
                    image_label1.config(image=img)
                    image_label1.image = img  # Keep a reference to the image

                    # Enable reset button after QR code is generated
                    reset_button.config(state=NORMAL)
                except Exception as e:
                    showerror(title='Error', message=f'An error occurred while generating QR code.\nError: {e}')

    generate_button.config(command=generate_qrcode)

    # Function for resetting or clearing the image label
    def reset():
        if askyesno(title='Reset', message='Are you sure you want to reset?'):
            image_label1.config(image='')
            reset_button.config(state=DISABLED)
            data_entry.delete(0, END)
            filename_entry.delete(0, END)

    reset_button.config(command=reset)

    # Function to open file dialogs
    def open_dialog():
        name = fd.askopenfilename()
        file_entry.delete(0, END)
        file_entry.insert(0, name)

    browse_button.config(command=open_dialog)

    # Function to detect the QR codes
    def detect_qrcode():
        image_file = file_entry.get()
        if image_file == '':
            showerror(title='Error', message='Please provide a QR Code image file to detect')
        else:
            try:
                qrcode_img = cv2.imread(image_file)
                detector = cv2.QRCodeDetector()
                data, bbox, _ = detector.detectAndDecode(qrcode_img)

                if data:
                    data_label.config(text=f'Detected QR Code Data:\n{data}')

                    img2 = ImageTk.PhotoImage(Image.open(image_file))  # No global variable
                    image_label2.config(image=img2)
                    image_label2.image = img2  # Keep a reference to the image
                else:
                    showerror(title='Error', message='No QR code found in the image.')
            except Exception as e:
                showerror(title='Error', message=f'An error occurred while detecting QR code.\nError: {e}')

    detect_button.config(command=detect_qrcode)

    # Start the Tkinter event loop
    window.mainloop()


# Create login window
login_window = Tk()
login_window.title("Login")
login_window.geometry('300x200+500+250')

# Username and Password Labels and Entries
username_label = Label(login_window, text="Username")
username_label.pack(pady=10)
username_entry = Entry(login_window)
username_entry.pack()

password_label = Label(login_window, text="Password")
password_label.pack(pady=10)
password_entry = Entry(login_window, show='*')
password_entry.pack()

# Login button function
def login():
    # Allow any username/password to pass
    open_main_window()

login_button = Button(login_window, text="Login", command=login)
login_button.pack(pady=20)

# Start the Tkinter event loop for the login window
login_window.mainloop()
