# DVS Toolkit

The simple toolkit for processing event-based data. Any suggestions and questions, please contact me with [KugaMaxx@outlook.com](mailto:KugaMaxx@outlook.com) or comment in the [issue](https://github.com/KugaMaxx/taro-dvstoolkit/issues).

<div align=center><img src="https://github.com/KugaMaxx/taro-dvstoolkit/blob/main/assets/images/demonstrate.gif" alt="demonstrate" width="100%"></div>

## Preliminaries

### Installation

We recommend to create a new [conda](https://docs.conda.io/en/main/miniconda.html) environment and install our package as follows:
```unix
python setup.py install
```

### Running

You can run `test/demo.py` to verify its validity
```unix
python test/demo.py
```

## Getting started

This package aims to provide a series of wrapped modules to help users to do subsequent processing and analysis on event camera data. We follows standards in [dv](https://inivation.gitlab.io/dv/dv-docs/docs/getting-started/) and [dv-python](https://gitlab.com/inivation/dv/dv-python) documentation. **Now the supported data types are**:
 
- [x] Size
- [x] Event
- [x] Frame
- [ ] IMU

---

### I/O Operations

**DvsFile** can be used to read and write event data files. 

+ `load(path: str)` reads file containing streams of data that are defined like [dv](https://inivation.gitlab.io/dv/dv-docs/docs/getting-started/) style. It supports load all the information including `.aedat4` and `.txt` file.

    ```python
    from evtool.dvs import DvsFile

    # load event data
    data = DvsFile.load(<path/to/load>)

    # access dimensions of the event stream
    height, width = data['size']

    # loop through the "events"
    for event in data['events']:
        print(event.timestamp, event.x, event.y, event.polarity)

    # loop through the "frames" (.txt not supported)
    for frame in data['frames']:
        print(frame.timestamp, frame.image.shape)
    ```

+ `save(data: Data, path: str)` writes data to `.txt` file, whose type is determined by suffix.
    ```python
    from evtool.dvs import DvsFile

    # load event data
    data = DvsFile.load(<path/to/load>)

    # save event data
    DvsFile.save(data, <path/to/save>)
    ```

---

### Standard Type

**Event** stores basic information of event data, including `timestamp`, `x`, `y` and `polarity`.

+ `slice(t: interval{'unit'})` divides events into subsets by time interval.
    ```python
    # loop through sliced event packet by time interval ('s', 'ms', 'us')
    for timestamp, event in data['events'].slice('25ms'):
        print(timestamp, event.shape)
    ```

+ `project(size: Size)` accumulates events into a 2D plane
    ```python
    import matplotlib.pyplot as plt

    # get projected events frame
    counts = data['events'].project(data['size'])

    # display projected frame
    plt.imshow(counts, vmin=-1, vmax=1, cmap=plt.set_cmap('bwr'))
    plt.show()
    ```

+ `hotpixel(size: Size, thres: int)` returns potential hot-pixel index. It will project events first and return a set of index whose pixels' median numbers are larger than defined `thres`.
    ```python
    # return hot-pixel index
    idx = data['events'].hotpixel(data['size'], thres=1000)

    # filter all hot-pixels
    data['events'] = data['events'][idx]
    ```

+ `shot_noise(size: Size, rate: int, down_sample: int)` generates shot noise events. It simulates the process of generating shot noise with Poisson distribution at fixed `rate` and downsamples raw events at `down_sample`.
    ```python
    # generate shot noise
    data['events'] = data['events'].shot_noise(data['size'], rate=5, down_sample=0.8)
    ```

**Frame** stores Active Pixel Sensor (APS) outputs, including `timestamp` and `image`.

+ `find_closest(t: int)` finds the frame which is closet to timestamp `t`, returns the frame's timestamp and corresponding image.
    ```python
    from numpy.random import randint
    import matplotlib.pyplot as plt

    # find closet frame
    idx = data['frames'].find_closest(randint(0, 1E16, 1))
    timestamp, image = data['frames'][idx]
    
    # display frame closest to referred timestamp
    plt.imshow(image)
    plt.show()
    ```

---

### Utilities

**Player** is a class to provide visualization. It has `matplotlib` and `plotly` implementation, the former is suggested to view a real-time animation while the latter is more suitable for static 2D and 3D rendering (which means may take a long time to generate animation).

+ `view(t: interval{'unit'}, core: {'matplotlib'(default), 'plotly'})` gives a glance at events stream.
  ```python
  from evtool.utils import Player

  # load file
  data = DvsFile.load(<path/to/load>)

  # load data into player and choose core
  player = Player(data, core='matplotlib')

  # view data
  player.view("25ms", use_aps=True)
  ```

---

## Acknowledgement

Special thanks to [Jinze Chen](mailto:chjz@mail.ustc.edu.cn).
