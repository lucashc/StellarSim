from direct.showbase.ShowBase import ShowBase
import barneshut_cpp.cppsim as cs
from panda3d.core import GeomVertexData, GeomVertexFormat, Geom, GeomVertexWriter, GeomPoints, Geom, GeomNode
from math import pi, cos, sin
from direct.task import Task

scale = 20

class RenderApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        bl = cs.BodyList3.load('galaxies.bin')
        vdata = GeomVertexData('galaxies', GeomVertexFormat.get_v3c4(), Geom.UHStatic)
        vdata.setNumRows(len(bl))
        self.vertex = GeomVertexWriter(vdata, 'vertex')
        color = GeomVertexWriter(vdata, 'color')
        self.load_data()
        for i in range(len(bl)):
            pos = self.data[0][i].pos / scale
            self.vertex.addData3(*pos)
            color.addData4(1,1,1,1)
        prim = GeomPoints(Geom.UHStatic)
        prim.add_consecutive_vertices(0, len(bl)-1)
        geom = Geom(vdata)
        geom.addPrimitive(prim)
        node = GeomNode('gnode')
        node.addGeom(geom)
        nodePath = self.render.attach_new_node(node)
        nodePath.setRenderModeThickness(2)
        self.camera.set_pos(0,0,100)
        self.camera.set_hpr(0,-90,0)
        self.disableMouse()
        self.setBackgroundColor(0,0,0)
        self.taskMgr.add(self.update_task, "VertexUpdateTask")
    
    def load_data(self):
        self.data = []
        for i in range(1501):
            self.data.append(cs.BodyList3.load(f"galaxies{i:3d}.bin"))

    def update_vertex(self, i):
        for j in range(len(self.data[0])):
            pos = self.data[i][j].pos/scale
            self.vertex.setRow(j)
            self.vertex.setData3(*pos)

    def update_task(self, task):
        index = int((task.time * 100)) % 1501
        self.update_vertex(index)
        return Task.cont
app = RenderApp()
app.run()