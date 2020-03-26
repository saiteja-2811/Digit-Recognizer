# -*- coding: utf-8 -*-
"""
@author: mahitha.sree
"""
#%%
import tkinter as tk
from PIL import Image
import io
import os
import glob
from app_func import predict_letter


class ocr_app(tk.Tk):
    def __init__(self,parent):
       tk.Tk.__init__(self,parent)
       self.parent = parent
       self.initialize()
      
    def initialize(self):
        self.grid()
        
        self.message = tk.Label( self, text = "Drag the mouse to draw" )
        self.message.grid(column = 1,row = 0)
        
        self.myCanvas = tk.Canvas( self )
        self.myCanvas.grid(column = 1,row = 1)
        self.myCanvas.bind( "<B1-Motion>", self.paint )
        
        self.button = tk.Button(self,text="Predict",command = self.predictiction)
        self.button.grid(column=2,row=0)
        
        self.button = tk.Button(self,text = "Clear",command = self.clear)
        self.button.grid(column = 2,row = 1)
    
    def paint( self, event ):
      x1, y1 = ( event.x - 4 ), ( event.y - 4 )
      x2, y2 = ( event.x + 4 ), ( event.y + 4 )
      self.myCanvas.create_oval( x1, y1, x2, y2, fill = "black" )
     
    def clear(self):
        self.myCanvas.delete("all")
        files = glob.glob('pix*.png')
        for f in files:
            os.remove(f)
        
    
    def predictiction(self):
        ps = self.myCanvas.postscript(colormode='color')
        img = Image.open(io.BytesIO(ps.encode('utf-8')))
        img.save('canvas.jpg')
        print("Image saved")
        predict_letter('canvas.jpg')
   

if __name__ == "__main__":
    app = ocr_app(None)
    app.title('OCR Application')
    app.mainloop()
#%%