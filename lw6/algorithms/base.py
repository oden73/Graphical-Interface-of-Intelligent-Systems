class FillAlgorithm:
    def __init__(self, canvas, debug_mode=False):
        self.canvas = canvas
        self.debug_mode = debug_mode

    def fill(self, polygon):
        raise NotImplementedError
