class Polygon:
    def __init__(self):
        self.points = []
        self.closed = False

    def add_point(self, point):
        if not self.closed:
            self.points.append(point)

    def close(self):
        if len(self.points) >= 3:
            self.closed = True

    def get_center(self):
        if not self.points:
            return 0, 0
        x_sum = sum(p[0] for p in self.points)
        y_sum = sum(p[1] for p in self.points)
        return x_sum // len(self.points), y_sum // len(self.points)

    def reset(self):
        self.points = []
        self.closed = False
