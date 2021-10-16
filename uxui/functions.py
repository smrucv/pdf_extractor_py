from tkinter import *
from tkmacosx import Button
from PIL import Image, ImageTk
import PyPDF2
from tkinter.filedialog import askopenfile


page_contents = []
all_images = []
img_idx = [0]
displayed_img = []
browse_text = ""
num_pages = 0
current_page = 0


def right_arrow(frame, all_images, current_img, what_text):
    if img_idx[-1] < len(all_images) - 1:
        new_idx = img_idx[-1] + 1
        img_idx.pop()
        img_idx.append(new_idx)
        if displayed_img:
            displayed_img[-1].grid_forget()
            displayed_img.pop()
        new_img = all_images[img_idx[-1]]
        current_img = display_images(frame, new_img)
        displayed_img.append(current_img)
        what_text.set("Image " + str(img_idx[-1] + 1) + " out of " + str(len(all_images)))


def left_arrow(frame, all_images, current_img, what_text):
    if img_idx[-1] > 0:
        new_idx = img_idx[-1] - 1
        img_idx.pop()
        img_idx.append(new_idx)
        if displayed_img:
            displayed_img[-1].grid_forget()
            displayed_img.pop()
        new_img = all_images[img_idx[-1]]
        current_img = display_images(frame, new_img)
        displayed_img.append(current_img)
        what_text.set("Image " + str(img_idx[-1] + 1) + " out of " + str(len(all_images)))


def right_arrow_page(frame, read_pdf, what_page_text):
    global current_page
    if current_page < num_pages - 1:
        current_page = current_page + 1
        page = read_pdf.getPage(current_page)
        page_content = page.extractText()
        # page_content = page_content.encode('cp1252')
        page_content = page_content.replace('\u2122', "'")
        page_contents.append(page_content)

        display_textbox(frame, page_content)
        what_page_text.set("Page " + str(current_page+1) + " out of " + str(num_pages))


def left_arrow_page(frame, read_pdf, what_page_text):
    global current_page
    if current_page > 0:
        current_page = current_page - 1
        page = read_pdf.getPage(current_page)
        page_content = page.extractText()
        # page_content = page_content.encode('cp1252')
        page_content = page_content.replace('\u2122', "'")
        page_contents.append(page_content)

        display_textbox(frame, page_content)
        what_page_text.set("Page " + str(current_page+1) + " out of " + str(num_pages))


def copy_text(root, content):
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


# display header frame
def display_hdr(root, url):
    hdr_frame = Frame(root, width=800, height=130, bg="white")
    hdr_frame.grid(sticky=EW)

    img = Image.open(url)
#    img = img.resize((int(img.size[0]/1.5), int(img.size[1]/1.5)))
    img = ImageTk.PhotoImage(img)
    img_label = Label(hdr_frame, image=img, bg="white")
    img_label.image = img
    img_label.place(x=400, y=65, anchor=CENTER)


# display browse frame
def display_browse(root, frame_del):
    brw_frame = Frame(root, width=800, height=60, bg="white")
    brw_frame.grid(row=3, column=0, sticky=NSEW)

    instructions = Label(brw_frame, text="Select a PDF file on your computer please", font=("Raleway", 14), bg="white")
    instructions.place(x=500, y=30, anchor=CENTER)

    browse_text = StringVar()
    browse_btn = Button(brw_frame, textvariable=browse_text, command=lambda: open_file(), font=("Raleway", 14),
                        bg="#20bebe", fg="white", padx=20, pady=10, borderless=True)
    browse_text.set("Browse")
    browse_btn.place(x=720, y=30, anchor=CENTER)

    def open_file():
        for i in img_idx:
            img_idx.pop()
        img_idx.append(0)

        browse_text.set("loading...")
        file = askopenfile(parent=root, mode='rb', filetypes=[("Pdf file", "*.pdf")])
        if file:
            read_pdf = PyPDF2.PdfFileReader(file)
            num_pages = read_pdf.getNumPages()
            page = read_pdf.getPage(current_page)
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

            if all_images:
                img = images[img_idx[-1]]

            frame_del.grid_forget()
            content_frame = Frame(root, width=800, height=420, bg="#20bebe")
            content_frame.grid(rowspan=2, row=1, column=0, sticky=NSEW)
            content_frame.grid_columnconfigure(0, weight=1)
            content_frame.grid_columnconfigure(1, weight=1)
            content_frame.grid_propagate(0)

            text_frame = Frame(content_frame, width=400, height=360, bg="#20bebe")
            text_frame.grid(row=0, column=0, sticky=EW)
            text_frame.grid_rowconfigure(0, weight=5)
            text_frame.grid_rowconfigure(0, weight=1)
            text_frame.grid_propagate(0)

            display_textbox(text_frame, page_content)

            page_menu = Frame(text_frame, width=400, height=60)
            page_menu.grid(column=0, row=1)
            page_menu.grid_columnconfigure(0, weight=1)
            page_menu.grid_columnconfigure(1, weight=3)
            page_menu.grid_columnconfigure(2, weight=1)

            what_page_text = StringVar()
            what_page = Label(page_menu, textvariable=what_page_text, font=("shanti", 10))
            what_page_text.set("Page " + str(current_page+1) + " out of " + str(num_pages))
            what_page.grid(row=0, column=1)

            display_icon(page_menu, "arrow_l.png", 0, 0, E,
                         lambda: left_arrow_page(text_frame, read_pdf, what_page_text))
            display_icon(page_menu, "arrow_r.png", 0, 2, W,
                         lambda: right_arrow_page(text_frame, read_pdf, what_page_text))

            img_frame = Frame(content_frame, width=400, height=360, bg="#20bebe")
            img_frame.grid(row=0, column=1, sticky=EW)
            img_frame.grid_rowconfigure(0, weight=5)
            img_frame.grid_rowconfigure(0, weight=1)
            img_frame.grid_propagate(0)

            if all_images:
                current_image = display_images(img_frame, img)
                displayed_img.append(current_image)

                # image area - image scroll
                img_menu = Frame(img_frame, width=400, height=60)
                img_menu.grid(column=0, row=1)
                img_menu.grid_columnconfigure(0, weight=1)
                img_menu.grid_columnconfigure(1, weight=3)
                img_menu.grid_columnconfigure(2, weight=1)

                what_text = StringVar()
                what_img = Label(img_menu, textvariable=what_text, font=("shanti", 10))
                what_text.set("Image " + str(img_idx[-1] + 1) + " out of " + str(len(all_images)))
                what_img.grid(row=0, column=1)

                display_icon(img_menu, "arrow_l.png", 0, 0, E,
                             lambda: left_arrow(img_frame, all_images, current_image, what_text))
                display_icon(img_menu, "arrow_r.png", 0, 2, W,
                             lambda: right_arrow(img_frame, all_images, current_image, what_text))

            # reset the button text back to Browse
            browse_text.set("Browse")

            # save area - buttons bar
            menu_frame = Frame(content_frame, width=400, height=60, bg="#20bebe")
            menu_frame.grid(row=1, column=1, sticky=E)
            menu_frame.grid_propagate(0)

            copyText_btn = Button(menu_frame, text="Copy Text", command=lambda: copy_text(root, page_contents),
                                  font=("shanti", 10), borderless=True, width=130, pady=12)
            saveAll_btn = Button(menu_frame, text="Save All Images", command=lambda: save_all(all_images),
                                 font=("shanti", 10), borderless=True, width=130, pady=12)
            save_btn = Button(menu_frame, text="Save Image", command=lambda: save_image(all_images[img_idx[-1]]),
                              font=("shanti", 10), borderless=True, width=130, pady=12)

            copyText_btn.grid(row=0, column=0, pady=6)
            saveAll_btn.grid(row=0, column=1, pady=6)
            save_btn.grid(row=0, column=2, pady=6)
        else:
            browse_text.set("Browse")


# place an icon button on the grid
def display_icon(frame, url, row, column, sticky, funct):
    icon = Image.open(url)
    # resize image
    icon = icon.resize((20, 20))
    icon = ImageTk.PhotoImage(icon)
    icon_label = Button(frame, image=icon, command=funct, padx=3, pady=3)
    icon_label.image = icon
    icon_label.grid(column=column, row=row, sticky=sticky)


# place a textbox on the pages
def display_textbox(frame, content):
    text_box = Text(frame, height=15, width=40, padx=5, pady=5)
    text_box.insert(1.0, content)
    text_box.tag_configure("center", justify="center")
    text_box.tag_add("center", 1.0, "end")
    text_box.grid(column=0, row=0, columnspan=3, sticky=NSEW, padx=20, pady=20)


# Detect Images inside the PDF document
# Thank you sylvain of Stackoverflow
# https://stackoverflow.com/questions/2693820/extract-images-from-pdf-without-resampling-in-python
def extract_images(page):
    images = []
    if '/XObject' in page['/Resources']:
        xObject = page['/Resources']['/XObject'].getObject()

        for obj in xObject:
            if xObject[obj]['/Subtype'] == '/Image':
                size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
                data = xObject[obj].getData()
                mode = ""
                if xObject[obj]['/ColorSpace'] == '/DeviceRGB':
                    mode = "RGB"
                else:
                    mode = "CMYK"
                img = Image.frombytes(mode, size, data)
                images.append(img)
    return images


def resize_image(img):
    width, height = int(img.size[0]), int(img.size[1])
    if width > height:
        height = int(300 / width * height)
        width = 300
    elif height > width:
        width = int(300 / height * width)
        height = 300
    else:
        width, height = 300, 300
    img = img.resize((width, height))
    return img


def display_images(frame, img):
    img = resize_image(img)
    img = ImageTk.PhotoImage(img)
    img_label = Label(frame, image=img, bg="white")
    img_label.image = img
    img_label.grid(column=0, row=0, padx=50)
    return img_label
