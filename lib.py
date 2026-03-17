import pygame
import numpy as np

class Hormiga:
    def __init__(self, x, y, paso=5):
        self.x = x
        self.y = y
        self.angulo = 0
        self.paso = paso
        self.frames = []
        for i in range(1,4):
            img = pygame.image.load(f"imagenes/hormiga{i}.png")
            self.frames.append(img)

    def mover(self, dx, dy):
        if np.random.uniform(0,1)<0.33:
            self.angulo += np.random.randint(-10, 10)
            return
        l = np.linalg.norm([dx,dy])
        if l>0.4*self.paso:
            self.x += self.paso*dx/l
            self.y += self.paso*dy/l
        else:
            self.angulo += np.random.randint(-10,10)
        rad = 0
        if dx == 0:
            if dy < 0:
                rad = -np.pi/2
            elif 0 < dy:
                rad = np.pi/2
        else:
            rad = np.arctan(abs(dy)/abs(dx))
            if dx < 0:
                if dy < 0:
                    rad = np.pi + rad
                elif 0 < dy:
                    rad = np.pi - rad
                else:
                    rad = np.pi
            else:
                if dy < 0:
                    rad = -rad

        rad = np.pi/2 - rad
        self.angulo = int(180*rad/np.pi)

    def destino(self, x, y):
        dx = x - self.x
        dy = y - self.y
        self.mover(dx, dy)
        return np.linalg.norm([dx,dy])> 2*self.paso

    def mostrar(self, ventana):
        idx = np.random.randint(0,2)
        img = pygame.transform.rotate(
            self.frames[idx],
            self.angulo
        )
        ventana.blit(img, (self.x, self.y))

class Peloton:
    def __init__(self, num, ventana, txt=None):
        self.destinos = []
        self.en_movimiento = True
        self.hormigas = []
        w, h = ventana.get_size()
        num = min(num, 30_000)

        for _ in range(num):
            x = np.random.randint(0, w)
            y = np.random.randint(0, h)
            hormiga = Hormiga(x, y)
            self.hormigas.append(hormiga)
        if txt:
            self.cargar_destinos(txt)

    def cargar_destinos(self, txt):
        if txt is None:
            return
        self.destinos.clear()
        with open(txt, "r") as f:
            for i, line in enumerate(f):
                if i>= len(self): return
                linea = line.strip().split()
                if len(linea) == 2:
                    x, y = linea
                    punto = (int(x), int(y))
                    self.destinos.append(punto)

    def mover(self):
        acumulador = False
        for i, hormiga in enumerate(self.hormigas):
            x, y = self.destinos[i]
            estado = hormiga.destino(x,y)
            acumulador = acumulador or estado

        self.en_movimiento = acumulador

    def mostrar(self, ventana):
        for hormiga in self.hormigas:
            hormiga.mostrar(ventana)

    def __len__(self):
        return len(self.hormigas)


class Destinos:
    def __init__(self):
        self.lista = [
            "mensajes/bienvenidos.txt",
            "mensajes/al_curso.txt",
            "mensajes/poo.txt",
            "mensajes/fin.txt"]

    def __iter__(self):
        self.idx = 0
        return self

    def __next__(self):
        if self.idx < len(self):
            t = self[self.idx]
            self.idx += 1
        else:
            t = None
        return t

    def __getitem__(self, item):
        return self.lista[item]

    def __len__(self):
        return len(self.lista)
