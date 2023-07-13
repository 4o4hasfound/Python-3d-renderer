import numpy as np
import math
import pygame

import Func

class vector:
    def __init__(self, pos):
        self.pos = np.array(pos)
     
        
class Triangle:
    def __init__(self, points):
        self.vectors = points
        self.color = [0, 0, 0]
        
    def get_normal(self, coords, verts):
        self.normal = Func.normal(verts[self.vectors[0]][0], verts[self.vectors[0]][1], verts[self.vectors[1]][0], verts[self.vectors[1]][1], verts[self.vectors[2]][0], verts[self.vectors[2]][1])
        
class Cam:
    def __init__(self, pos, rot, fov, width, height):
        self.pos = pos
        self.rot = rot
        self.fov = fov
        self.sin = [float(math.sin(i)) for i in self.rot]
        self.cos = [float(math.cos(i)) for i in self.rot]
        self.width = width
        self.height = height
        self.r = 0
        self.r_pressed = False
        
    def get3dcoord(self, coord):
        temp = Func.get3dcoord(coord[0], coord[1], coord[2], self.pos[0], self.pos[1], self.pos[2], self.cos[0], self.cos[1], self.cos[2], self.sin[0], self.sin[1], self.sin[2], (self.width / 2) * math.tan(self.fov / 2), self.width / 2, self.height / 2)
        return temp
    
    def get2dcoord(self, coord):
        temp = Func.get2dcoord(coord[0], coord[1], coord[2], (self.width / 2) * math.tan(self.fov / 2), self.width / 2, self.height / 2)
        return temp
    
    def events(self, event):
        if event.type == pygame.MOUSEMOTION:
            x, y = event.rel
            x /= 300
            y /= 300
            self.rot[0] -= y
            self.rot[1] += x
    
    def update(self, dt, key):
        s = dt * 15
        if key[pygame.K_LSHIFT]: self.pos[1] -= s + dt * 2
        if key[pygame.K_SPACE]: self.pos[1] += s + dt * 2

        x, y = s*math.sin(self.rot[1]), s*math.cos(self.rot[1])

        if key[pygame.K_w]: self.pos[0] -= x; self.pos[2] -= y;
        if key[pygame.K_s]: self.pos[0] += x; self.pos[2] += y
        if key[pygame.K_a]: self.pos[0] += y; self.pos[2] -= x
        if key[pygame.K_d]: self.pos[0] -= y; self.pos[2] += x
        self.sin = [float(math.sin(i)) for i in self.rot]
        self.cos = [float(math.cos(i)) for i in self.rot]
        if key[pygame.K_r] and self.r_pressed == False:
            self.r_pressed = True
            self.r += 1
            if self.r > 1: self.r = 0
        elif not key[pygame.K_r]: self.r_pressed = False
        
        if key[pygame.K_1]: self.fov += 0.01
        if key[pygame.K_2]:
            self.fov -= 0.01
            if self.fov <= 0: self.fov -= 0.01
        
