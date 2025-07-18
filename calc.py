from tkinter import *
from tkinter import ttk
from math import sin, cos, tan, log, radians, pi, sqrt
root = Tk()
ans = 'Error'
fr_style = ttk.Style(root)
fr_style.theme_use('clam')
fr_style.configure(
    'Base.TFrame',
    # width=750,
    # height=550,
    borderwidth=2,
    bordercolor='grey',
    relief='raised',
)

input_style = ttk.Style()
input_style.configure(
    'Input.TButton',
    font=('Comic Sans MS', 15),
    foreground='#2c2c29',
    background='#e9de8b',
    borderwidth=5,
    bordercolor='grey',
    width=5,
    relief='raised',
    height=16
)
entry_style = ttk.Style()
entry_style.configure(
    'Entry.TEntry',
    fieldbackground='#grey',  # Change the background color here
    bordercolor='#grey',         # Change the border color here
    borderwidth=0,
    font=('Constantia', 18)
)

def press_input(val):
    entry.insert('end', val)
    
def delete():
    l = len(entry.get()) - 1
    entry.delete(l, 'end')

def clear():
    entry.delete(0, 'end')
    
    
    
#Maths functions
def xsin(num):
    return(sin(radians(num)))

def xcos(num):
    return(cos(radians(num)))

def xtan(num):
    return (tan(radians(num)))

def xlog(num):
    return log(num, 10)

#Parsing

def parse(string):
    change = {
        'x': "*", 'sin': 'xsin', 'cos': 'xcos', 'tan': 'xtan',
        'log': 'xlog', '÷': '/', '√': 'sqrt', 'π': str(pi), 'ans': ans,
        '^': '**'
    }
    for k, v in change.items():
        string = string.replace(k, v)
    x = None
    try:
        x = str(eval(string))
    except Exception as e:
        print(string)
        print(e)
        x = 'Error'
    finally:
        return x

def equal_to():
    global entry, ans
    val = entry.get()
    result = parse(val)
    ans = result if result != 'Error' else ans
    clear()
    entry.insert(0, result)

def gen_buttons(parent):
    ttk.Button(parent, text='1', style='Input.TButton', command= lambda : press_input('1')).grid(row=1, column=1)
    ttk.Button(parent, text='2', style='Input.TButton', command= lambda : press_input('2')).grid(row=1, column=2)
    ttk.Button(parent, text='3', style='Input.TButton', command= lambda : press_input('3')).grid(row=1, column=3)
    ttk.Button(parent, text='4', style='Input.TButton', command= lambda : press_input('4')).grid(row=2, column=1)
    ttk.Button(parent, text='5', style='Input.TButton', command= lambda : press_input('5')).grid(row=2, column=2)
    ttk.Button(parent, text='6', style='Input.TButton', command= lambda : press_input('6')).grid(row=2, column=3)
    ttk.Button(parent, text='7', style='Input.TButton', command= lambda : press_input('7')).grid(row=3, column=1)
    ttk.Button(parent, text='8', style='Input.TButton', command= lambda : press_input('8')).grid(row=3, column=2)
    ttk.Button(parent, text='9', style='Input.TButton', command= lambda : press_input('9')).grid(row=3, column=3)

    ttk.Button(parent, text='+', style='Input.TButton', command= lambda : press_input(' + ')).grid(row=0, column=4)
    ttk.Button(parent, text='-', style='Input.TButton', command= lambda : press_input(' - ')).grid(row=1, column=4)
    ttk.Button(parent, text='x', style='Input.TButton', command= lambda : press_input(' x ')).grid(row=2, column=4)
    ttk.Button(parent, text='÷', style='Input.TButton', command= lambda : press_input(' ÷ ')).grid(row=3, column=4)
 
    ttk.Button(parent, text='sin', style='Input.TButton', command= lambda : press_input('sin(')).grid(row=0, column=0)
    ttk.Button(parent, text='cos', style='Input.TButton', command= lambda : press_input('cos(')).grid(row=1, column=0)
    ttk.Button(parent, text='tan', style='Input.TButton', command= lambda : press_input('tan(')).grid(row=2, column=0)
    ttk.Button(parent, text='log', style='Input.TButton', command= lambda : press_input('log(')).grid(row=3, column=0)

    ttk.Button(parent, text='√', style='Input.TButton', command= lambda : press_input('√(')).grid(row=0, column=1)
    ttk.Button(parent, text='π', style='Input.TButton', command= lambda : press_input('π')).grid(row=0, column=2)
    ttk.Button(parent, text='^', style='Input.TButton', command= lambda : press_input('^(')).grid(row=0, column=3)

    ttk.Button(parent, text='(', style='Input.TButton', command= lambda : press_input('(')).grid(row=5, column=0)
    ttk.Button(parent, text=')', style='Input.TButton', command= lambda : press_input(')')).grid(row=5, column=1)
    ttk.Button(parent, text='0', style='Input.TButton', command= lambda : press_input('0')).grid(row=5, column=2)
    ttk.Button(parent, text='.', style='Input.TButton', command= lambda : press_input('.')).grid(row=5, column=3)
    ttk.Button(parent, text='ans', style='Input.TButton', command= lambda : press_input('ans')).grid(row=5, column=4)

    ttk.Button(parent, text='del', style='Input.TButton', command=delete).grid(row=0, column=5)
    ttk.Button(parent, text='CE', style='Input.TButton', command=clear).grid(row=1, column=5)
    ttk.Button(parent, text='=', style='Input.TButton', command=equal_to).grid(row=2, column=5, sticky='nsew', rowspan=4)



root.geometry('800x600')
root.resizable(False, False)
root.title('My Calc')
base = ttk.Frame(root, style='Base.TFrame')
base.pack(anchor='center', ipady=15,)
title = ttk.Label(base, font=('Parchment', 28), text='My Calculator', foreground='#105bcc')
title.pack(anchor='w')
entry = ttk.Entry(base, width=40, font=('Constantia', 18), style="Entry.TEntry", justify='right')
entry.pack(anchor='e', pady=30)
buttonpad = ttk.Frame(base, width=600, height=400, relief='solid')
buttonpad.pack(anchor='center')
buttonpad.columnconfigure(6)
buttonpad.rowconfigure(5)
gen_buttons(buttonpad)

print(5 ** 3)
root.mainloop()
