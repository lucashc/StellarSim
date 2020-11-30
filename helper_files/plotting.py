import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
import helper_files.sim_utils as utils


def data_gen(ax, dataset, index, particle_indices, frame_config, plotting_config):
    frame_data = np.empty(0)
    if frame_config["mode"] == 'line':
        frame_data = dataset[:index]
        plotting_config = {}
    elif frame_config["mode"] == 'point':
        frame_data = dataset[index:index+1]
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
        if frame_config["particle_config"] is None:
            indiv_plotting_config = plotting_config
        else:
            indiv_plotting_config = {**plotting_config, **frame_config["particle_config"][p_index]}

        plotlist.append(ax.plot3D(frame_data[:, p_index, 0], frame_data[:, p_index, 1], frame_data[:, p_index, 2],
                                  **indiv_plotting_config))


    ax.set(**{lim: bounds for lim, bounds in frame_config.items() if lim in ["xlim", "ylim", "zlim"]})
    ax.view_init(elev=frame_config["elevation"],
                 azim=index*frame_config["rotation_speed"]/3600/frame_config["skip_steps"] + frame_config["init_azimuth"])
    return plotlist


def movie3d(dataset, particle_indices, **CONFIG):
    """Makes a 3D plot movie of particles over time.
     -Dataset is a numpy array containing an array of 3D coordinates for each time step
     -particle_indices is a list of the indices of the particles you want to plot
     -CONFIG allows you to pass a bunch of plotting parameters. The parameters present in VIDEO_CONFIG and FRAME_CONFIG
        (see source code) can be used to customize your plot. All other keywords are passed on to the matplotlib
        ax.plot3D function, so matplotlib plotting settings such as color, linestyle or marker style can be set this
         way

        The parameter particle_config can be used to stylize each individual particle. This config will override any
        settings set by the "mode" parameter or by other parameters set in CONFIG. Usage: list of dicts.

         Explanation of some CONFIG parameters:
          - mode (str): sets some default parameters for the matplotlib ax.plot3D call. Current options are "line" and "point"
          - preview (bool): show a preview still before rendering. By default renders 1st frame, change with ⏎
          - preview_frame (int): choose which frame to preview
          - skip_steps (int): how many time steps to skip between each frame. By default no steps are skipped,
            but if your time step is small, consider increasing this value for faster rendering
          - rotation speed (float): how many arcseconds the scene will rotate per frame (default 30)
          - init_azimuth (float): viewing angle around z-axis in the first frame
          - elevation (float): viewing angle relative to x-y plane in degrees
          - axes (bool): true by default
          - grid (bool): false by default

      General tips: if rendering takes too long, increase skip_steps. If video plays too fast, decrease fps.
     """


    VIDEO_CONFIG = {
        "filename": 'test.mp4',
        "preview": True,
        "preview_frame": 0,
        "until_timestep": len(dataset)-1,
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
        "grid": False,
        "particle_config": None
    }
    dataset = utils.get_positions(dataset)
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

    frame_config["skip_steps"] = video_config["skip_steps"]  # pass along to data gen to normalize rotation speed
    if video_config['preview']:
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1, projection='3d')
        data_gen(ax, dataset, video_config["preview_frame"], particle_indices, frame_config, plotting_config)
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
