import tkinter
from tkinter import ttk
import cv2
import PIL.Image, PIL.ImageTk
import mediapipe
from threading import Thread
import HandTracking

class MyVideoCapture:
    def __init__(self, video_source = 0):
        self.vid = cv2.VideoCapture(video_source, cv2.CAP_DSHOW)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            cv2.flip(frame, 1)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            if ret:
                return (ret, frame)
            else:
                return (ret, None)
        else:
            return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

class App:
    def __init__(self, window):
        ### Main Window Configurations##
        # Main window will stay at top-left corner and always on top of other windows
        self.window = window
        self.window.resizable(False, False)
        self.window.attributes('-topmost', True)
        self.window.overrideredirect(True)
        self.window.configure(background="#F5DD84")

        ###---------- Building UI ----------###
        # Buttons
        buttonLabel = tkinter.Label(self.window)
        buttonLabel.configure(background="#F5DD84")
        buttonLabel.grid(row = 0, column = 0, columnspan = 5)

        self.mouse_btn=tkinter.Button(buttonLabel, bg="#6FC8EB", text="Mouse Control", width=12, height=4, command=self.mouse_control)
        self.mouse_btn.grid(row=0, column=0, padx=(5,33),pady=10)
        self.m_is_on = False

        self.draw_btn=tkinter.Button(buttonLabel, bg="#6FC8EB", text="Draw", width=12, height=4, command=self.drawing)
        self.draw_btn.grid(row=0, column=1, padx=(0,33),pady=10)
        self.d_is_on = False

        self.type_btn=tkinter.Button(buttonLabel, bg="#6FC8EB", text="Type", width=12, height=4, command=self.typing)
        self.type_btn.grid(row=0, column=2, padx=(0,33),pady=10)
        self.t_is_on = False

        self.cam_btn=tkinter.Button(buttonLabel, bg="#6FC8EB", text="Camera On/Off", width=12, height=4, command=self.canvas_toggle)
        self.cam_btn.grid(row=0, column=3, padx=(0,33),pady=10)

        self.exit_btn=tkinter.Button(buttonLabel, bg="#6FC8EB", text="Exit", width=12, height=4, command=self.exit)
        self.exit_btn.grid(row=0, column=4, padx=(0,33),pady=10)

        # Canvas for video display
        self.canvas = tkinter.Canvas(self.window, width = 640, height = 480)
        self.canvas.grid(row = 1, column = 0, columnspan = 5)
        self.canvas.config(state='disable')
        self.canvas.grid_remove()

        #Side window for draw and type functions, hidden at start
        self.side_window = SideWindow()
        self.side_window.withdraw()

        ###----------- Video Capture -----------###
        self.vid = MyVideoCapture()

        self.read_thread = Thread(target = self.update, args=(), daemon=True)
        self.read_thread.start()
        self.window.mainloop()

    # This method will be used to show/hide camera display
    def canvas_toggle(self):
        if (self.canvas.cget('state') == "normal"):
            self.canvas.grid_remove()
            self.canvas.config(state='disable')
            self.cam_btn.config(bg="#6FC8EB")
        else:
            self.canvas.grid()
            self.canvas.config(state='normal')
            self.cam_btn.config(bg="#2B7DF0")

    def mouse_control(self):
        if self.m_is_on == False and self.d_is_on == False and self.t_is_on == False:
            print("Starting mouse control...")
            self.m_is_on = True
            self.mouse_btn.config(bg="#2B7DF0")
        elif self.m_is_on == True and self.d_is_on == False and self.t_is_on == False:
            print("Stopping mouse control...")
            self.m_is_on = False
            self.mouse_btn.config(bg="#6FC8EB")
        else:
            print("Disable other functions!")

    def drawing(self):
        if self.m_is_on == False and self.d_is_on == False and self.t_is_on == False:
            print("Starting drawing...")
            self.d_is_on = True
            self.draw_btn.config(bg="#2B7DF0")
            self.side_window.deiconify()
        elif self.m_is_on == False and self.d_is_on == True and self.t_is_on == False:
            print("Stopping drawing...")
            self.d_is_on = False
            self.draw_btn.config(bg="#6FC8EB")
            self.side_window.withdraw()
        else:
            print("Disable other functions!")

    def typing(self):
        if self.m_is_on == False and self.d_is_on == False and self.t_is_on == False:
            print("Starting typing...")
            self.t_is_on = True
            self.type_btn.config(bg="#2B7DF0")
            self.side_window.deiconify()
        elif self.m_is_on == False and self.d_is_on == False and self.t_is_on == True:
            print("Stopping typing...")
            self.t_is_on = False
            self.type_btn.config(bg="#6FC8EB")
            self.side_window.withdraw()
        else:
            print("Disable other functions!")

    # Since toolbar is removed a custom exit method is required
    def exit(self):
        self.window.destroy()
        self.side_window.destroy()
        self.window, self.side_window = None, None

    # Update canvas display using video frames
    def update(self):
        ret, frame = self.vid.get_frame()
        if ret and self.canvas.cget('state') == 'normal':               
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)

        if self.m_is_on:
            pass

        if self.d_is_on:
            pass

        if self.t_is_on:
            pass

        self.window.after(33, self.update)


    def mouse(self):
        pass

    def draw(self):
        pass

    def type(self):
        pass

    
class SideWindow:
    def __init__(self):
        self.side_window = tkinter.Tk()
        self.side_window.resizable(False, False)
        self.side_window.attributes('-topmost', True)
        self.side_window.attributes('-alpha', 0.5)
        self.side_window.overrideredirect(True)
        self.side_window.configure(background="#F5DD84")
        self.screen_width = self.side_window.winfo_screenwidth()
        self.screen_height = self.side_window.winfo_screenheight()
        self.side_window.geometry("%dx%d+%d+%d" % (self.screen_width-650, self.screen_height, 644, 0))

        self.top_bar = tkinter.Label(self.side_window, bg = "#F5DD84")
        self.top_bar.grid(row=0, column=0)

        self.label = tkinter.Label(self.top_bar, text = "Opacity", bg = "#F5DD84")
        self.label.config(font=("Courier Bold", 20))
        self.label.grid(row = 1, column=0, padx=20, pady=10)

        self.slider = ttk.Scale(self.top_bar,from_ = 0.2, to = 1.0, value = 1.0, orient = tkinter.HORIZONTAL, command=self.slide)
        self.slider.grid(row = 2, column=0, padx=20)

    def slide(self, x):
        self.side_window.attributes('-alpha', self.slider.get())

    def withdraw(self):
        self.side_window.withdraw()

    def deiconify(self):
        self.side_window.deiconify()

    def destroy(self):
        self.side_window.destroy()

app = App(tkinter.Tk())