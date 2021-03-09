import numpy as np
from scipy import signal
from PIL import Image
from copy import deepcopy
import math

original_image = input()
n = int(input())
a, b = map(int, input().split())

if n <= 500:
    update = 0.3
elif n <= 1000:
    update = 0.2
else: 
    update = 0.1


arrMain = Image.open(original_image, 'r')

arrMain = arrMain.resize((int(arrMain.size[0]*update), int(arrMain.size[1]*update)))

openCVimMain = np.asarray(arrMain)

openCVimMain = (openCVimMain - openCVimMain.mean())# / (openCVimMain.std())

for i in range(n):

    segment = input()
    
    arrSegment = Image.open(segment, 'r')
    

    arrSegment = arrSegment.resize(( int(a * update), int(b * update) ))
    
    openCVSegment = np.asarray(arrSegment)
    
    openCVSegment = (openCVSegment - openCVSegment.mean())# / openCVSegment.std() 

    arr = signal.correlate(openCVimMain, openCVSegment, mode = 'valid', method='auto')
    sol = np.unravel_index(arr.argmax(), arr.shape)
    
    print(f"{int(sol[1] / update)},{int(sol[0] / update)}")