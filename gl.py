import struct

"""
Bryann Alfaro 19372
SR2 - GRAFICAS POR COMPUTADORA
References for conversions:
https://stackoverflow.com/questions/10848990/rgb-values-to-0-to-1-scale
https://docs.microsoft.com/en-us/windows/win32/opengl/glviewport

PUNTOS REALIZADOS:

    (100 puntos) Deben crear una función glLine(x0, y0, x1, y1) que se utilice para dibujar una línea recta de (x0, y0) a (x1, y1)
        x0, y0, x1, y1 deben estar en el rango -1 a 1 al igual que glPoint

"""
def char(c):
    return struct.pack('=c',c.encode('ascii'))

def word(w):
    #short
    return struct.pack('=h',w)

def dword(d):
    #long
    return struct.pack('=l',d)

#setting the function to get color with bytes
def color(r,g,b):
    return bytes([b,g,r])

BLACK = color(0,0,0)
WHITE = color(255,255,255)

class Renderer(object):
    def __init__(self):
        self.default_color = color(0,0,139)
        self.cl_color = BLACK

    def point(self, x, y):
        self.framebuffer[y][x] =self.default_color



    def glInit(self):
        pass

    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height
        self.framebuffer = []

    def glViewPort(self, x, y, width, height):
        self.vp_x = x
        self.vp_y = y
        self.vp_width = width
        self.vp_height = height

    #Fill the bitmap
    def glClear(self):
        self.framebuffer = [
            [self.cl_color for x in range(self.width)] for y in range(self.height)
            ]

    def glClearColor(self, r,g,b):
        self.cl_color = color(int(r*255),int(g*255),int(b*255))
        self.glClear()

    def glVertex(self,x,y):
        #formula get from microsoft glViewport function
        x_pos = int((x+1)*(self.vp_width/2)+self.vp_x)
        y_pos = int((y+1)*(self.vp_height/2)+self.vp_y)
        self.point(x_pos,y_pos)

    #change color of vertex
    def glColor(self, r,g,b):
        self.default_color = color(int(r*255),int(g*255),int(b*255))

    #Using class implementation
    def line(self,x0,y0,x1,y1):
        x0 = int((x0+1)*(self.vp_width/2)+self.vp_x)
        y0 = int((y0+1)*(self.vp_height/2)+self.vp_y)
        x1 = int((x1+1)*(self.vp_width/2)+self.vp_x)
        y1 = int((y1+1)*(self.vp_height/2)+self.vp_y)

        dy = abs(y1-y0)
        dx = abs(x1-x0)

        steep = dy>dx
        #en caso de pendiente mayor a 1
        if steep:
            x0,y0 = y0,x0
            x1,y1 = y1,x1

            dy = abs(y1-y0)
            dx = abs(x1-x0)

        #en caso que el segundo valor sea menor que el primero
        if x1<x0:
            x0,x1 =x1,x0
            y0,y1 = y1,y0

            dy = abs(y1-y0)
            dx = abs(x1-x0)

        offset = 0 *2*dx
        threshold = 0.5 *2*dx
        y = y0

        points = []
        for x in range(x0,x1+1):
            if steep:
                points.append((y,x))

            else:
                points.append((x,y))

            offset += (dy)*2
            if offset >= threshold:

                y +=1 if y0<y1 else -1
                threshold +=1 *2* dx

            for pointf in points:
                self.point(*pointf)

    def glFinish(self, filename):
        #bw means binary write
        f = open(filename, 'bw')
        #file header
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14+40+ 3*(self.width*self.height)))
        f.write(dword(0))
        f.write(dword(14+40))

        #info header
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(3*(self.width*self.height)))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        #bitmap
        for y in range(self.height):
            for x in range(self.width):
                f.write(self.framebuffer[y][x])

        f.close()