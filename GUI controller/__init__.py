import serial
import serial.tools.list_ports
import tkinter as tk
from tkinter import messagebox
import threading
import pyautogui
import PIL.Image
import PIL.ImageTk
import cv2

# Gloval variables

main_window = tk.Tk()
current_option = tk.StringVar(main_window)
btn_text_var = None
arduino_thread = None
window_is_alive = True
ser = None
presentation_started = False
glove_image = None

IMAGES_DIR = "../assets/pics/"


class GloveController:

    def __init__(self):
        self.fingers = {"index_finger_action": 'LEFT',
                        "middle_finger_action": 'RIGHT',
                        "ring_finger_action": 'F5',
                        "baby_finger_action": None}

        print("Starting glove controller")


def transform_img(img_array):
    global glove_image, main_window
    img_array = cv2.cvtColor(cv2.resize(img_array, (300, 300)), cv2.COLOR_BGR2RGB)
    img = PIL.Image.fromarray(img_array)
    img_tk = PIL.ImageTk.PhotoImage(img)
    return img_tk


def get_finger(index):
    global glove_image, main_window
    if index == 'I':
        tmp_img = transform_img(cv2.imread("../assets/pics/gc_index.png"))
        glove_image.configure(image=tmp_img)
        glove_image.image = tmp_img
        main_window.update()
        return 'index_finger'
    elif index == 'M':
        tmp_img = transform_img(cv2.imread("../assets/pics/gc_middle.png"))
        glove_image.configure(image=tmp_img)
        glove_image.image = tmp_img
        main_window.update()
        return 'middle_finger'
    elif index == 'R':
        tmp_img = transform_img(cv2.imread("../assets/pics/gc_ring.png"))
        glove_image.configure(image=tmp_img)
        glove_image.image = tmp_img
        main_window.update()
        return 'ring_finger'
    elif index == 'B':
        tmp_img = transform_img(cv2.imread("../assets/pics/gc_baby.png"))
        glove_image.configure(image=tmp_img)
        glove_image.image = tmp_img
        main_window.update()
        return None
    else:
        return None


def do_action(action, glove_controller):
    global presentation_started

    finger = get_finger(action)

    finger_action = "{}_action".format(finger)
    if finger is not None:
        pyautogui.press(glove_controller.fingers[finger_action])
        if finger == 'ring_finger':
            if presentation_started:
                glove_controller.fingers['ring_finger_action'] = "ESC"
                presentation_started = False
            else:
                glove_controller.fingers['ring_finger_action'] = "F5"
                presentation_started = True


def kill_arduino_thread():
    global window_is_alive, arduino_thread, main_window, ser

    print("Exiting")

    window_is_alive = False
    main_window.destroy()
    if ser is not None:
        ser.close()
    if arduino_thread is not None:
        arduino_thread.join()


def start_listening():
    global window_is_alive, ser, arduino_thread
    if current_option.get() != "Select port":
        port_selected = current_option.get().split("-")[0].strip()
        try:
            ser = serial.Serial(port_selected)
            messagebox.showinfo(title="Connected", message="¡Connected successfully!")
            btn_text_var.set("Stop listening")
            glove_controller = GloveController()
            while window_is_alive:
                serial_data = (ser.read()).decode('utf-8')
                if len(serial_data) > 0:
                    print("Doing action")
                    do_action(serial_data, glove_controller)
            #ser.close()
            print("Good bye")
        except Exception as e:
            print(e)
            messagebox.showerror(title="Error", message="Error. Port is Busy")
            btn_text_var.set("Start listening")


def init_thread():
    global arduino_thread, ser, window_is_alive
    if arduino_thread is None:
        arduino_thread = threading.Thread(target=start_listening)
        arduino_thread.start()
    else:
        if ser is not None:
            window_is_alive = False
            ser.close()
            btn_text_var.set("Start listening")

        arduino_thread.join()
        arduino_thread = None


def get_ports():
    ports = serial.tools.list_ports.comports()
    ports_desc = []
    for port in ports:
        device = port.device
        description = port.description
        ports_desc.append(f"{device} - {description}")
        print(f"Device: {device}, Description: {description}")
    if len(ports_desc) > 0:
        return ports_desc
    else:
        return None


def display_ports():
    options = get_ports()
    if options is not None:
        select = tk.OptionMenu(main_window, current_option, *options)
        select.config(bg="#F1FAEE",font=('Open Sans', 8))
        select.place(x=170, y=100, width=300)


def main():
    global arduino_thread, window_is_alive, glove_image, btn_text_var

    # Window settup
    window_title = "Glove Controller"
    width, height = 600, 600

    main_window.title(window_title)
    main_window.resizable(False, False)
    main_window.geometry(f"{width}x{height}")
    main_window.config(bg="#F1FAEE")
    # Title label
    title_label = tk.Label(master=main_window, text="Glove Controller", font=('Open Sans', 32),bg="#F1FAEE")
    title_label.place(x=150, y=20)

    current_option.set("Select port")

    # Button start listening
    btn_text_var = tk.StringVar(value="Start listening")
    btn_start_listening = tk.Button(master=main_window, textvariable=btn_text_var,
                                    command=init_thread, font=('Open Sans', 16))
    btn_start_listening.config(bg="#F1FAEE")
    btn_start_listening.place(x=220, y=200, width=150, height=40)

    # Initial glove image
    tmp_img = transform_img(cv2.imread("../assets/pics/gc.png"))
    glove_image = tk.Label(main_window, bg="#F1FAEE")
    glove_image.configure(image=tmp_img)

    glove_image.place(x=150, y=300)

    # Main process
    display_ports()
    main_window.protocol("WM_DELETE_WINDOW", kill_arduino_thread)
    main_window.mainloop()


if __name__ == '__main__':
    main()
