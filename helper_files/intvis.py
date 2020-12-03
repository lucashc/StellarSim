from direct.showbase.ShowBase import ShowBase
import barneshut_cpp.cppsim as cs
from panda3d.core import GeomVertexData, GeomVertexFormat, Geom, GeomVertexWriter, GeomPoints, Geom, GeomNode
from panda3d.core import TextNode
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from math import pi, cos, sin
from direct.task import Task
import argparse
import numpy as np


class RenderApp(ShowBase):
    def __init__(self, data, timescale, scale, record):
        self.data = data
        self.scale = scale
        self.timescale = timescale
        ShowBase.__init__(self)
        vdata = GeomVertexData('galaxies', GeomVertexFormat.get_v3c4(), Geom.UHStatic)
        vdata.setNumRows(self.data.shape[1])
        self.vertex = GeomVertexWriter(vdata, 'vertex')
        color = GeomVertexWriter(vdata, 'color')
        for i in range(self.data.shape[1]):
            pos = self.data[0][i].pos / self.scale
            self.vertex.addData3(*pos)
            color.addData4(1,1,1,1)
        prim = GeomPoints(Geom.UHStatic)
        prim.add_consecutive_vertices(0, self.data.shape[1]-1)
        geom = Geom(vdata)
        geom.addPrimitive(prim)
        node = GeomNode('gnode')
        node.addGeom(geom)
        nodePath = self.render.attach_new_node(node)
        nodePath.setRenderModeThickness(2)
        self.disableMouse()
        self.useTrackball()
        self.trackball.node().set_pos(0,100,0)
        self.trackball.node().set_hpr(90,0,90)
        self.setBackgroundColor(0,0,0)
        self.taskMgr.add(self.update_task, "VertexUpdateTask")
        self.record(record)
    
    def load_data(self):
        self.data = cs.Result.load(self.file).numpy()
    
    def record(self, time):
        if time > 0:
            self.movie("screenshot", time, fps=60)

    def update_vertex(self, i):
        for j in range(self.data.shape[1]):
            pos = self.data[i][j].pos/self.scale
            self.vertex.setRow(j)
            self.vertex.setData3(*pos)

    def update_task(self, task):
        index = int((task.time * self.timescale)) % self.data.shape[0]
        self.update_vertex(index)
        return Task.cont

def visualize_result(result, timescale=100, scale=1e18, record=False):
    data = result.numpy()
    app = RenderApp(data, timescale, scale, record)
    app.run()

def visualize_bodylist(bl, scale=1e18, record=False):
    data = np.expand_dims(np.array([bl[i] for i in range(len(bl))]), axis=0)
    app = RenderApp(data, 0, scale, record)
    app.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualize simulation")
    parser.add_argument('file', help="binv file to play")
    parser.add_argument('-s', '--scale', help="Scale of the simulation", default=1e18, type=float)
    parser.add_argument('-t', '--timescale', help="Timescale of the simulation", default=100, type=float)
    parser.add_argument('-r', '--record', default=0, type=int)

    args = parser.parse_args()
    if args.file.endswith("binv"):
        data = cs.Result.load(args.file)
        visualize_result(data, args.timescale, args.scale, args.record)
    else:
        data = cs.BodyList3.load(args.file)
        visualize_bodylist(data, args.scale, args.record)