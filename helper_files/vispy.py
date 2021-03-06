import barneshut_cpp.cppsim as cs
from helper_files.sim_utils import get_positions
from helper_files.mass_to_color import bodies_to_color
import argparse
import numpy as np
from vispy import app, gloo, scene
from vispy.visuals import Visual
from vispy.plot import Fig
from vispy.scene.cameras import ArcballCamera, FlyCamera
from vispy import io
import imageio
from tqdm import tqdm

app.use_app('PyQt5')

"""
This module visualizes a BINV-file using VisPy and OpenGL. 
It supports recording, speed adjustment, camera adjustment and standard sizes.
Use the `-r <filename>` option to record to a file. This file can have any format.
Keybinding:
* `]` Double speed of replay
* `[` Half speed of replay
* `r` Start recording, only if `-r` passed
* `s` Stop recording, quits the visualization
* `m` Make shot (one full play)
* `Esc` Quit the visualization
* `f` Set full HD size, 1920x1080
* `h` Set HD size, 1280x720  
* F11 Set fullscreen
* `=` Increase pointsize by 1
* `-` Decrease pointsize by 1
* `spacebar` Pause and continue
* `z` zoom in
* `x` zoom out
"""



vertex_shader = """
varying vec3 v_color;
void main() {
    gl_Position = $transform(vec4($position, 1));
    gl_PointSize = $pointsize;
    v_color = $color;
}
"""

fragment_shader = """
uniform sampler2D u_texture;
varying vec3 v_color;
void main() {
    float star_tex_intensity = texture2D(u_texture, gl_PointCoord).r;
    gl_FragColor = vec4(star_tex_intensity * v_color, 0.8);
}
"""


def load_star_image():
    #fname = io.load_data_file('galaxy/star-particle.png')
    raw_image = io.read_png('helper_files/star-particle.png')
    return raw_image


def load_data(filename, mass_scale, show_dm, no_show_m, darkmatter_intensity):
    print("Start loading data...")
    preloaded = cs.Result.load(filename).numpy()
    print("Selecting data...")
    func = np.vectorize(lambda b: (show_dm and b.dark_matter) or (not no_show_m and not b.dark_matter))
    preloaded = preloaded[:,func(preloaded[0])]
    print(preloaded.shape)
    print("Extracting positions and adding color...")
    positions = get_positions(preloaded).astype(np.float32)
    c = bodies_to_color(preloaded[0], mass_scale)
    if show_dm:
        dm_index = [i for i, b in enumerate(preloaded[0]) if b.dark_matter]
        c[dm_index] = [0, darkmatter_intensity, 0]
    colors = gloo.VertexBuffer(c)
    print("Data loaded and ready for GPU")
    return positions, colors

class GalaxyVisual(Visual):
    def __init__(self, positions, colors):
        Visual.__init__(self, vertex_shader, fragment_shader)
        self.positions = positions
        self.colors = colors
        self.frames = self.positions.shape[0]
        self._vertices = gloo.VertexBuffer()
        self.set_vertex_data(0)
        self._draw_mode = 'points'
        self.texture = gloo.Texture2D(load_star_image(), interpolation='linear')
        self.shared_program['u_texture'] = self.texture
        self.shared_program.vert['color'] = self.colors
        self.pointsize = 5
        self.set_gl_state(clear_color=(0.0, 0.0, 0.03, 1.0), 
                            depth_test=False, blend=True,
                            blend_func=('src_alpha', 'one'))
    def set_vertex_data(self, i):
        self._vertices.set_data(self.positions[i])
        self.update()

    def _prepare_transforms(self, view):
        view.view_program.vert['transform'] = view.get_transform()

    def _prepare_draw(self, view):
        self.shared_program.vert['position'] = self._vertices
        self.shared_program.vert['pointsize'] = self.pointsize



# Argument parsing
parser = argparse.ArgumentParser(description="Visualize simulation")
parser.add_argument('file', help="binv file to play")
parser.add_argument('-r', '--record', default='-', type=str, help="Record to file")
parser.add_argument('-m', '--massscale', default=1, type=float, help="Mass scale")
parser.add_argument('-d', '--darkmatter', action='store_true', help="Whether to show darkmatter")
parser.add_argument('-i', '--darkmatter_intensity', default=0.5, type=float, help="Darkmatter intensity 0.0 to 1.0")
parser.add_argument('-o', '--no_ordinary_matter', action='store_true', help='Whether to remove ordinary matter')
args = parser.parse_args()


# Data loading
pos, col = load_data(args.file, args.massscale, args.darkmatter, args.no_ordinary_matter, args.darkmatter_intensity)

print("Starting GUI")
Galaxy = scene.visuals.create_visual_node(GalaxyVisual)
canvas = scene.SceneCanvas(size=(800, 800), keys='interactive', show=True)
view = canvas.central_widget.add_view()
view.camera = ArcballCamera(fov=45, distance=5e20)

# Create Globals
print("Start the galaxy visual")
vis = Galaxy(pos, col, parent=view.scene)
print("Created visual")
timescale = 1
record = False
can_record = args.record != '-'
filename = args.record
frames = []
fps = 1
paused = False
lag = 0
start_shot= False
started_shot = False
finished_shot = False

# fps setter
def set_fps(result):
    global fps
    fps = result


# Handle update
def update_vertices(ev, *args):
    global vis, timescale, canvas, frames, lag, paused, record, start_shot, started_shot, finished_shot
    if not paused:
        index = int((ev.count-lag) / timescale) % vis.frames
        vis.set_vertex_data(index)
        if start_shot and index == 0:
            if started_shot:
                finished_shot = True
            print("Start round")
            record = True
            started_shot = True

    else:
        lag += 1
    if record:
        im = canvas.render()
        frames.append(im)
        if finished_shot:
            print("Start saving")
            record = False
            can_record = False
            app.quit()
            canvas.close()
            print("Saving...")
            write_recording()

timer = app.Timer()
timer.connect(update_vertices)
timer.start(0)

def write_recording():
    global frames, filename, fps
    writer = imageio.get_writer(filename, fps=fps, codec='libx264', quality=10, pixelformat='yuv420p')
    for i in tqdm(frames):
        writer.append_data(i)
    writer.close()
    print("Saved to file", filename)


# Handle speedupapp.use_app('Pyglet')
@canvas.events.key_press.connect
def handle_key(ev):
    global timescale, record, can_record, frames, filename, canvas, paused, start_shot, view
    if ev.text == ']':
        # Increase speed
        timescale /= 2
        print("Timescale is now", timescale)
    elif ev.text == '[':
        # Decrease speed
        timescale *= 2
        print("Timescale is now", timescale)
    elif ev.text == 'r':
        # Start record
        if record:
            print("Already recording")
        elif can_record:
            record = True
            print("Started recording")
            # Measure fps
            canvas.measure_fps(callback=set_fps)
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
    elif ev.text == 'f':
        canvas.size = (1920, 1080)
    elif ev.text == 'h':
        canvas.size = (1280, 720)
    elif ev.text == '=':
        vis.pointsize += 1
        print(f"Pointsize is {vis.pointsize}")
    elif ev.text == '-':
        vis.pointsize -= 1
        print(f"Pointsize is {vis.pointsize}")
    elif ev.text == ' ':
        if paused:
            print("Unpaused")
        else:
            print("Paused")
        paused = not paused
    elif ev.text == 'm':
        start_shot = True
    elif ev.text == 'z':
        view.camera.distance *= 0.9
    elif ev.text == 'x':
        view.camera.distance *= 1.1
app.run()