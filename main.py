import tkinter
import tkmacosx
import PyPDF2
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile


def open_file():
    browse_text.set('Loading...')
    file = askopenfile(parent=root, mode="rb", title="Pick a File", filetypes=[("Pdf file", "*.pdf")])
    if file:
        read_pdf = PyPDF2.PdfFileReader(file)
        page_content = ""
        for page in read_pdf.pages:
            page_content += page.extractText()

        # Text Box
        text_box = tkinter.Text(root, height=10, width=50, padx=15, pady=15)
        text_box.insert(1.0, page_content)
        text_box.tag_configure("center", justify="left")
        text_box.tag_add("center", 1.0, "end")
        text_box.grid(column=1, row=3)
    browse_text.set('Browse')


if __name__ == '__main__':
    root = tkinter.Tk()

    canvas = tkinter.Canvas(root, width=600, height=300)
    canvas.grid(columnspan=3, rowspan=3)

    # Logo
    logo = Image.open('logo.png')
    logo = ImageTk.PhotoImage(logo)
    logo_label = tkinter.Label(image=logo)
    logo_label.image = logo
    logo_label.grid(column=1, row=0)

    # Instructions
    instructions = tkinter.Label(root, text='Select a PDF file on your computer please.', font="ElliotSix")
    instructions.grid(columnspan=3, column=0, row=1)

    # Browse Button
    browse_text = tkinter.StringVar()
    browse_btn = tkmacosx.Button(root, textvariable=browse_text, command=lambda: open_file(),
                                 font='ElliotSix', bg='#20bebe', fg='white', padx=20, pady=10)  # height=2, width=15)
    browse_text.set('Browse')
    browse_btn.grid(column=1, row=2)

    canvas = tkinter.Canvas(root, width=600, height=250)
    canvas.grid(columnspan=3)

    root.mainloop()
