import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np


def data_gen(ax, dataset, index, particle_indices, frame_config, plotting_config):
    frame_data = np.empty(0)
    if frame_config["mode"] == 'line':
        frame_data = dataset[:index]
        plotting_config = {}
    elif frame_config["mode"] == 'point':
        frame_data = dataset[index]
        plotting_config = {'linestyle': 'none', 'marker': '.'}
    ax.clear()
    if frame_config["axes"]:
        ax.axis('on')
    else:
        ax.axis('off')

    if frame_config["grid"]:
        ax.grid('on')
    else:
        ax.grid('off')

    plotlist = []
    for p_index in particle_indices:
        plotlist.append(ax.plot3D(frame_data[p_index, 0], frame_data[p_index, 1], frame_data[p_index, 2], **plotting_config))
    ax.set(**{lim: bounds for lim, bounds in frame_config.items() if lim in ["xlim", "ylim", "zlim"]})
    ax.view_init(elev=frame_config["elevation"], azim=index*frame_config["rotation_speed"]/3600 + frame_config["init_azimuth"])
    return plotlist


def movie3d(dataset, particle_indices, **CONFIG):
    VIDEO_CONFIG = {
        "filename": 'test.mp4',
        "preview": True,
        "until_timestep": len(dataset) - 1,
        "skip_steps": 1,
        "fps": 30,
        "artist": "",
        "bitrate": 1800,
    }

    FRAME_CONFIG = {
        "mode": "line",
        "xlim": (-100, 100),
        "ylim": (-100, 100),
        "zlim": (-100, 100),
        "rotation_speed": 30,  # arcseconds per frame
        "init_azimuth": 270,
        "elevation": 10,
        "axes": True,
        "grid": False
    }

    plotting_config = {}
    frame_config = {}
    video_config = {}
    for key, value in CONFIG.items():
        if key in FRAME_CONFIG:
            frame_config[key] = value
        elif key in VIDEO_CONFIG:
            video_config[key] = value
        else:  # other kwargs are passed on to mpl ax.plot3D
            plotting_config[key] = value

    frame_config = {**FRAME_CONFIG, **frame_config}
    video_config = {**VIDEO_CONFIG, **video_config}

    if VIDEO_CONFIG['preview']:
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1, projection='3d')
        data_gen(ax, dataset, video_config["until_timestep"], particle_indices, frame_config, plotting_config)
        plt.show()

    fig = plt.figure()
    # ax = plt.axes(projection='3d')
    ax = fig.add_subplot(1, 1, 1, projection='3d')

    data_gen_formatted = lambda index: data_gen(ax, dataset, index, particle_indices, frame_config, plotting_config)

    grav_ani = animation.FuncAnimation(fig, data_gen_formatted,
                                       frames=np.arange(0, video_config["until_timestep"], video_config["skip_steps"]),
                                       interval=30, blit=False)

    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=video_config["fps"], metadata=dict(artist=video_config["artist"]), bitrate=video_config["bitrate"])
    filename = video_config["filename"]
    print("Started writing video to {}".format(filename))
    grav_ani.save(filename, writer=writer)
    print("Video saved at {}".format(filename))
