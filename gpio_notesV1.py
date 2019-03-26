#! /usr/bin/python3
from tkinter import messagebox
from tkinter import filedialog
from tkinter import *
from PIL import Image
import subprocess, os


root = Tk()
root.title('Raspberry Pi GPIO Notes')
root.resizable(0, 0)

# Layout spacing.
user = 30
pin_width = 3
info_width = 8
# Backgrounds.
gpio_bg = 'yellow'
gpio_12c_bg = 'grey'
gpio_i2c_bg = 'grey'
gpio_uart_bg = 'blue'
gpio_spi_bg = 'orange'
dnc_bg = 'green'
v_bg = 'red'
g_bg = 'black'
# Due to black background white text on GND pins.
g_fg = 'white'

# Screenshot.
default_save = StringVar()
curr_dir = os.getcwd()
default_save.set(curr_dir + '/gpio_shot.png')


gpio_pins = {1:['3.3v', v_bg], 2:['5v', v_bg],
             3:['GPIO 2', gpio_i2c_bg], 4:['5v', v_bg],
             5:['GPIO 3', gpio_i2c_bg], 6:['GND', g_bg],
             7:['GPIO 4', gpio_bg], 8:['GPIO 14', gpio_uart_bg],
             9:['GND', g_bg], 10:['GPIO 15', gpio_uart_bg],
             11:['GPIO 17', gpio_bg], 12:['GPIO 18', gpio_bg],
             13:['GPIO 27', gpio_bg], 14:['GND', g_bg],
             15:['GPIO 22', gpio_bg], 16:['GPIO 23', gpio_bg],
             17:['3.3v', v_bg], 18:['GPIO 24', gpio_bg],
             19:['GPIO 10', gpio_spi_bg], 20:['GND', g_bg],
             21:['GPIO 9', gpio_spi_bg], 22:['GPIO 25', gpio_bg],
             23:['GPIO 11', gpio_spi_bg], 24:['GPIO 8', gpio_spi_bg],
             25:['GND', g_bg], 26:['GPIO 7', gpio_spi_bg],
             27:['DNC', dnc_bg], 28:['DNC', dnc_bg],
             29:['GPIO 5', gpio_bg], 30:['GND', g_bg],
             31:['GPIO 6', gpio_bg], 32:['GPIO 12', gpio_bg],
             33:['GPIO 13', gpio_bg], 34:['GND', g_bg],
             35:['GPIO 19', gpio_bg], 36:['GPIO 16', gpio_bg],
             37:['GPIO 26', gpio_bg], 38:['GPIO 20', gpio_bg],
             39:['GND', g_bg], 40:['GPIO 21', gpio_bg]}

def layout():
    Label(root, text='NOTES').grid(row=0, column=0, pady=5)
    Label(root, text='BCM').grid(row=0, column=1, pady=5)
    Label(root, text='BOARD').grid(row=0, columnspan=6, pady=5)
    Label(root, text='BCM').grid(row=0, column=4, pady=5)
    Label(root, text='NOTES').grid(row=0, column=5, pady=5)
    for pins in gpio_pins:
        g = gpio_pins[pins][0]
        b = gpio_pins[pins][1]
        if pins % 2 == 0:
            Label(root, text=pins, width=pin_width, relief=RAISED).grid(row=pins - 1, column=3, padx=2)
            if b == g_bg:
                Label(root, text=g, bg=b, fg=g_fg, width=info_width, relief=RAISED).grid(row=pins - 1, column=4, padx=2)
            else:
                Label(root, text=g, bg=b, width=info_width, relief=RAISED).grid(row=pins - 1, column=4, padx=2)
            data = Entry(root, width=user).grid(row=pins - 1, column=5, padx=2)
        else:
            data = Entry(root, width=user).grid(row=pins, column=0, padx=2)
            if b == g_bg:
                Label(root, text=g, bg=b, fg=g_fg, width=info_width, relief=RAISED).grid(row=pins, column=1, padx=2)
            else:
                Label(root, text=g, bg=b, width=info_width, relief=RAISED).grid(row=pins, column=1, padx=2)
            Label(root, text=pins, width=pin_width, relief=RAISED).grid(row=pins, column=2, padx=2)
    Button(root, text='!!! CLEAR ALL NOTES !!!', bg='yellow', fg='red', width=50, command=layout).grid(row=41, columnspan=6, pady=10)
    Label(root, text='SAVE SHOT TO:').grid(row=42, column=0, padx=2)
    Entry(root, textvariable=default_save, width=45).grid(row=42, columnspan=6)
    save_scrn = Button(root, text='SAVE SCREENSHOT', bg='yellow', fg='red', width=50, command=scrnshot).grid(row=43, columnspan=6, pady=10)

def scrnshot():
    save_file = default_save.get()
    if os.path.isfile(save_file) == False:
        if save_file.startswith('/home/pi/') and save_file.endswith('.png' or '.jpg' or '.bmp') and len(save_file) >= 14:
            subprocess.call('scrot {} -u'.format(save_file), shell=True)
            img = Image.open(save_file)
            area = (0, 0, 708, 435)
            cropped_img = img.crop(area)
            cropped_img.save(save_file)
            print(len(save_file))
            if os.path.isfile(save_file):
                messagebox.showinfo('Information', save_file + ' saved.')
            else:
                messagebox.showinfo('!! Warning !!.', save_file + ' failed to be saved, check you have entered the correct file path and try again.')
        else:
            messagebox.showinfo('!! WARNING !!', 'Save file needs to be at least /home/pi/ and using *.png, *.jpg, *.bmp file extensions.')
            print(len(save_file))
    elif save_file.startswith('/home/pi/') and len(save_file) == 13:
        messagebox.showinfo('!! WARNING !!', 'File name missing, check and retry.')
        print(len(save_file))
    else:
        messagebox.showinfo('!! WARNING !!', 'File exists already, check and retry.')
        print(len(save_file))

layout()
root.mainloop()
