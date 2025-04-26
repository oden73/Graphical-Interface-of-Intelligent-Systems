class FileLoader:
    @staticmethod
    def load(file_path):
        vertices = []
        edges = []

        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                if line.startswith('v '):
                    parts = line.split()
                    if len(parts) != 4:
                        raise ValueError('Неверный формат файла')

                    x, y, z = map(float, parts[1:])
                    vertices.append((x, y, z, 1.0))
                elif line.startswith('l '):
                    parts = line.split()
                    if len(parts) != 3:
                        raise ValueError('Неверный формат файла')

                    v1, v2 = int(parts[1]) - 1, int(parts[2]) - 1
                    edges.append((v1, v2))

        return vertices, edges
