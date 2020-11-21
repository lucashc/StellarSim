import numpy as np
import matplotlib.animation as animation
import matplotlib.pyplot as plt

class Plane:
    def __init__(self, direction, support, e1, e2):
        self.direction = direction/np.linalg.norm(direction)
        self.support = support
        self.e1 = e1
        self.e2 = e2

    def project(self, points):
        localised = points - self.support
        return np.tensordot(localised, np.array([self.e2, self.e1]), axes=(1, 1))

class Raster:
    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y
        self.center = np.array([size_y//2, size_x//2])
        self.raster = np.zeros((size_y, size_x))

    def inbounds(self, points):
        return np.logical_and(np.all(points >= np.array([0, 0]), 1), np.all(points < np.array([self.size_y, self.size_x]),1))

    def fill(self, points, weights):
        new_points = (points + self.center).astype(int)
        mask = self.inbounds(new_points)
        X, Y = zip(*new_points[mask])
        self.raster[X, Y] = weights[mask]

    def get_image(self, coloring):
        return coloring(self.raster)

def animate(point_series, masses, plane, size_x, size_y):
    dpi = 100
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_aspect('equal')
    # com = (points*masses[..., np.newaxis])/np.sum(masses)
    raster = Raster(size_x, size_y)
    raster.fill(plane.project(point_series[0]), masses)
    normalise = lambda raster: (raster/np.max(raster))**(np.log(0.5)/(
        np.log(np.median(raster[raster != 0])) - np.log(np.max(raster))))
    im = ax.imshow(raster.get_image(normalise), cmap='gray', interpolation='nearest')
    im.set_clim([0,1])
    fig.set_size_inches([5,5])
    plt.tight_layout()

    def func(n):
        print(n)
        points = point_series[n]
        # com = (points*masses)/np.sum(masses)
        raster = Raster(size_x, size_y)
        raster.fill(plane.project(points), masses)
        im.set_data(raster.get_image(normalise))
        return im
    
    ani = animation.FuncAnimation(fig,func,frames=np.arange(len(point_series)), interval = 100)
    writer = animation.writers['ffmpeg'](fps=30)
    # ani.save('demo.mp4',writer=writer,dpi=dpi)
    plt.show()
    return ani
