import tkinter as tk


class PixelCanvas(tk.Canvas):
    def __init__(self, master, pixel_size=5, **kwargs):
        self.pixel_size = pixel_size
        self.width = 100
        self.height = 100
        super().__init__(master,
                         width=self.width * pixel_size,
                         height=self.height * pixel_size,
                         **kwargs)
        self.grid_visible = True
        self.draw_grid()

    def draw_grid(self):
        for i in range(self.width + 1):
            x = i * self.pixel_size
            self.create_line(x, 0, x, self.height * self.pixel_size, fill="gray80")
        for i in range(self.height + 1):
            y = i * self.pixel_size
            self.create_line(0, y, self.width * self.pixel_size, y, fill="gray80")

    def draw_pixel(self, x, y, color="black"):
        x1 = x * self.pixel_size
        y1 = y * self.pixel_size
        self.create_rectangle(x1, y1,
                              x1 + self.pixel_size,
                              y1 + self.pixel_size,
                              fill=color, outline="")

