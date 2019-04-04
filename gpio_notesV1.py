#! /usr/bin/python3
import subprocess, csv, sys, os
from tkinter import messagebox
from tkinter import filedialog
import tkinter.font as font
from tkinter import *
from PIL import Image

root = Tk()
root.title('Raspberry Pi GPIO Notes')
root.resizable(0, 0)
font.nametofont('TkDefaultFont').configure(size=11)

# data entries
data_list = []
d1 = StringVar(); d2 = StringVar(); d3 = StringVar(); d4 = StringVar(); d5 = StringVar()
d6 = StringVar(); d7 = StringVar(); d8 = StringVar(); d9 = StringVar(); d10 = StringVar()
d11 = StringVar(); d12 = StringVar(); d13 = StringVar(); d14 = StringVar(); d15 = StringVar()
d16 = StringVar(); d17 = StringVar(); d18 = StringVar(); d19 = StringVar(); d20 = StringVar()
d21 = StringVar(); d22 = StringVar(); d23 = StringVar(); d24 = StringVar(); d25 = StringVar()
d26 = StringVar(); d27 = StringVar(); d28 = StringVar(); d29 = StringVar(); d30 = StringVar()
d31 = StringVar(); d32 = StringVar(); d33 = StringVar(); d34 = StringVar(); d35 = StringVar()
d36 = StringVar(); d37 = StringVar(); d38 = StringVar(); d39 = StringVar(); d40 = StringVar()

# Layout spacing.
user = 35
pin_width = 3
info_width = 11

# Backgrounds.
gpio_bg = 'yellow'
gpio_i2c_bg = 'grey'
gpio_uart_bg = 'blue'
gpio_spi_bg = 'orange'
dnc_bg = 'green'
v_bg = 'red'
g_bg = 'black'
g_fg = 'white'

gpio_pins = {1:['3.3Volts', v_bg, d1], 2:['5Volts', v_bg, d2],
             3:['GPIO2/SDA', gpio_i2c_bg, d3], 4:['5Volts', v_bg, d4],
             5:['GPIO3/SCL', gpio_i2c_bg, d5], 6:['GND/0V', g_bg, d6],
             7:['GPIO4', gpio_bg, d7], 8:['GPIO14/TXD', gpio_uart_bg, d8],
             9:['GND/0V', g_bg, d9], 10:['GPIO15/RXD', gpio_uart_bg, d10],
             11:['GPIO17', gpio_bg, d11], 12:['GPIO18', gpio_bg, d12],
             13:['GPIO27', gpio_bg, d13], 14:['GND/0V', g_bg, d14],
             15:['GPIO22', gpio_bg, d15], 16:['GPIO23', gpio_bg, d16],
             17:['3.3Volts', v_bg, d17], 18:['GPIO24', gpio_bg, d18],
             19:['GPIO10/MOSI', gpio_spi_bg, d19], 20:['GND/0V', g_bg, d20],
             21:['GPIO9/MISO', gpio_spi_bg, d21], 22:['GPIO25', gpio_bg, d22],
             23:['GPIO11/SCLK', gpio_spi_bg, d23], 24:['GPIO8/CE0', gpio_spi_bg, d24],
             25:['GND/0V', g_bg, d25], 26:['GPIO7/CE1', gpio_spi_bg, d26],
             27:['DNC/ID_SD', dnc_bg, d27], 28:['DNC/ID_SC', dnc_bg, d28],
             29:['GPIO5', gpio_bg, d29], 30:['GND/0V', g_bg, d30],
             31:['GPIO6', gpio_bg, d31], 32:['GPIO12', gpio_bg, d32],
             33:['GPIO13', gpio_bg, d33], 34:['GND/0V', g_bg, d34],
             35:['GPIO19', gpio_bg, d35], 36:['GPIO16', gpio_bg, d36],
             37:['GPIO26', gpio_bg, d37], 38:['GPIO20', gpio_bg, d38],
             39:['GND/0V', g_bg, d39], 40:['GPIO21', gpio_bg, d40]}

def layout():
    Label(root, text='POWER', width=8, bg=v_bg).grid(row=0, column=0, columnspan=2, pady=5)
    Label(root, text='GROUND', width=8, bg=g_bg, fg=g_fg).grid(row=0, column=0, columnspan=2, sticky=NE, pady=5)
    Label(root, text='GPIO', width=8, bg=gpio_bg).grid(row=0, column=2, pady=5)
    Label(root, text='I2C', width=8, bg=gpio_i2c_bg).grid(row=0, columnspan=8, pady=5)
    Label(root, text='UART', width=8, bg=gpio_uart_bg).grid(row=0, column=5, pady=5)
    Label(root, text='SPI', width=8, bg=gpio_spi_bg).grid(row=0, column=6, columnspan=2, sticky=NW, pady=5)
    Label(root, text='EEPROM', width=8, bg=dnc_bg).grid(row=0, column=6, columnspan=2, pady=5)
    Label(root, text='NOTES', fg='red').grid(row=1, column=0, columnspan=2, pady=5)
    Label(root, text='BCM', fg='red').grid(row=1, column=2, pady=5)
    Label(root, text='BOARD PINS', fg='red').grid(row=1, columnspan=8, pady=5)
    Label(root, text='BCM', fg='red').grid(row=1, column=5, pady=5)
    Label(root, text='NOTES', fg='red').grid(row=1, column=6, columnspan=2, pady=5)
    for pins in gpio_pins:
        g = gpio_pins[pins][0]
        b = gpio_pins[pins][1]
        d = gpio_pins[pins][2]
        if pins % 2 == 0:
            Label(root, text=pins, width=pin_width, relief=RAISED).grid(row=pins, column=4, sticky=E, padx=6, pady=1)
            if b == g_bg:
                Label(root, text=g, bg=b, fg=g_fg, width=info_width, relief=RAISED).grid(row=pins, column=5, padx=6, pady=1)
            else:
                Label(root, text=g, bg=b, width=info_width, relief=RAISED).grid(row=pins, column=5, padx=6, pady=1)
            data = Entry(root, textvariable=d, width=user).grid(row=pins, column=6, columnspan=2, padx=6, pady=1)
        else:
            data = Entry(root, textvariable=d, width=user).grid(row=pins + 1, column=0, columnspan=2, padx=6, pady=1)
            if b == g_bg:
                Label(root, text=g, bg=b, fg=g_fg, width=info_width, relief=RAISED).grid(row=pins + 1, column=2, padx=6, pady=1)
            else:
                Label(root, text=g, bg=b, width=info_width, relief=RAISED).grid(row=pins + 1, column=2, padx=6, pady=1)
            Label(root, text=pins, width=pin_width, relief=RAISED).grid(row=pins + 1, column=3, padx=6, pady=1)
    Button(root, text='!!! CLEAR ALL NOTES !!!', fg='red', width=30, command=clearMyData).grid(row=42, column=1, columnspan=2, pady=10)
    Button(root, text='LOAD PROJECT', fg='red', width=30, command=grabMyFileData).grid(row=42, column=5, columnspan=2, pady=10)
    Button(root, text='SCREENSHOT', fg='red', width=30, command=grabMyShot).grid(row=43, column=1, columnspan=2, pady=5)
    Button(root, text='SAVE PROJECT', fg='red', width=30, command=grabMyData).grid(row=43, column=5, columnspan=2, pady=5)

def grabMyData():
    data_list.clear()
    data_list.append([d1.get()]); data_list.append([d2.get()]); data_list.append([d3.get()])
    data_list.append([d4.get()]); data_list.append([d5.get()]); data_list.append([d6.get()])
    data_list.append([d7.get()]); data_list.append([d8.get()]); data_list.append([d9.get()])
    data_list.append([d10.get()]); data_list.append([d11.get()]); data_list.append([d12.get()])
    data_list.append([d13.get()]); data_list.append([d14.get()]); data_list.append([d15.get()])
    data_list.append([d16.get()]); data_list.append([d17.get()]); data_list.append([d18.get()])
    data_list.append([d19.get()]); data_list.append([d20.get()]); data_list.append([d21.get()])
    data_list.append([d22.get()]); data_list.append([d23.get()]); data_list.append([d24.get()])
    data_list.append([d25.get()]); data_list.append([d26.get()]); data_list.append([d27.get()])
    data_list.append([d28.get()]); data_list.append([d29.get()]); data_list.append([d30.get()])
    data_list.append([d31.get()]); data_list.append([d32.get()]); data_list.append([d33.get()])
    data_list.append([d34.get()]); data_list.append([d35.get()]); data_list.append([d36.get()])
    data_list.append([d37.get()]); data_list.append([d38.get()]); data_list.append([d39.get()])
    data_list.append([d40.get()])
    saveMyData()

def insertMyData():
    d1.set(data_list[0]); d2.set(data_list[1]); d3.set(data_list[2]); d4.set(data_list[3])
    d5.set(data_list[4]); d6.set(data_list[5]); d7.set(data_list[6]); d8.set(data_list[7])
    d9.set(data_list[8]); d10.set(data_list[9]); d11.set(data_list[10]); d12.set(data_list[11])
    d13.set(data_list[12]); d14.set(data_list[13]); d15.set(data_list[14]); d16.set(data_list[15])
    d17.set(data_list[16]); d18.set(data_list[17]); d19.set(data_list[18]); d20.set(data_list[19])
    d21.set(data_list[20]); d22.set(data_list[21]); d23.set(data_list[22]); d24.set(data_list[23])
    d25.set(data_list[24]); d26.set(data_list[25]); d27.set(data_list[26]); d28.set(data_list[27])
    d29.set(data_list[28]); d30.set(data_list[29]); d31.set(data_list[30]); d32.set(data_list[31])
    d33.set(data_list[32]); d34.set(data_list[33]); d35.set(data_list[34]); d36.set(data_list[35])
    d37.set(data_list[36]); d38.set(data_list[37]); d39.set(data_list[38]); d40.set(data_list[39])

def clearMyData():
    d1.set(''); d2.set(''); d3.set(''); d4.set(''); d5.set(''); d6.set(''); d7.set(''); d8.set('')
    d9.set(''); d10.set(''); d11.set(''); d12.set(''); d13.set(''); d14.set(''); d15.set(''); d16.set('')
    d17.set(''); d18.set(''); d19.set(''); d20.set(''); d21.set(''); d22.set(''); d23.set(''); d24.set('')
    d25.set(''); d26.set(''); d27.set(''); d28.set(''); d29.set(''); d30.set(''); d31.set(''); d32.set('')
    d33.set(''); d34.set(''); d35.set(''); d36.set(''); d37.set(''); d38.set(''); d39.set(''); d40.set('')

def saveMyData():
    try:
        save_as = filedialog.asksaveasfile(parent=root, initialdir='/home/pi/',
                                           title = 'Save project file',
                                           filetypes=(('GPIO Notes file format','*.csv'),))
        if not save_as:
            messagebox.showinfo('Information', 'No file specified, cancelled.')
        else:
            os.chdir('/')
            write_data_file(save_as.name, data_list)
            messagebox.showinfo('Information', save_as.name + ' saved.')
    except:
        messagebox.showinfo('!!! Warning !!!', 'Error, data not saved.')

def grabMyFileData():
    try:
        clearMyData()
        data_list.clear()
        open_as = filedialog.askopenfile(parent=root, initialdir='/home/pi/',
                                           title = 'Open project file',
                                           filetypes=(('GPIO Notes file format','*.csv'),))
        if not open_as:
            messagebox.showinfo('Information', 'No file specified, cancelled.')
        else:
            os.chdir('/')
            read_data_file(open_as.name, data_list)
            insertMyData()
    except:
        messagebox.showinfo('!!! Warning !!!', 'Error, data not loaded.')

def read_data_file(file, temp):
    try:
        with open(file, 'r') as project_data:
            data = csv.reader(project_data)
            for line in data:
                if len(line) == 0:
                    temp.append('')
                else:
                    temp.append(str(line).replace("['","").replace("']", "").replace('["', '').replace('"]', ''))
        project_data.close()
        return temp
    except:
        messagebox.showinfo('!!! Warning !!!', 'Error, unable to read data file.')

def write_data_file(file, temp):
    try:
        with open(file, 'w+', newline='') as project_data:
            pdd = csv.writer(project_data)
            pdd.writerows(temp)
        project_data.close()
    except:
        messagebox.showinfo('!!! Warning !!!', 'Error, unable to write data.')

def grabMyShot():
    try:
        temp_file = 'Just1SuperQuickPicB4DEL.png' # relax this temp file will be deleted.
        subprocess.call('sudo scrot {} -u'.format(temp_file), shell=True)
        save_as = filedialog.asksaveasfile(mode='w',
                                           parent=root,
                                           initialdir='/home/pi/',
                                           title = 'Save screenshot',
                                           filetypes=(('PNG','*.png'),('JPG','*.jpg')))
        if not save_as:
            messagebox.showinfo('Information', 'No file specified, cancelled.')
        else:
            img = Image.open(temp_file)
            area = (0, 0, 940, 550)
            cropped_img = img.crop(area)
            cropped_img.save(save_as.name)
            subprocess.call('sudo rm {}'.format(temp_file), shell=True) # temp file now deleted.
            messagebox.showinfo('Information', save_as.name + ' saved, please check your picture before closing or clearing window.')
    except:
        messagebox.showinfo('!!! Warning !!!', 'Error, data not saved.')

try:
    layout()
    root.mainloop()
except:
    sys.exit()
