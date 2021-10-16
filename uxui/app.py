from tkinter import Tk, Frame
from functions import *

root = Tk()
root.title('PDF Extractor')
root.resizable(width=FALSE, height=FALSE)
root.geometry('%dx%d+%d+%d' % (800,610,200, 20))
root.configure(bg="red")

display_hdr(root, 'logo.png')
# main content area - text and image extraction
main_content = Frame(root, width=800, height=420, bg="#20bebe")
main_content.grid(rowspan=2, row=1, column=0, sticky=NSEW)
display_browse(root, main_content)

root.mainloop()
