import numba as nb
import numpy as np

@nb.njit()
def get3dcoord(coord1: float, coord2: float, coord3: float, p1: float, p2: float, p3: float, cosx: float, cosy: float, cosz: float, sinx: float, siny: float, sinz: float, ez: int, hwidth: int, hheight: int):
    mx = coord1 - p1
    my = coord2 - p2
    mz = coord3 - p3
    dx = cosy * (sinz * my + cosz * mx) - siny * mz
    dy = sinx * (cosy * mz + siny * (sinz * my + cosz * mx)) + cosx * (cosz * my + sinz * mx)
    dz = cosx * (cosy * mz + siny * (sinz * my + cosz * mx)) - sinx * (cosz * my + sinz * mx)
    return [dx, dy, dz]

@nb.njit()
def get2dcoord(dx: float, dy: float, dz: float, ez: float, hwidth: int, hheight: int):
    if dz == 0: return [hwidth, hheight]
    x = hwidth +  ez * dx / dz
    y = hheight + ez * dy / dz
    return [x, y]

@nb.njit()
def normal(p1x: float, p1y: float, p2x: float, p2y: float, p3x: float, p3y: float):
    line1x = p2x - p1x
    line1y = p2y - p1y
    line2x = p3x - p2x
    line2y = p3y - p2y
    normalz = line1x * line2y - line1y * line2x
    return normalz

@nb.njit()
def vector_intersect(sx: float, sy: float, sz: float, ex: float, ey: float, ez: float, plane_px: float, plane_py: float, plane_pz: float, plane_nx: float, plane_ny: float, plane_nz: float):
    plane_d = -(plane_nx * plane_px + plane_ny * plane_py + plane_nz * plane_pz)
    ad = (plane_nx * sx + plane_ny * sy + plane_nz * sz)
    bd = (plane_nx * ex + plane_ny * ey + plane_nz * ez)
    t = (-plane_d - ad) / (bd - ad)
    stex, stey, stez = ex - sx, ey - sy, ez - sz # line start to end
    ltix, ltiy, ltiz = stex * t, stey * t, stez * t # line to intersect
    return [sx + ltix, sy + ltiy, sz + ltiz]
    

@nb.njit()
def dist_on_plane(x: float, y: float, z: float, plane_px: float, plane_py: float, plane_pz: float, plane_nx: float, plane_ny: float, plane_nz: float):
    return (plane_nx * x + plane_ny * y + plane_nz * z - (plane_nx * plane_px + plane_ny * plane_py + plane_nz * plane_pz))


@nb.jit()
def clip(plane_px: float, plane_py: float, plane_pz: float, plane_nx: float, plane_ny: float, plane_nz: float, tri1x: float, tri1y: float, tri1z: float, tri2x: float, tri2y: float, tri2z: float, tri3x: float, tri3y: float, tri3z: float):
    inpoint_count, outpoint_count = 0, 0
    d0 = dist_on_plane(tri1x, tri1y, tri1z, plane_px, plane_py, plane_pz, plane_nx, plane_ny, plane_nz)
    d1 = dist_on_plane(tri2x, tri2y, tri2z, plane_px, plane_py, plane_pz, plane_nx, plane_ny, plane_nz)
    d2 = dist_on_plane(tri3x, tri3y, tri3z, plane_px, plane_py, plane_pz, plane_nx, plane_ny, plane_nz)
    
    inpoint = np.array([0, 0, 0])
    outpoint = np.array([0, 0, 0])
    
    if d0 >= 0: inpoint_count += 1; inpoint[inpoint_count - 1] = 0
    else: outpoint_count += 1; outpoint[outpoint_count - 1] = 0
    
    if d1 >= 0: inpoint_count += 1; inpoint[inpoint_count - 1] = 1
    else: outpoint_count += 1; outpoint[outpoint_count - 1] = 1
    
    if d2 >= 0: inpoint_count += 1; inpoint[inpoint_count - 1] = 2
    else: outpoint_count += 1; outpoint[outpoint_count - 1] = 2
    
    if inpoint_count == 0:
        return [-1]
    
    if inpoint_count == 3:
        return [0]
    
    if inpoint_count == 1 and outpoint_count == 2:
        p1 = np.array([0.0, 0.0, 0.0])
        p2 = np.array([0.0, 0.0, 0.0])
        p3 = np.array([0.0, 0.0, 0.0])
        if inpoint[0] == 0:
            p1[0] = tri1x
            p1[1] = tri1y
            p1[2] = tri1z
        elif inpoint[0] == 1:
            p1[0] = tri2x
            p1[1] = tri2y
            p1[2] = tri2z
        elif inpoint[0] == 2:
            p1[0] = tri3x
            p1[1] = tri3y
            p1[2] = tri3z
            
        if outpoint[0] == 0:
            p2 = np.array(vector_intersect(p1[0], p1[1], p1[2], tri1x, tri1y, tri1z, plane_px, plane_py, plane_pz, plane_nx, plane_ny, plane_nz))
        elif outpoint[0] == 1:
            p2 = np.array(vector_intersect(p1[0], p1[1], p1[2], tri2x, tri2y, tri2z, plane_px, plane_py, plane_pz, plane_nx, plane_ny, plane_nz))
        elif outpoint[0] == 2:
            p2 = np.array(vector_intersect(p1[0], p1[1], p1[2], tri3x, tri3y, tri3z, plane_px, plane_py, plane_pz, plane_nx, plane_ny, plane_nz))
            
        if outpoint[1] == 0:
            p3 = np.array(vector_intersect(p1[0], p1[1], p1[2], tri1x, tri1y, tri1z, plane_px, plane_py, plane_pz, plane_nx, plane_ny, plane_nz))
        elif outpoint[1] == 1:
            p3 = np.array(vector_intersect(p1[0], p1[1], p1[2], tri2x, tri2y, tri2z, plane_px, plane_py, plane_pz, plane_nx, plane_ny, plane_nz))
        elif outpoint[1] == 2:
            p3 = np.array(vector_intersect(p1[0], p1[1], p1[2], tri3x, tri3y, tri3z, plane_px, plane_py, plane_pz, plane_nx, plane_ny, plane_nz))

        return [1, p1[0], p1[1], p1[2], p2[0], p2[1], p2[2], p3[0], p3[1], p3[2]]
    
    if inpoint_count == 2 and outpoint_count == 1:
        p1 = np.array([0.0, 0.0, 0.0])
        p2 = np.array([0.0, 0.0, 0.0])
        p3 = np.array([0.0, 0.0, 0.0])
        p4 = np.array([0.0, 0.0, 0.0])
        p5 = np.array([0.0, 0.0, 0.0])
        p6 = np.array([0.0, 0.0, 0.0])
        
        if inpoint[0] == 0:
            p1[0] = tri1x
            p1[1] = tri1y
            p1[2] = tri1z
        elif inpoint[0] == 1:
            p1[0] = tri2x
            p1[1] = tri2y
            p1[2] = tri2z
        elif inpoint[0] == 2:
            p1[0] = tri3x
            p1[1] = tri3y
            p1[2] = tri3z
        
        if inpoint[1] == 0:
            p2[0] = tri1x
            p2[1] = tri1y
            p2[2] = tri1z
            p4[0] = p2[0]
            p4[1] = p2[1]
            p4[2] = p2[2]
        elif inpoint[1] == 1:
            p2[0] = tri2x
            p2[1] = tri2y
            p2[2] = tri2z
            p4[0] = p2[0]
            p4[1] = p2[1]
            p4[2] = p2[2]
        elif inpoint[1] == 2:
            p2[0] = tri3x
            p2[1] = tri3y
            p2[2] = tri3z
            p4[0] = p2[0]
            p4[1] = p2[1]
            p4[2] = p2[2]
            
        if outpoint[0] == 0:
            p3 = np.array(vector_intersect(p1[0], p1[1], p1[2], tri1x, tri1y, tri1z, plane_px, plane_py, plane_pz, plane_nx, plane_ny, plane_nz))
            p6 = np.array(vector_intersect(p2[0], p2[1], p2[2], tri1x, tri1y, tri1z, plane_px, plane_py, plane_pz, plane_nx, plane_ny, plane_nz))
        elif outpoint[0] == 1:
            p3 = np.array(vector_intersect(p1[0], p1[1], p1[2], tri2x, tri2y, tri2z, plane_px, plane_py, plane_pz, plane_nx, plane_ny, plane_nz))
            p6 = np.array(vector_intersect(p2[0], p2[1], p2[2], tri2x, tri2y, tri2z, plane_px, plane_py, plane_pz, plane_nx, plane_ny, plane_nz))
        elif outpoint[0] == 2:
            p3 = np.array(vector_intersect(p1[0], p1[1], p1[2], tri3x, tri3y, tri3z, plane_px, plane_py, plane_pz, plane_nx, plane_ny, plane_nz))
            p6 = np.array(vector_intersect(p2[0], p2[1], p2[2], tri3x, tri3y, tri3z, plane_px, plane_py, plane_pz, plane_nx, plane_ny, plane_nz))
        p5 = p3
        return [2, p1[0], p1[1], p1[2], p2[0], p2[1], p2[2], p3[0], p3[1], p3[2], p4[0], p4[1], p4[2], p5[0], p5[1], p5[2], p6[0], p6[1], p6[2]]