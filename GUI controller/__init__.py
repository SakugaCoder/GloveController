import serial
import serial.tools.list_ports
import tkinter as tk
import threading

main_window = tk.Tk()
current_option = tk.StringVar(main_window)
arduino_thread = None
window_is_alive = True


def kill_arduino_thread():
    global window_is_alive
    global arduino_thread
    global main_window
    print("Saliendo")
    window_is_alive = False
    main_window.destroy()
    arduino_thread.join()


def start_listening():
    global window_is_alive
    if current_option.get() != "Select port":
        port_selected = current_option.get().split("-")[0].strip()
        with serial.Serial(port_selected) as ser:
            while window_is_alive == True:
                val = ser.readline()
                print(val.decode('utf-8'))
                print(type(val))
            ser.close()
            print("Good bye")


def init_thread():
    global arduino_thread
    arduino_thread = threading.Thread(target=start_listening)
    arduino_thread.start()


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
        select.place(x=170, y=100, width=300)


def main():
    global arduino_thread, window_is_alive

    window_title = "Glove Controller"
    width, height = 600, 600

    main_window.title(window_title)
    main_window.geometry(f"{width}x{height}")

    title_label = tk.Label(master=main_window, text="Glove Controller", font=('Open Sans', 32))
    title_label.place(x=150, y=20)

    current_option.set("Select port")

    btn_start_listening = tk.Button(master=main_window, text="Listen", command=init_thread)
    btn_start_listening.place(x=220, y=200, width=150, height=40)

    display_ports()
    main_window.protocol("WM_DELETE_WINDOW", kill_arduino_thread)
    main_window.mainloop()


if __name__ == '__main__':
    main()
