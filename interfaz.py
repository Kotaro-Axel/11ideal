from tkinter import *
import tkinter as tk
from ui import main
def send_data():
  prob_info = prob.get()
  generaciones_info = generaciones.get()
  main(prob_info, generaciones_info)

if __name__ == "__main__": 
    ventana = Tk()
    ventana.geometry("1200x600")
    ventana.title("Algoritmo génetico canonico")
    ventana.resizable(False,False)
    frame_izquierda = tk.Frame(ventana, width=700, height=750, pady=10, padx=10)
    frame_derecha = tk.Frame(ventana, width=700, height=750, pady=10, padx=10)
    frame_derecha.pack(side="right")
    frame_izquierda.pack(side="left")
    ventana.config(background = "#FFFFFF")
    prob_label = Label(frame_izquierda, text = "probabilidad de mutacion")
    prob_label.place(x = 22, y = 310)
    generaciones_label = Label(frame_izquierda, text = "Numero de generaciones")
    generaciones_label.place(x = 22, y = 370)
    prob = IntVar()
    generaciones = IntVar()
    prob_entry = Entry(frame_izquierda, textvariable = prob, width = 40)
    generaciones_entry = Entry(frame_izquierda, textvariable = generaciones, width = 40)
    prob_entry.place(x = 22, y = 340)
    generaciones_entry.place(x = 22, y = 400)
    submit_btn = Button(frame_izquierda, text="Continuar", command = send_data)
    submit_btn.place(x = 22, y = 480)
    ventana.mainloop()