from __future__ import print_function
import matplotlib
import numpy as np

matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation

import tkinter as tk
from tkinter import ttk


a = Figure(figsize=(4, 4))
plot_a = a.add_subplot(111)
plot_a.set_xlim([0, 2*np.pi])
plot_a.set_ylim([-1, 1])
lna, = plot_a.plot([], [], color='orange', lw=5)

b = Figure(figsize=(4, 4))
plot_b = b.add_subplot(111)
plot_b.set_xlim([0, 2*np.pi])
plot_b.set_ylim([-1, 1])

lnb, = plot_b.plot([], [], color='olive', lw=5)

x = np.linspace(0, 2*np.pi, 1024)


def updateGraphsA(i):
    lna.set_xdata(x)
    lna.set_ydata(np.sin(x + i * np.pi / 10))
    print('in A')

def updateGraphsB(i):
    lnb.set_xdata(x)
    lnb.set_ydata(np.sin(x - i * np.pi / 10))

    print('in B')


class TransientAnalysis(tk.Tk):

    def __init__(self, *args, **kwargs):
        self._running_anim = None
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Transient Analysis GUI: v1.0")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (GraphPageA, GraphPageB):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(GraphPageA)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()
        frame.canvas.draw_idle()


class GraphPageA(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        button1 = ttk.Button(self, text="Show Graph B",
                             command=(
                                 lambda: controller.show_frame(GraphPageB)))
        button1.grid(row=1, column=0, pady=20, padx=10, sticky='w')

        canvasA = FigureCanvasTkAgg(a, self)
        canvasA.show()
        canvasA.get_tk_widget().grid(
            row=1, column=1, pady=20, padx=10, sticky='nsew')
        self.canvas = canvasA


class GraphPageB(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        button1 = ttk.Button(self, text="Show Graph A",
                             command=(
                                 lambda: controller.show_frame(GraphPageA)))

        button1.grid(row=1, column=0, pady=20, padx=10, sticky='w')

        canvasB = FigureCanvasTkAgg(b, self)
        canvasB.show()
        canvasB.get_tk_widget().grid(
            row=1, column=1, pady=20, padx=10, sticky='nsew')
        self.canvas = canvasB


app = TransientAnalysis()
app.geometry("800x600")
aniA = animation.FuncAnimation(a, updateGraphsA, interval=1000, blit=False)
aniB = animation.FuncAnimation(b, updateGraphsB, interval=1000, blit=False)

app.mainloop()