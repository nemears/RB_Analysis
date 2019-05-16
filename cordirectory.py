import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import csv

path = '150cSt-40V-4.74mm'
pictures = []
for entry in os.listdir(path):
    if entry.endswith('.jpg'):
        im = Image.open(path +'/'+ entry).convert('L')
        pictures.append(np.asarray(im))

x = []
y = []


def onclick(event):
    x.append(int(event.xdata))
    y.append(int(event.ydata))
    if len(x) >= 2:
        plt.close()
        print('x: ',x)
        print('y: ',y)

def redraw(event):
    x.clear()
    y.clear()
    plt.close()
    draw()

def run(event):
    plt.close()

def draw():
    fig = plt.figure(1)
    cid = fig.canvas.mpl_connect('button_press_event', onclick)    
    plt.imshow(np.asarray(pictures[-1]),cmap='gray')
    font = {'family': 'serif',
            'color':  'white',
            'weight': 'normal',
            'size': 16,
            }
    plt.text(20,20,'click to draw rectangle',fontdict=font)
    plt.show()

    fig2 = plt.figure(2)
    plt.imshow(np.asarray(pictures[len(pictures)//2])[min(y):max(y),min(x):max(x)],cmap='gray')
    global h_array
    h_array = pictures[len(pictures)//2][min(x):max(x),min(y):max(y)]
    axredraw = plt.axes([0.7, 0.05, 0.1, 0.075])
    axrun = plt.axes([0.81, 0.05, 0.1, 0.075])
    redraw_btn = Button(axredraw, 'Redraw')
    redraw_btn.on_clicked(redraw)
    run_btn = Button(axrun, 'Run')
    run_btn.on_clicked(run)
    plt.show()

draw()

crop = []
for p in pictures:
    crop.append(p[min(y):max(y),min(x):max(x)])


def getCircle(cx,cy,r):
    coords = []
    x = r
    y = 0
    while x>=y:
        coords.append((x,y))
        if x**2 + (y+1)**2 > r**2:
            x-=1
        y+=1
    tcoords = []
    for c in coords:
        tcoords.append((-c[0]+cx,-c[1]+cy))
        tcoords.append((-c[0]+cx,c[1]+cy))
        tcoords.append((c[0]+cx,-c[1]+cy))
        tcoords.append((c[0]+cx,c[1]+cy))
        tcoords.append((-c[1]+cx,-c[0]+cy))
        tcoords.append((-c[1]+cx,c[0]+cy))
        tcoords.append((c[1]+cx,-c[0]+cy))
        tcoords.append((c[1]+cx,c[0]+cy))
    return tcoords

def acf(array):
    hwidth, hheight = np.shape(array)
    fftim = np.fft.fft2(array)
    conjim = np.conj(fftim)
    ans1 = fftim*conjim
    ans2 = np.fft.ifft2(ans1)/(hwidth*hheight)
    ans3 = ans2.real
    global ans4
    ans4 = np.zeros(np.shape(ans3))

    for i in range(hwidth):
        for j in range(hheight):
            ans4[i][j]=ans3[i][j]-np.min(ans3)
    
    ans4 = ans4/np.max(ans4)
    ans5 = np.fft.fftshift(ans4)
    cor = []
    for r in range(min(hwidth//2,hheight//2)):
        coords = getCircle(hwidth//2,hheight//2,r)
        tot = 0
        for c in coords:
            tot+=ans5[c[0]][c[1]]
        cor.append(tot/len(coords))
    return cor

cor = []
i=0
myFile = open(path+'.csv', 'w')
with myFile:  
    writer = csv.writer(myFile)
    writer.writerow(range(len(acf(crop[0]))))
    for c in crop:
        a = acf(c)
        writer.writerow(a)
        print(i)
        cor.append(a)
        i+=1
