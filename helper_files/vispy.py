import barneshut_cpp.cppsim as cs
from helper_files.sim_utils import get_positions
import argparse
import numpy as np
from vispy import app, gloo, scene
from vispy.visuals import Visual
from vispy.plot import Fig
from vispy.scene.cameras import ArcballCamera, FlyCamera
from vispy import io
from time import time

vertex_shader = """
void main() {
    gl_Position = $transform(vec4($position, 1));
    gl_PointSize = 5;
}
"""

fragment_shader = """
uniform sampler2D u_texture;
void main() {
    float star_tex_intensity = texture2D(u_texture, gl_PointCoord).r;
    gl_FragColor = vec4(star_tex_intensity * vec3(1,1,1), 0.8);
}
"""

def load_star_image():
    #fname = io.load_data_file('galaxy/star-particle.png')
    raw_image = io.read_png('helper_files/star-particle.png')
    return raw_image

class GalaxyVisual(Visual):
    def __init__(self, filename):
        Visual.__init__(self, vertex_shader, fragment_shader)
        self._load_data(filename)
        self.data = np.empty((self.n_objs, 3), dtype=np.float32)
        self._create_vertex_data(0)
        self._vertices = gloo.VertexBuffer(self.data)
        self._draw_mode = 'points'
        self.texture = gloo.Texture2D(load_star_image(), interpolation='linear')
        self.shared_program['u_texture'] = self.texture
        self.time = time()

    def _load_data(self, filename):
        preloaded = cs.Result.load(filename).numpy()
        self.positions = get_positions(preloaded).astype(np.float32)
        del preloaded
        self.frames = self.positions.shape[1]
        self.n_objs = self.positions.shape[0]
    def _create_vertex_data(self, i):
        self.data = self.positions[i]

    def _prepare_transforms(self, view):
        view.view_program.vert['transform'] = view.get_transform()
    def _prepare_draw(self, view):
        self._create_vertex_data(0)
        self.shared_program.vert['position'] = self._vertices
    

Galaxy = scene.visuals.create_visual_node(GalaxyVisual)


canvas = scene.SceneCanvas(size=(800, 800), keys='interactive', show=True)
view = canvas.central_widget.add_view()
view.camera = ArcballCamera(fov=45, distance=1e19)

vis = Galaxy('PI_test.binv', parent=view.scene)



app.run()