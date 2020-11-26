from direct.showbase.ShowBase import ShowBase
import barneshut_cpp.cppsim as cs
from panda3d.core import GeomVertexData, GeomVertexFormat, Geom, GeomVertexWriter, GeomPoints, Geom, GeomNode
from math import pi, cos, sin
from direct.task import Task

scale = 1e18
timescale = 100

class RenderApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.load_data()
        vdata = GeomVertexData('galaxies', GeomVertexFormat.get_v3c4(), Geom.UHStatic)
        vdata.setNumRows(self.data.shape[1])
        self.vertex = GeomVertexWriter(vdata, 'vertex')
        color = GeomVertexWriter(vdata, 'color')
        for i in range(self.data.shape[1]):
            pos = self.data[0][i].pos / scale
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
    
    def load_data(self):
        self.data = cs.Result.load("Scenarios/stable.binv").numpy()

    def update_vertex(self, i):
        print(i)
        for j in range(self.data.shape[1]):
            pos = self.data[i][j].pos/scale
            self.vertex.setRow(j)
            self.vertex.setData3(*pos)

    def update_task(self, task):
        index = int((task.time * timescale)) % self.data.shape[0]
        self.update_vertex(index)
        return Task.cont


app = RenderApp()
app.run()