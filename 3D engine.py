import pygame
import numpy as np
import sys #sus
import copy
import math

import Camera
import Func

Verts = []

def getobj(filename):
    ind = []
    triangles = []
    data = None
    with open(filename, 'r') as f:
        data = f.readline()
        while data:
            data = data.rstrip("\n").split(" ")
            if data[0] == 'v':
                Verts.append([int(float(data[1])),int(float(data[2])),int(float(data[3]))])
            elif data[0] == 'f':
                v = []
                t = []
                n = []
                for i in range(3):
                    l = data[i + 1].split('/')
                    v.append(int(l[0]))
                    t.append(int(l[1]))
                    n.append(int(l[2]))
                ind.append([v, t, n])
            data = f.readline()
    for points in ind:
        v = []
        for i in points[0]:
            v.append(i - 1)
        triangles.append(Camera.Triangle(v))
    return triangles

width, height = 1200, 700

cam = Camera.Cam([0.0, 0.0, 0.0], [10.0, 0.0, 0.0], 90, width, height)

triangles = getobj("Deer.obj")


pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

pygame.event.get()
pygame.mouse.get_rel()
pygame.mouse.set_visible(0)
pygame.event.set_grab(1)
angle_y = 0

while True:
    dt = clock.tick() / 1000
    coords = copy.deepcopy(Verts)
    coords3d = copy.deepcopy(Verts)
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        cam.events(event)
    for i in range(len(coords)):
        c = coords[i]
        c = cam.get3dcoord(c)
        coords[i] = cam.get2dcoord(c)
        coords3d[i] = c
    tris = sorted(triangles, key=lambda e: coords3d[e.vectors[0]][2] + coords3d[e.vectors[1]][2] + coords3d[e.vectors[2]][2], reverse=1)
    for tri in triangles:
        tri.get_normal(coords, coords)
        # temp = Func.clip(0.0, 0.0, 0.1, 0.0, 0.0, -1.0, coords3d[tri.vectors[0]][0], coords3d[tri.vectors[0]][1], coords3d[tri.vectors[0]][2], coords3d[tri.vectors[1]][0], coords3d[tri.vectors[1]][1], coords3d[tri.vectors[1]][2], coords3d[tri.vectors[2]][0], coords3d[tri.vectors[2]][1], coords3d[tri.vectors[2]][2])
        # if coords3d[tri.vectors[0]][2] < 0 and coords3d[tri.vectors[1]][2] < 0 and coords3d[tri.vectors[2]][2] < 0:
        if (True):
            # extra = []
            # if temp[0] >= 1:
            #     extra.append([cam.get2dcoord(cam.get3dcoord([temp[1], temp[2], temp[3]])), cam.get2dcoord(cam.get3dcoord([temp[4], temp[5], temp[6]])), cam.get2dcoord(cam.get3dcoord([temp[7], temp[8], temp[9]]))])
            # if temp[0] == 2:
            #     extra.append([cam.get2dcoord(cam.get3dcoord([temp[10], temp[11], temp[12]])), cam.get2dcoord(cam.get3dcoord([temp[13], temp[14], temp[15]])), cam.get2dcoord(cam.get3dcoord([temp[16], temp[17], temp[18]]))])
            coord1 = coords[tri.vectors[0]]
            coord2 = coords[tri.vectors[1]]
            coord3 = coords[tri.vectors[2]]
            if cam.r == 0:
                pygame.draw.line(screen, (0, 0, 0), (int(coord1[0]), int(coord1[1])), (int(coord2[0]), int(coord2[1])))
                pygame.draw.line(screen, (0, 0, 0), (int(coord2[0]), int(coord2[1])), (int(coord3[0]), int(coord3[1])))
                pygame.draw.line(screen, (0, 0, 0), (int(coord3[0]), int(coord3[1])), (int(coord1[0]), int(coord1[1])))
            elif cam.r == 1:
                try:
                    pygame.draw.polygon(screen, tri.color, [coord1, coord2, coord3])
                except:
                    pass
            # coord1 = tri[0]
            # coord2 = tri[1]
            # coord3 = tri[2]
            # if cam.r == 0:
            #     pygame.draw.line(screen, (0, 0, 0), (int(coord1[0]), int(coord1[1])), (int(coord2[0]), int(coord2[1])))
            #     pygame.draw.line(screen, (0, 0, 0), (int(coord2[0]), int(coord2[1])), (int(coord3[0]), int(coord3[1])))
            #     pygame.draw.line(screen, (0, 0, 0), (int(coord3[0]), int(coord3[1])), (int(coord1[0]), int(coord1[1])))
            # elif cam.r == 1:
            #     try:
            #         pygame.draw.polygon(screen, tri.color, [coord1, coord2, coord3])
            #     except:
            #         pass
    pygame.display.flip()
    
    key = pygame.key.get_pressed()
    cam.update(dt, key)

# for tri in triangles:
#     p1 = Verts[tri.vectors[0]]
#     p2 = Verts[tri.vectors[1]]
#     p3 = Verts[tri.vectors[2]]
#     p1 = cam.get2dcoord(cam.get3dcoord(p1))
#     p2 = cam.get2dcoord(cam.get3dcoord(p2))
#     p3 = cam.get2dcoord(cam.get3dcoord(p3))
#     print(f"{p1[0]}, {p1[1]} {p2[0]}, {p2[1]} {p3[0]}, {p3[1]}")