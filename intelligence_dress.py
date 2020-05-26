import tkinter as tk
import cv2
import numpy as np
from PIL import Image, ImageTk
from tkinter import filedialog
import os
import pandas as pd
import get_attr

WIDTH = 950
HEIGHT = 600
os.system('chcp 65001')


class Page:
    def __init__(self, master):
        self.master = master
        self.page = tk.Frame(self.master)

    def show(self):
        self.page.pack(fill='both', expand=True)

    def hide(self):
        self.page.pack_forget()


stop = False
cv2image = []


def take_snapshot():
    global stop, cv2image
    stop = True
    cv2image = cv2.cvtColor(cv2image, cv2.COLOR_RGB2BGR)
    cv2.imshow("the photo you catch", cv2image)


def re_photo():
    global stop
    if stop:
        stop = False
        video_loop()


def video_loop():
    global stop, cv2image
    success, img = camera.read()  # 从摄像头读取照片
    if success and not stop:
        cv2.waitKey(10)
        cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 转换颜色从BGR到RGBA
        cv2image = cv2.flip(cv2image, 1)
        current_image = Image.fromarray(cv2image)  # 将图像转换成Image对象
        image = ImageTk.PhotoImage(image=current_image)
        p2_image.image = image
        p2_image.config(image=image)
        root.after(1, video_loop)


def switch_page(current_page, target_page):
    current_page.hide()
    target_page.show()


camera = cv2.VideoCapture(0)

root = tk.Tk()
root.geometry("950x600")
root.resizable(width=False, height=False)

page1 = Page(root)
page2 = Page(root)
page3 = Page(root)
page_wardrobe = Page(root)

# 第一页
page1.show()
btn_start = tk.Button(page1.page, text='开始', command=lambda: switch_page(page1, page2),
                      width=10, height=1, font=('simhei', 20))
btn_start.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
btn_wardrobe = tk.Button(page1.page, text="我的衣柜", command=lambda: switch_page(page1, page_wardrobe),
                         width=10, height=1, font=('simhei', 20))
btn_wardrobe.place(relx=0.2, rely=0.8, anchor=tk.CENTER)
label_title = tk.Label(page1.page, text='穿搭小助手', font=('simhei', 35))
label_title.place(relx=0.5, rely=0.382, anchor=tk.CENTER)

# 第二页
p2_label1 = tk.Label(page2.page, text='首先我们来照一张全身照吧！', font=('simhei', 10))
p2_label1.place(relx=0.5, rely=0.05, anchor=tk.CENTER)
p2_label2 = tk.Label(page2.page, text='请你站在红色的框框里面', font=('simhei', 8))
p2_label2.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
p2_image = tk.Label(page2.page)
p2_image.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=0.8, relheight=0.6)
video_loop()
btn_temp = tk.Button(page2.page, text='临时跳转下一页', command=lambda: switch_page(page2, page3), font=('simhei', 10))
btn_temp.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

# 第三页
p3_label1 = tk.Label(page3.page, text='请问你出门去哪里呢？', font=('simhei', 10))
p3_label1.place(relx=0.5, rely=0.05, anchor=tk.CENTER)
p3_label2 = tk.Label(page3.page, text='请在嘀的一声后说下吧', font=('simhei', 8))
p3_label2.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
b1 = tk.Button(page3.page, text='上班')
b2 = tk.Button(page3.page, text='旅游')
b3 = tk.Button(page3.page, text='上学')
b4 = tk.Button(page3.page, text='运动')
b5 = tk.Button(page3.page, text='聚会')
p3_buttons = [b1, b2, b3, b4, b5]
item_width = 1 / 5
for i in range(len(p3_buttons)):
    rx = np.random.rand() * 0.6 + 0.2
    ry = np.random.rand() * 0.6 + 0.2
    p3_buttons[i].place(relx=rx, rely=ry, anchor='center')

# 衣橱页面

current_page = 0
cloth_dir = 'data'
cloth_images_name = []
selectFile = None
filename = None

for r, dirs, files in os.walk(cloth_dir):
    for f in files:
        if f[-3:] == 'jpg' or f[-3:] == 'png':
            cloth_images_name.append(r + os.sep + f)
default_image = ImageTk.PhotoImage(Image.open('default.jpg').resize((150, 200)))
img = Image.open('background.jpg')
photo = ImageTk.PhotoImage(img)
background_label = tk.Label(
    page_wardrobe.page,
    image=photo,
    fg="white",
    width=WIDTH,
    height=HEIGHT
)
background_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

pw_label_title = tk.Label(page_wardrobe.page, text='我的衣橱', font=('simhei', 20), bg='grey')
pw_label_title.place(relx=0.5, rely=0.07, anchor=tk.CENTER)

# cloth_images_name = ["data/Figure_1.png", "data/Figure_2.png", "data/hello.jpg"]

all_page = len(cloth_images_name) // 4
if len(cloth_images_name) % 4 != 0:
    all_page += 1

cloth_images = [ImageTk.PhotoImage(Image.open(x).resize((150, 200))) for x in cloth_images_name]
cloth_label1 = tk.Label(
    page_wardrobe.page,
    width=150,
    height=200
)
cloth_label2 = tk.Label(
    page_wardrobe.page,
    width=150,
    height=200
)
cloth_label3 = tk.Label(
    page_wardrobe.page,
    width=150,
    height=200
)
cloth_label4 = tk.Label(
    page_wardrobe.page,
    width=150,
    height=200
)
cloth_label1.place(relx=0.2, rely=0.3, anchor=tk.CENTER)
cloth_label2.place(relx=0.4, rely=0.3, anchor=tk.CENTER)
cloth_label3.place(relx=0.6, rely=0.3, anchor=tk.CENTER)
cloth_label4.place(relx=0.8, rely=0.3, anchor=tk.CENTER)


def next_page():
    global current_page, cloth_images, all_page
    if all_page == 0:
        cloth_label1.config(image=default_image)
        cloth_label1.image = default_image
        cloth_label2.config(image=default_image)
        cloth_label2.image = default_image
        cloth_label3.config(image=default_image)
        cloth_label3.image = default_image
        cloth_label4.config(image=default_image)
        cloth_label4.image = default_image
        return
    current_page = (current_page + 1) % all_page
    if current_page == 0:
        left = len(cloth_images_name) % 4
        if left == 1:
            cloth_label1.config(image=cloth_images[-1])
            cloth_label1.image = cloth_images[-1]
            cloth_label2.config(image=default_image)
            cloth_label2.image = default_image
            cloth_label3.config(image=default_image)
            cloth_label3.image = default_image
            cloth_label4.config(image=default_image)
            cloth_label4.image = default_image
        elif left == 2:
            cloth_label1.config(image=cloth_images[-2])
            cloth_label1.image = cloth_images[-2]
            cloth_label2.config(image=cloth_images[-1])
            cloth_label2.image = cloth_images[-1]
            cloth_label3.config(image=default_image)
            cloth_label3.image = default_image
            cloth_label4.config(image=default_image)
            cloth_label4.image = default_image
        elif left == 3:
            cloth_label1.config(image=cloth_images[-3])
            cloth_label1.image = cloth_images[-3]
            cloth_label2.config(image=cloth_images[-2])
            cloth_label2.image = cloth_images[-2]
            cloth_label3.config(image=cloth_images[-1])
            cloth_label3.image = cloth_images[-1]
            cloth_label4.config(image=default_image)
            cloth_label4.image = default_image
        else:
            cloth_label1.config(image=cloth_images[-4])
            cloth_label1.image = cloth_images[-4]
            cloth_label2.config(image=cloth_images[-3])
            cloth_label2.image = cloth_images[-3]
            cloth_label3.config(image=cloth_images[-2])
            cloth_label3.image = cloth_images[-2]
            cloth_label4.config(image=cloth_images[-1])
            cloth_label4.image = cloth_images[-1]
    else:
        cloth_label1.config(image=cloth_images[(current_page - 1) * 4])
        cloth_label1.image = cloth_images[(current_page - 1) * 4]
        cloth_label2.config(image=cloth_images[(current_page - 1) * 4 + 1])
        cloth_label2.image = cloth_images[(current_page - 1) * 4 + 1]
        cloth_label3.config(image=cloth_images[(current_page - 1) * 4 + 2])
        cloth_label3.image = cloth_images[(current_page - 1) * 4 + 2]
        cloth_label4.config(image=cloth_images[(current_page - 1) * 4 + 3])
        cloth_label4.image = cloth_images[(current_page - 1) * 4 + 3]


def upload_file():
    global selectFile, filename, cloth_images_name, all_page, cloth_images
    target_dir = 'data'
    selectFile = filedialog.askopenfilename(title='选择图片文件', filetypes=[('服装图片', '*.png;*.jpg')])
    filename = selectFile.split('/')[-1]
    selectFile = selectFile.replace("/", "\\")
    if selectFile is not None:
        if not os.path.exists(target_dir):
            os.mkdir(target_dir)
        command = 'copy  ' + selectFile + '  ' + target_dir + '\\' + filename
        os.system(command)
        if not os.path.exists(target_dir + os.sep + "分类数据.csv"):
            cloth_attrs = ["name", "Graphic Ringer Tee", "Sheer Pleated Front Blouse",
                           "Sheer Sequin Tank", "Single Button Blazer"]
            temp_data = pd.DataFrame(columns=cloth_attrs)
        else:
            temp_data = pd.read_csv(target_dir + os.sep + "分类数据.csv")
        temp_image = get_attr.get_one_image(target_dir + '\\' + filename)
        temp_attr = get_attr.evaluate_one_image(temp_image)
        my_dic = {"name": filename, "Graphic Ringer Tee": temp_attr[0], "Sheer Pleated Front Blouse": temp_attr[1],
                  "Sheer Sequin Tank": temp_attr[2], "Single Button Blazer": temp_attr[3]}
        all_attr = [my_dic]
        pd_data = pd.DataFrame(all_attr)
        temp_data = temp_data.append(pd_data)
        temp_data.to_csv(target_dir + os.sep + "分类数据.csv", index=False)

        # 更新页面
        cloth_images_name = []
        for rt, dirs, files in os.walk(cloth_dir):
            for f in files:
                if f[-3:] == 'jpg' or f[-3:] == 'png':
                    cloth_images_name.append(rt + os.sep + f)
        all_page = len(cloth_images_name) // 4
        if len(cloth_images_name) % 4 != 0:
            all_page += 1
        cloth_images = []
        cloth_images = [ImageTk.PhotoImage(Image.open(x).resize((150, 200))) for x in cloth_images_name]
        next_page()
        return
    selectFile = None
    filename = None


next_page()
pw_button_next = tk.Button(page_wardrobe.page, text="下一个衣橱", command=next_page,
                           font=('simhei', 20), bg='grey')
pw_button_next.place(relx=0.8, rely=0.8, anchor=tk.CENTER)
pw_button_back = tk.Button(page_wardrobe.page, text="返回主页面", command=lambda: switch_page(page_wardrobe, page1),
                           font=('simhei', 20), bg='grey')
pw_button_back.place(relx=0.2, rely=0.8, anchor=tk.CENTER)
pw_button_insert = tk.Button(page_wardrobe.page, text="上传我的衣服", command=upload_file,
                             font=('simhei', 20), bg='grey')
pw_button_insert.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
root.mainloop()
