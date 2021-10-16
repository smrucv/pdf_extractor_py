from tkinter import *
from tkmacosx import Button
import PyPDF2
from PIL import ImageTk
from tkinter.filedialog import askopenfile
from functions import *

page_contents = []
all_images = []
img_idx =[0]
displayed_img = []


def right_arrow(all_images, current_img, what_text):
    if img_idx[-1] < len(all_images) -1:
        new_idx = img_idx[-1] + 1
        img_idx.pop()
        img_idx.append(new_idx)
        if displayed_img:
            displayed_img[-1].grid_forget()
            displayed_img.pop()
        new_img = all_images[img_idx[-1]]
        current_img = display_images(new_img)
        displayed_img.append(current_img)
        what_text.set("Image " + str(img_idx[-1] + 1) + " out of " + str(len(all_images)))


def left_arrow(all_images, current_img, what_text):
    if img_idx[-1] > 0:
        new_idx = img_idx[-1] - 1
        img_idx.pop()
        img_idx.append(new_idx)
        if displayed_img:
            displayed_img[-1].grid_forget()
            displayed_img.pop()
        new_img = all_images[img_idx[-1]]
        current_img = display_images(new_img)
        displayed_img.append(current_img)
        what_text.set("Image " + str(img_idx[-1] + 1) + " out of " + str(len(all_images)))


def copy_text(content):
    root.clipboard_clear()
    root.clipboard_append(content[-1])


def save_all(images):
    counter = 1
    for i in images:
        if i.mode != "RGB":
            i = i.convert("RGB")
        i.save("img" + str(counter) + ".png", format="png")
        counter += 1


def save_image(img):
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save("img.png", format="png")


root = Tk()
root.geometry('+%d+%d' % (350, 10))  # place GUI at x=350, y=10

# header area - logo & browse button
header = Frame(root, width=800, height=175, bg="white")
header.grid(columnspan=3, rowspan=2, row=0)

# main content area - text and image extraction
main_content = Frame(root, width=800, height=250, bg="#20bebe")
main_content.grid(columnspan=3, rowspan=2, row=4)


def open_file():

    for i in img_idx:
        img_idx.pop()
    img_idx.append(0)

    browse_text.set("loading...")
    file = askopenfile(parent=root, mode='rb', filetypes=[("Pdf file", "*.pdf")])
    if file:
        read_pdf = PyPDF2.PdfFileReader(file)
        page = read_pdf.getPage(0)
        page_content = page.extractText()
        # page_content = page_content.encode('cp1252')
        page_content = page_content.replace('\u2122', "'")
        page_contents.append(page_content)

        if displayed_img:
            displayed_img[-1].grid_forget()
            displayed_img.pop()

        for i in range(0, len(all_images)):
            all_images.pop()

        images = extract_images(page)

        for i in images:
            all_images.append(i)

        img = images[img_idx[-1]]

        current_image =  display_images(img)
        displayed_img.append(current_image)

        # show text box on row 4 col 0
        display_textbox(page_content, 4, 0, root)

        # reset the button text back to Browse
        browse_text.set("Browse")

        # image area - image scroll
        img_menu = Frame(root, width=800, height=60)
        img_menu.grid(columnspan=3, rowspan=1, row=2)

        what_text = StringVar()
        what_img = Label(root, textvariable=what_text, font=("shanti", 10))
        what_text.set("Image " + str(img_idx[-1] + 1) + " out of " + str(len(all_images)))
        what_img.grid(row=2, column=1)

        display_icon("arrow_l.png", 2, 0, E, lambda: left_arrow(all_images, current_image, what_text))
        display_icon("arrow_r.png", 2, 2, W, lambda: right_arrow(all_images, current_image, what_text))

        # save area - buttons bar
        save_img = Frame(root, width=800, height=60, bg="#c8c8c8")
        save_img.grid(columnspan=3, rowspan=1, row=3)

        copyText_btn = Button(root, text="Copy Text", command=lambda:copy_text(page_contents), font=("shanti", 10), padx=20, pady=10)
        saveAll_btn = Button(root, text="Save All Images", command=lambda:save_all(all_images), font=("shanti", 10), padx=20, pady=10)
        save_btn = Button(root, text="Save Image", command=lambda:save_image(all_images[img_idx[-1]]), font=("shanti", 10), padx=20, pady=10)

        copyText_btn.grid(row=3, column=0)
        saveAll_btn.grid(row=3, column=1)
        save_btn.grid(row=3, column=2)


display_logo('logo.png', 0, 0)

# instructions
instructions = Label(root, text="Select a PDF file", font=("Raleway", 10), bg="white")
instructions.grid(column=2, row=0, sticky=SE, padx=75, pady=5)

# browse button
browse_text = StringVar()
browse_btn = Button(root, textvariable=browse_text, command=lambda: open_file(), font=("Raleway", 12),
                       bg="#20bebe", fg="white", padx=20, pady=10)
browse_text.set("Browse")
browse_btn.grid(column=2, row=1, sticky=NE, padx=50)

root.mainloop()
