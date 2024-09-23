from tkinter import Tk, StringVar
import tkinter.messagebox as msgbox
from tkinter.ttk import Frame, Button
from sqlalchemy.exc import IntegrityError
from tkinter.constants import BOTH, BOTTOM

from storage import storage
from frames import AppFrame, FRAMES



def validate_length(text: str, max_length: str, min_length: str = "0"):
    length = len(text)
    min_length, max_length = int(min_length), int(max_length)
    return min_length <= length <= max_length



class App:
    def __init__(self) -> None:
        self.root = Tk()
        self.frame = Frame(self.root)
        self.var_back = StringVar(self.frame, "Exit", "back")
        self.button_back = Button(self.frame, textvariable = self.var_back, command = self.back)
        self.loaded_frame: AppFrame = None
        self.init()
    

    def init(self):
        """Creates components and sets up interface"""
        # Set up window
        self.root.wm_title("Student Management Application")
        self.root.wm_geometry("640x480+200+100")
        self.root.wm_resizable(False, False)

        # Bind events
        self.root.bind("<Escape>", self.close)

        self.validate_length = self.frame.register(validate_length)
    

    def run(self):
        """Starts the application"""
        self.frame.pack(expand = True, fill = BOTH)
        self.button_back.pack(expand = True, side = BOTTOM)
        self.load_frame(FRAMES.LOGIN.value)
        self.root.mainloop()    

    def back(self) -> None:
        if isinstance(self.loaded_frame, FRAMES.MENU.value):
            self.load_frame(FRAMES.LOGIN.value)
        elif isinstance(self.loaded_frame, FRAMES.LOGIN.value):
            self.close()
        else:
            self.load_frame(FRAMES.MENU.value)


    def close(self, event = None) -> None:
        """Exits the application"""
        if msgbox.askyesno("Close Window" , "Exit the application ?"):
            self.quit()
    

    def quit(self):
        """Quits the application"""
        self.root.destroy()
        self.root.quit()


    def load_frame(self, frame: AppFrame):
        """Loads a frame"""
        assert issubclass(frame, AppFrame)
        if self.loaded_frame:
            self.close_frame()
        self.loaded_frame = frame(self, self.frame)
        self.loaded_frame.layout()
                
        if isinstance(self.loaded_frame, FRAMES.MENU.value):
            self.var_back.set("Logout")

        elif isinstance(self.loaded_frame, FRAMES.LOGIN.value):
            self.var_back.set("Exit")
        else:
            self.button_back.configure(width = '')
            self.var_back.set("Back")
 

    def close_frame(self):
        assert self.loaded_frame, "No frame has been loaded"
        self.loaded_frame.destroy()
        self.loaded_frame = None
    
    
    def handle_event(self , event):
        """ Method to handle events"""
        self.event = event
    