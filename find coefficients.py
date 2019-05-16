import csv
from scipy.optimize import curve_fit
from math import pi
import numpy as np
import matplotlib.pyplot as plt

directory = '150cSt-40V-5.02mm'
save = directory+'-fit'
acfs = []

with open(directory+'.csv','r') as file:
    reader = csv.reader(file)
    for row in reader:
        if row != []:
            temp = [float(i) for i in row]
            acfs.append(temp)

file.close()

def norm(x,mu,sigma): # Dont use
    return (2*sigma**2*pi)**-0.5*np.exp(-(mu-x)**2/(2*sigma**2))

def ex(x,l,A):
    return A*np.exp(-l*x)

def iex(x,l): # Dont use
    return 1-np.exp(-l/x)

x = acfs.pop(0)

fit1,fit2,fit3 = [],[],[]
cov1,cov2,cov3 = [],[],[]

def index0(a):
    grad = np.gradient(a)
    zIndex = [0]
    thresh = len(a)//2
    for i in range(1,len(grad)):
        if np.sign(grad[i]) < np.sign(grad[i-1]) and i < zIndex[-1]+thresh:
            thresh = 2*(i-zIndex[-1])
            zIndex.append(i)
    return zIndex

def fitem(a):
    fits = []
    cov = []
    zeros = index0(a)
    
    for z in zeros:
        t1,t2 = curve_fit(ex,x[z:],a[z:])
        for t in t1:
            fits.append(t)
        cov.append(t2)
    return fits, cov

for a in acfs:
    t1,t2 = fitem(a)
    fit1.append(t1)
    cov1.append(t2)

with open(save+'.csv','w') as wFile:
    writer = csv.writer(wFile)
    writer.writerow(['T','L1','A1','L2','A2','L3','A3'])
    count = 0
    for f in fit1:
        writer.writerow([count]+f)
        count+=1
    wFile.close()
