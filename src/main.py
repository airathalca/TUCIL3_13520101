from grid4x4 import *
from time import perf_counter

#function to solve matrix after button Solve pressed
def solve():
    global iterationnumber
    global Puz
    global window
    tStart = perf_counter()
    if (not Puz.Valid()):
        text.delete("1.0","end")
        text.insert("1.0", "Input Tidak Valid")
        text.tag_add("tag_name", "1.0", "end")
    else:
        text.delete("1.0","end")
        for i in range(5):
            check = 3*i + 1
            text.insert(str(float(i+1)), f"Kurang({check})={Puz.Kurang(check)}  Kurang({check+1})={Puz.Kurang(check+1)}  Kurang({check+2})={Puz.Kurang(check+2)}\n")
        text.insert("6.0", f"Nilai dari sum_{1}^{16} kurang(i)+X adalah={Puz.KurangTotal()}\n")
        if (Puz.Cek()):
            solution, iterationnumber = SolvePuzzle(Puz, iterationnumber)
            tStop = perf_counter()
            text.insert("7.0", "Jumlah simpul yang dibangkitkan = " + str(iterationnumber) + "\nWaktu Eksekusi = " + str("{:.6f}".format(tStop-tStart)) + " sekon")
            text.tag_add("tag_name", "1.0", "end")
            grid.path(solution, window)
        else:
            text.insert("7.0", "Puzzle tidak dapat diselesaikan")
            text.tag_add("tag_name", "1.0", "end")

#function to open browser file
def select_file():
    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)
    Puz.readFile(filename)
    grid.change_button()

#function to read input from entry to matrix
def inputManual():
    Puz.inputCommand(entryofstate.get())
    grid.change_button()

#function to delete temporary text in entry
def temp_text(e):
   entryofstate.delete(0,"end")

def input_failed():
    text.delete("1.0","end")
    text.insert("1.0", "Gagal Membaca Input")
    text.tag_add("tag_name", "1.0", "end")

#create window
window = Tk()
Puz = Puzzle()
window.title("15-Puzzle Solver")
window.geometry("600x400")
window.configure(background='dark slate gray')

#create label for title
Label(text="BnB 15 Puzzle",bg = 'dark slate gray', fg = 'white', font = ("Comic Sans MS", "24")).pack()

#initialization
grid = gridFrame(window, Puz)
iterationnumber = 0

#create button for open file
open_button = Button(text='Open a File',fg = 'white', bg = 'slate gray', command=select_file)
open_button.place(x=300, y = 95)
open_button.config(width = 20)

#create text
label2 = Label(text='OR', bg = 'dark slate gray')
label2.config(font='helvetica 10 bold')
label2.place(x = 360, y= 125)

#create entry for manual input
entryofstate = Entry()
entryofstate.config(width = 24)
entryofstate.insert(0, "Input Here (ex: 1 2 3 16 etc.)")
entryofstate.bind("<FocusIn>", temp_text)
entryofstate.place(x = 300, y = 150)

#create confirm button for manual input
confirmbutton = Button(text = 'Confirm Manual', fg = 'white', bg = 'slate gray', command = inputManual)
confirmbutton.config(width = 20)
confirmbutton.place(x=300, y = 170)

#create solve button to solve 15 puzzle
solvebutton = Button(text = 'Solve', fg = 'white', bg = 'slate gray', command = solve)
solvebutton.config(width = 15, height = 6)
solvebutton.place(x=460, y = 95)

#create text for constraint etc.
text=Text(bg = 'dark slate gray', font = ("Comic Sans MS", "10"))
text.tag_configure("tag_name", justify='left')
text.config(width = 34, height = 8)
text.place(x=300, y = 210)

window.mainloop()