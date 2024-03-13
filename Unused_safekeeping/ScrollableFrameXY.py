import tkinter as tk

class ScrollableFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        # Create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        vscrollbar.grid(row=0, column=1, sticky='ns')
        hscrollbar = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        hscrollbar.grid(row=1, column=0, sticky='ew')

        self.canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                                yscrollcommand=vscrollbar.set,
                                xscrollcommand=hscrollbar.set, width=700, height=300)
        self.canvas.grid(row=0, column=0, sticky='nsew')

        vscrollbar.config(command=self.canvas.yview)
        hscrollbar.config(command=self.canvas.xview)

        # Reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # Create a frame inside the canvas which will be scrolled with it
        self.interior = tk.Frame(self.canvas)
        self.canvas.create_window(0, 0, window=self.interior, anchor=tk.NW)

        self.interior.bind('<Configure>', self._configure_interior)
        self.canvas.bind('<Configure>', self._configure_canvas)

    def _configure_interior(self, event):
        # Update the scrollbars to match the size of the inner frame
        size = (700, 300)
        self.canvas.config(scrollregion="0 0 %s %s" % size)
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # Update the canvas's width to fit the inner frame
            self.canvas.config(width=700)

    def _configure_canvas(self, event):
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # Update the inner frame's width to fill the canvas
            self.canvas.itemconfigure(self.interior, width=700)