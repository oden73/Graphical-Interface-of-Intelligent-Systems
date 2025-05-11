# Лабораторная работа №6 - Заполнение полигонов

## Задача

---

Разработать элементарный графический редактор, реализуюший построение полигонов
и их заполнение, используя алгоритм растровой развертки с упорядоченным списком ребер;
алгоритм растровой развертки с упорядоченным списком ребер, использующий список 
активных ребер; простой алгоритм заполнения с затравкой; построчный алгоритм заполнения
с затравкой. Выбор алгоритма задается из пункта меню и доступен через панель инструментов
"Алгоритмы заполнения полигонов". В редакторе должен быть предусмотрен режим отладки,
где отображается пошаговое решение.

## Ход работы

---

### Средства разработки
1. Язык программирования Python.
2. Встроенная библиотека PyQt5.

### Описание алгоритма

1. Пользователь с помощью левой кнопки мыши задает точки полигона.
2. При нажатии правой кнопкой мыши полигон замыкается, образуя единый объект, готовый к заполнению.
3. Алгоритм растровой развертки с упорядоченным списком ребер
   1. Определяются ребра полигона, игнорируются горизонтальные.
   2. Для каждого ребра вычисляется начальная и конечная высоты и инкремент для вычисления горизонтальной позиции.
   3. Ребра сортируются по минимальной высоте.
   4. Для каждой строки заполняются все пиксели между двумя пересекающимися ребрами, которые отображаются на текущей строке
4. Алгоритм растровой развертки с упорядоченным списком ребер, использующий список активных ребер
   1. Определяются ребра полигона, аналогично первому алгоритму. Вычисляются те же параметры.
   2. В процессе сканирования строк поддерживается список активных ребер, которые пересекаются с текущей горизонтальной линией. 
   3. Эти активные ребра сортируются по их текущей горизонтальной линии.
   4. Между каждой парой ребер происходит заливка пикселей.
   5. Этот процесс повторяется для каждой горизонтальной строки, пока не будут обработаны все ребра.
5. Простой алгоритм заполнения с затравкой
   1. Алгоритм начинает с начальной точки (сид), для автоматизации процесса выбора точки всегда выбирается центр полигона.
   2. Для каждого пикселя, которые еще не был залит (цвет отличается от цвета заливки), алгоритм меняет его цвет на нужный.
   3. После заливки текущего пикселя алгоритм добавляет в стек все соседние пиксели по четырем направлениям, если они еще не были залиты и если они принадлежат полигону.
   4. Процесс повторяется, пока стек не станет пустым.
6. Построчный алгоритм заполнения с затравкой
   1. Алгоритм начинает с начальной точки (как в предыдущем алгоритме).
   2. Алгоритм ищет на текущей строке непрерывные участки, которые можно заполнить, двигаясь влево и вправо от начальной точки, пока не встретятся пиксели другого цвета.
   3. После этого в стек добавляются пиксели из соседних строк, которые должны быть обработаны.
   4. Процесс повторяется, пока стек не станет пустым.

### Реализация основных частей кода

**Алгоритм растровой развертки с упорядоченным списком ребер**
```python
class EdgeTableScanlineFill(FillAlgorithm):
    def fill(self, polygon):
        if not polygon.closed:
            return

        edges = []
        points = polygon.points
        for i in range(len(points)):
            x0, y0 = points[i]
            x1, y1 = points[(i + 1) % len(points)]
            if y0 == y1:
                continue  # игнорируем горизонтальные
            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            edges.append({'y_min': y0, 'y_max': y1, 'x': x0, 'inv_slope': (x1 - x0) / (y1 - y0)})

        edges.sort(key=lambda e: (e['y_min'], e['x']))
        y = min(e['y_min'] for e in edges)
        y_max = max(e['y_max'] for e in edges)
        AET = []
        count = 0

        while y < y_max:
            for e in edges:
                if e['y_min'] == y:
                    AET.append(e)
            AET = [e for e in AET if e['y_max'] > y]
            AET.sort(key=lambda e: e['x'])

            for i in range(0, len(AET), 2):
                x_start = int(round(AET[i]['x']))
                x_end = int(round(AET[i+1]['x']))
                for x in range(x_start, x_end):
                    self.canvas.image.setPixel(x, y, QColor(0, 0, 255).rgb())

            if self.debug_mode:
                count += 1
                if count % 10 == 0:
                    self.canvas.setPixmap(QPixmap.fromImage(self.canvas.image))
                    QApplication.processEvents()
                    time.sleep(0.1)

            y += 1
            for e in AET:
                e['x'] += e['inv_slope']
```

**Алгоритм растровой развертки с упорядоченным списком ребер, использующий список активных ребер**
```python
class ActiveEdgeListFill(FillAlgorithm):
    def fill(self, polygon):
        if not polygon.closed:
            return

        edges = []
        points = polygon.points
        for i in range(len(points)):
            x0, y0 = points[i]
            x1, y1 = points[(i + 1) % len(points)]
            if y0 == y1:
                continue
            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            edges.append({'y_min': y0, 'y_max': y1, 'x': x0, 'inv_slope': (x1 - x0) / (y1 - y0)})

        scanline = min(e['y_min'] for e in edges)
        AET = []
        count = 0
        while True:
            for e in edges:
                if e['y_min'] == scanline:
                    AET.append(e)
            AET = [e for e in AET if e['y_max'] > scanline]
            AET.sort(key=lambda e: e['x'])

            if not AET:
                break

            for i in range(0, len(AET), 2):
                x_start = int(round(AET[i]['x']))
                x_end = int(round(AET[i+1]['x']))
                for x in range(x_start, x_end):
                    self.canvas.image.setPixel(x, scanline, QColor(255, 0, 0).rgb())

            if self.debug_mode:
                count += 1
                if count % 10 == 0:
                    self.canvas.setPixmap(QPixmap.fromImage(self.canvas.image))
                    QApplication.processEvents()
                    time.sleep(0.1)

            scanline += 1
            for e in AET:
                e['x'] += e['inv_slope']
```

**Простой алгоритм заполнения с затравкой**
```python
class SimpleSeedFill(FillAlgorithm):
    def fill(self, polygon):
        if not polygon.closed or not polygon.points:
            return

        seed = polygon.points[0]
        target_color = QColor(255, 255, 255).rgb()
        fill_color = QColor(0, 255, 0).rgb()

        stack = [seed]
        count = 0
        while stack:
            x, y = stack.pop()
            if self.canvas.image.pixel(x, y) != target_color:
                continue
            self.canvas.image.setPixel(x, y, fill_color)
            stack.extend([(x+1, y), (x-1, y), (x, y+1), (x, y-1)])

            if self.debug_mode:
                count += 1
                if count % 50 == 0:
                    self.canvas.setPixmap(QPixmap.fromImage(self.canvas.image))
                    QApplication.processEvents()
```

**Построчный алгоритм заполнения с затравкой**
```python
class LineSeedFill(FillAlgorithm):
    def fill(self, polygon):
        if not polygon.closed or not polygon.points:
            return

        seed = polygon.points[0]
        target_color = QColor(255, 255, 255).rgb()
        fill_color = QColor(255, 255, 0).rgb()

        stack = [seed]
        count = 0
        while stack:
            x, y = stack.pop()
            if self.canvas.image.pixel(x, y) != target_color:
                continue

            x_left = x
            while x_left > 0 and self.canvas.image.pixel(x_left - 1, y) == target_color:
                x_left -= 1
            x_right = x
            while x_right < self.canvas.image.width() - 1 and self.canvas.image.pixel(x_right + 1, y) == target_color:
                x_right += 1

            for xi in range(x_left, x_right + 1):
                self.canvas.image.setPixel(xi, y, fill_color)

            for nx in range(x_left, x_right + 1):
                for ny in [y - 1, y + 1]:
                    if 0 <= ny < self.canvas.image.height() and self.canvas.image.pixel(nx, ny) == target_color:
                        stack.append((nx, ny))

            if self.debug_mode:
                count += 1
                if count % 50 == 0:
                    self.canvas.setPixmap(QPixmap.fromImage(self.canvas.image))
                    QApplication.processEvents()
                    time.sleep(0.1)

```

### Результат работы программы

**Главное окно приложения**
![](../img/lw6/main_window.png)

**Заливка алгоритмом растровой развертки с упорядоченным списком ребер**
![](../img/lw6/edge_table_fill.png)

**Заливка алгоритмом растровой развертки с упорядоченным списком ребер, использующим список активных ребер**
![](../img/lw6/active_edge_fill.png)

**Заливка простым алгоритмом с затравкой**
![](../img/lw6/seed_fill.png)

**Заливка построчным алгоритмом с затравкой**
![](../img/lw6/scanline_seed_fill.png)
