from tkinter import *
import os, sys
from multiprocessing import Process
import multiprocessing as m
import time


loadingpid = 0
def run_script():    
    p = os.system(
        "powershell.exe c:\\users\\tabbass\\desktop\\programming\\work_stuff\\passwordresetapplet.ps1"
    )    
    print(p)
    

def loading_screen():
    print(f'Loading Screen PID: {loadingpid}')
    class Window(Frame):

        def __init__(self, master=None):
            Frame.__init__(self, master)               
            self.master = master
            
    root = Tk()
    app = Window(root)
    root.update_idletasks()
    root.mainloop()


if __name__ == '__main__':
  p1 = Process(target=loading_screen)
  p2 = Process(target=run_script)
  p1.start()
  p2.start()
  time.sleep(15)
  p1.terminate()