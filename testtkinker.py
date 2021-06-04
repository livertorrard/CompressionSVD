import tkinter as tk
from tkinter.constants import *
import os
from numpy import pad
from tkinter import Grid, PhotoImage, filedialog
from PIL import Image , ImageTk
import numpy
import random
#mở ảnh, chia ra các kênh
def openImage(imagePath):
    imOrig = Image.open(imagePath)
    im = numpy.array(imOrig)

    aRed = im[:, :, 0]
    aGreen = im[:, :, 1]
    aBlue = im[:, :, 2]

    return [aRed, aGreen, aBlue, imOrig]
def compressSingleChannel(channelDataMatrix, singularValuesLimit):
    uChannel, sChannel, vhChannel = numpy.linalg.svd(channelDataMatrix) #phân tích ra U,S,V
    k = singularValuesLimit #Hệ số k
    print(uChannel.shape)
    print(sChannel.shape)
    print(vhChannel.shape)
    leftSide = numpy.matmul(uChannel[:, 0:k], numpy.diag(sChannel)[0:k, 0:k]) #tích của u có cột từ 0 đến k và s 
    aChannelCompressedInner = numpy.matmul(leftSide, vhChannel[0:k, :]) #tích của leftside và vh
    aChannelCompressed = aChannelCompressedInner.astype('uint8')
    return aChannelCompressed


def chonanh():
    pathname = filedialog.askopenfilename(initialdir = "D:\test",
                                          title = "Vui lòng chọn ảnh",
                                          filetypes = (("Image files",
                                                        "*.png .jpg .jpeg"),
                                                       ("all files",
                                                        "*.*")))                                             
    filename = os.path.basename(pathname)
    chonanhh(filename)
    aRed, aGreen, aBlue, originalImage = openImage(filename)
    singularValuesLimit = 431 # hệ số k
    #nén từng kênh của ảnh
    aRedCompressed = compressSingleChannel(aRed, singularValuesLimit)
    aGreenCompressed = compressSingleChannel(aGreen, singularValuesLimit)
    aBlueCompressed = compressSingleChannel(aBlue, singularValuesLimit)
    #tạo ra 1 đối tượng từ mảng 
    imr = Image.fromarray(aRedCompressed, mode=None)
    img = Image.fromarray(aGreenCompressed, mode=None)
    imb = Image.fromarray(aBlueCompressed, mode=None)
    #tổng hợp lại thành 1 ảnh
    newImage = Image.merge("RGB", (imr, img, imb))
    radomimg = random.randint(1, 1000000)
    newImage.save(str(radomimg)+"anhsaukhinen.gif")
    taolao = tk.PhotoImage(file=str(radomimg)+"anhsaukhinen.gif")
    test1.configure(image=taolao)
    test1.image = taolao

    infor1(filename)
    infor2(str(radomimg)+"anhsaukhinen.gif")
def chonanhh(filename):
    alo = tk.PhotoImage(file=filename)
    test.configure(image=alo)
    test.image = alo  
def infor1(filename):
    image = Image.open(filename)
    width, height = image.size  
    file_stats = os.stat(filename)    
    imform1.configure(text=f"Name : {filename} \nWidth : {width} \n Height : {height} \n Size on disk : {file_stats.st_size} ")
def infor2 (newname):
    image = Image.open(newname)
    width, height = image.size  
    file_stats = os.stat(newname)    
    imform2.configure(text=f"Name : {newname} \nWidth : {width} \n Height : {height} \n Size on disk : {file_stats.st_size} ")    
win = tk.Tk()
win.title("Xử lí tín hiệu số")
win.geometry('900x700')
win.resizable(width=False,height=False)
tieude = tk.Label(win,text="NÉN ẢNH BẰNG PHƯƠNG PHÁP SVD",font="Times 20 bold",fg="white",bg="black")
tieude.pack(side=TOP,pady=15)

FrameButton = tk.Frame(win)
FrameButton.pack(padx=120)

photo =tk.PhotoImage(file="logo.png")
test = tk.Label(win,image=photo)
test.place(width=350,height=400,x=50,y=180)

test1 = tk.Label(win,image=photo,width=200,height=200)
test1.place(width=350,height=400,x=490,y=180)

label = tk.Label(win,text="ẢNH GỐC",font="Times 20 bold",fg="green")
label.place(x =150,y = 130)

label2 = tk.Label(win,text="ẢNH SAU KHI NÉN",font="Times 20 bold",fg="green")
label2.place(x =530,y = 130)

chonAnh =  tk.Button(FrameButton,text="Chọn Ảnh",command=chonanh)
chonAnh.grid(row=1,column=1)

imform1 = tk.Label(text="Width : \n Height : \n Size on disk : ",font="Times 10 bold",fg="black") 
imform1.place(x = 150,y = 600)

imform2 = tk.Label(text="Width : \n Height : \n Size on disk : ",font="Times 10 bold",fg="black") 
imform2.place(x = 600,y = 600)

win.bind("<Return>", chonanhh)
win.mainloop()