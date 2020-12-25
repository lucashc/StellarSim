import barneshut_cpp.cppsim as cs
from helper_files.sim_utils import get_positions
import argparse
import numpy as np
from vispy import app, gloo, scene
from vispy.visuals import Visual
from vispy.plot import Fig
from vispy.scene.cameras import ArcballCamera, FlyCamera
from vispy import io
import imageio
from tqdm import tqdm


vertex_shader = """
void main() {
    gl_Position = $transform(vec4($position, 1));
    gl_PointSize = 4;
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
        self._vertices = gloo.VertexBuffer()
        self.set_vertex_data(0)
        self._draw_mode = 'points'
        self.texture = gloo.Texture2D(load_star_image(), interpolation='linear')
        self.shared_program['u_texture'] = self.texture
        self.set_gl_state(clear_color=(0.0, 0.0, 0.03, 1.0), 
                            depth_test=False, blend=True,
                            blend_func=('src_alpha', 'one'))

    def _load_data(self, filename):
        preloaded = cs.Result.load(filename).numpy()
        self.positions = get_positions(preloaded).astype(np.float32)
        del preloaded
        self.frames = self.positions.shape[0]
        self.n_objs = self.positions.shape[1]

    def set_vertex_data(self, i):
        self._vertices.set_data(self.positions[i])
        self.update()

    def _prepare_transforms(self, view):
        view.view_program.vert['transform'] = view.get_transform()

    def _prepare_draw(self, view):
        self.shared_program.vert['position'] = self._vertices

Galaxy = scene.visuals.create_visual_node(GalaxyVisual)


canvas = scene.SceneCanvas(size=(800, 800), keys='interactive', show=True)
view = canvas.central_widget.add_view()
view.camera = ArcballCamera(fov=45, distance=1e19)

# Argument parsing
parser = argparse.ArgumentParser(description="Visualize simulation")
parser.add_argument('file', help="binv file to play")
parser.add_argument('-r', '--record', default='-', type=str)
args = parser.parse_args()

# Create Globals
vis = Galaxy(args.file, parent=view.scene)
timescale = 1
record = False
can_record = args.record != '-'
filename = args.record
frames = []


# Handle update
def update_vertices(ev, *args):
    global vis, timescale, canvas, frames
    index = int(ev.count / timescale) % vis.frames
    vis.set_vertex_data(index)
    if record:
        im = canvas.render()
        frames.append(im)

timer = app.Timer()
timer.connect(update_vertices)
timer.start(0)

def write_recording():
    global frames, filename
    writer = imageio.get_writer(filename)
    for i in tqdm(frames):
        writer.append_data(i)
    writer.close()
    print("Saved to file", filename)


# Handle speedup
@canvas.events.key_press.connect
def handle_key(ev):
    global timescale, record, can_record, frames, filename, canvas
    if ev.text == ']':
        # Increase speed
        timescale /= 2
    elif ev.text == '[':
        # Decrease speed
        timescale *= 2
    elif ev.text == 'r':
        # Start record
        if can_record:
            record = True
            print("Started recording")
        else:
            print("Record is disabled")
    elif ev.text == 's':
        if can_record and record:
            record = False
            can_record = False
            app.quit()
            canvas.close()
            print("Saving...")
            write_recording()
    elif ev.text == 'q':
        if record:
            print("Cannot quit, still recording")
        else:
            app.quit()
            canvas.close()

app.run()