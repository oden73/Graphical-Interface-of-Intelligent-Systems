import tkinter as tk
from tkinter import ttk
import math

from pixel_canvas import PixelCanvas


class LineDrawingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Графический редактор линий")
        self.geometry("800x600")

        self.start_point = None
        self.debug_mode = tk.BooleanVar(value=False)
        self.selected_algorithm = tk.StringVar(value="DDA")

        self.create_widgets()

    def create_widgets(self):
        left_frame = tk.Frame(self)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas = PixelCanvas(left_frame, pixel_size=5, bg="white")
        self.canvas.pack(pady=10, padx=10)
        self.canvas.bind("<Button-1>", self.canvas_click)

        right_frame = tk.Frame(self)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10)

        algorithm_frame = tk.LabelFrame(right_frame, text="Алгоритм")
        algorithm_frame.pack(fill=tk.X, pady=5)

        algorithms = [("ЦДА", "DDA"),
                      ("Брезенхем", "Bresenham"),
                      ("Ву", "Wu")]
        for text, value in algorithms:
            rb = tk.Radiobutton(algorithm_frame, text=text,
                                variable=self.selected_algorithm,
                                value=value)
            rb.pack(anchor=tk.W)

        debug_check = tk.Checkbutton(right_frame, text="Режим отладки",
                                     variable=self.debug_mode)
        debug_check.pack(pady=5)

        clear_btn = tk.Button(right_frame, text="Очистить", command=self.clear_canvas)
        clear_btn.pack(pady=5)

        self.table = ttk.Treeview(right_frame, show="headings")
        self.table.pack(fill=tk.BOTH, expand=True, pady=10)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.canvas.draw_grid()
        self.start_point = None
        self.clear_table()

    def clear_table(self):
        for item in self.table.get_children():
            self.table.delete(item)
        self.table["columns"] = []
        for col in self.table["columns"]:
            self.table.heading(col, text="")
            self.table.column(col, width=0)

    def canvas_click(self, event):
        pixel_x = event.x // self.canvas.pixel_size
        pixel_y = event.y // self.canvas.pixel_size

        if not self.start_point:
            self.start_point = (pixel_x, pixel_y)
        else:
            self.draw_line(self.start_point, (pixel_x, pixel_y))
            self.start_point = None

    def draw_line(self, start, end):
        self.clear_table()
        algorithm = self.selected_algorithm.get()

        if algorithm == "DDA":
            steps = self.dda(start, end)
        elif algorithm == "Bresenham":
            steps = self.bresenham(start, end)
        elif algorithm == "Wu":
            steps = self.wu(start, end)

        columns = {
            "DDA": ["i", "x", "y", "Plot"],
            "Bresenham": ["i", "e", "x", "y", "e_new", "Plot"],
            "Wu": ["i", "x", "y", "Plot"]
        }[algorithm]

        self.table["columns"] = columns
        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=60)

        if self.debug_mode.get():
            self.animate_drawing(steps, algorithm)
        else:
            for step in steps:
                self.draw_step(step, algorithm)

    def animate_drawing(self, steps, algorithm):
        if not steps:
            return

        step = steps.pop(0)
        self.draw_step(step, algorithm)
        self.add_table_row(step, algorithm)

        if steps:
            self.after(500, lambda: self.animate_drawing(steps, algorithm))

    def draw_step(self, step, algorithm):
        x = step.get("x")
        y = step.get("y")
        color = step.get("color", "black")
        intensity = step.get("intensity", 1.0)

        if algorithm == "Wu":
            gray = int(255 * (1 - intensity))
            color = f"#{gray:02x}{gray:02x}{gray:02x}"

        self.canvas.draw_pixel(x, y, color)

    def add_table_row(self, step, algorithm):
        values = []
        if algorithm == "DDA":
            values = [step["i"], step["x"], step["y"], f"({step['x']}, {step['y']})"]
        elif algorithm == "Bresenham":
            values = [step["i"], step["e"], step["x"], step["y"],
                      step["e_new"], f"({step['x']}, {step['y']})"]
        elif algorithm == "Wu":
            values = [step["i"], step["x"], step["y"], f"({step['x']}, {step['y']})"]

        self.table.insert("", tk.END, values=values)

    def dda(self, start, end):
        x1, y1 = start
        x2, y2 = end
        dx = x2 - x1
        dy = y2 - y1
        steps = max(abs(dx), abs(dy))

        if steps == 0:
            return []

        x_inc = dx / steps
        y_inc = dy / steps

        x = x1
        y = y1
        result = []

        for i in range(steps + 1):
            result.append({
                "i": i,
                "x": round(x),
                "y": round(y)
            })
            x += x_inc
            y += y_inc

        return result

    def bresenham(self, start, end):
        x1, y1 = start
        x2, y2 = end
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        steep = dy > dx

        if steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2
            dx, dy = dy, dx

        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        dx = x2 - x1
        dy = abs(y2 - y1)
        error = dx / 2
        ystep = 1 if y1 < y2 else -1
        y = y1

        result = []
        i = 0

        for x in range(x1, x2 + 1):
            if steep:
                plot_x = y
                plot_y = x
            else:
                plot_x = x
                plot_y = y

            result.append({
                "i": i,
                "e": error,
                "x": plot_x,
                "y": plot_y,
                "e_new": error - dy
            })

            error -= dy
            if error < 0:
                y += ystep
                error += dx
            i += 1

        return result

    def wu(self, start, end):
        x1, y1 = start
        x2, y2 = end
        result = []

        def ipart(x):
            return math.floor(x)

        def fpart(x):
            return x - math.floor(x)

        def rfpart(x):
            return 1 - fpart(x)

        dx = x2 - x1
        dy = y2 - y1
        steep = abs(dy) > abs(dx)

        if steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2
            dx, dy = dy, dx

        if x2 < x1:
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        gradient = dy / dx if dx != 0 else 1.0

        xend = round(x1)
        yend = y1 + gradient * (xend - x1)
        xgap = rfpart(x1 + 0.5)
        xpxl1 = xend
        ypxl1 = ipart(yend)

        result.append({
            "i": 0,
            "x": xpxl1 if not steep else ypxl1,
            "y": ypxl1 if not steep else xpxl1,
            "intensity": rfpart(yend) * xgap
        })

        result.append({
            "i": 0,
            "x": xpxl1 if not steep else ypxl1 + 1,
            "y": ypxl1 + 1 if not steep else xpxl1,
            "intensity": fpart(yend) * xgap
        })

        intery = yend + gradient

        xend = round(x2)
        yend = y2 + gradient * (xend - x2)
        xgap = fpart(x2 + 0.5)
        xpxl2 = xend
        ypxl2 = ipart(yend)

        result.append({
            "i": x2 - x1,
            "x": xpxl2 if not steep else ypxl2,
            "y": ypxl2 if not steep else xpxl2,
            "intensity": rfpart(yend) * xgap
        })

        result.append({
            "i": x2 - x1,
            "x": xpxl2 if not steep else ypxl2 + 1,
            "y": ypxl2 + 1 if not steep else xpxl2,
            "intensity": fpart(yend) * xgap
        })

        index = 1
        for x in range(xpxl1 + 1, xpxl2):
            result.append({
                "i": index,
                "x": x if not steep else ipart(intery),
                "y": ipart(intery) if not steep else x,
                "intensity": rfpart(intery)
            })

            result.append({
                "i": index,
                "x": x if not steep else ipart(intery) + 1,
                "y": ipart(intery) + 1 if not steep else x,
                "intensity": fpart(intery)
            })

            intery += gradient
            index += 1

        return sorted(result, key=lambda s: s["i"])
