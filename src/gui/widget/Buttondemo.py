import ttk
import Tkinter

root = Tkinter.Tk()

ttk.Style().configure("TButton", padding=6, relief="lowered",
   background="#ccc")

btn = ttk.Button(text="Sample")
btn.pack()

root.mainloop()
