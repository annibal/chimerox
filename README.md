# Chimerox

Chimerism (illusion) + Paradox (chaotic).

**Chimerox** is a python script that generates abstract videos with randomness, but with tight file configurations.

## Installation

1. Have the `chimerox.py` file in your local machine;

2. Ensure `python` or `python3` is installed (use `which python3` for example);

3. Install required packages: `pip install opencv-python numpy`;

> Alternatively run `pip install -r requirements.txt` if the file is present

4. if you want, idk clone the file to `/usr/lib`, or make an alias to the python file in your `.bash_profile` like `alias chimerox="python3 /usr/home/repos/chimerox/chimerox.py", or something like that.

## Usage

Simplest form:

`python3 ./chimerox.py ~/movies/abstract_video_1.mp4`

This will generate a video in `~/movies` called `abstract_video_1.mp4`. It will be encoded with the MP4V codec, it will have 10 seconds of length, 24 fps, and a resolution of 640x480 pixels.

### Video File Settings

> Use `python3 chimerox.py "~/movies/video_$(date +%F | tr -d '-')_$(($(date +%s)-$(date -d0 +%s))).mp4` to append the date and the current elapsed seconds of the current day in the filename.
>
> `$(date +%F)` will provide the current day, in the format "2025-07-25".
>
> `$(date +%F | tr -d '-')` gives "20250725", year month and day as a single number.
>
> `$(($(date +%s)-$(date -d0 +%s)))` gives a number between 0 and 86400, representing the amount of seconds since the day started.
>
> Use `$(printf "%05d" $[$(date +%s)-$(date -d0 +%s)])` to keep the same amount of digits always

If you wish to, you can configure the video's parameters:

- `--dimensions 500x300`: sets the video width to 500px and the height to 300px. Provide the value as `"{width}letter{height}"` or use any of the presets instead. Defaults to **640x480**.
- `--length 10`: the duration of the video (`--duration` is an alias flag), in seconds. Use $((60 * MINUTES)) if you want a long abstract video. Default 10 seconds.
- `--fps 24`: How many Frames per Second the video will have, with 24 as the default.
- `--codec MJPG`: Chimerox infers the codec based on the extension of the provided filename - supports **mp4**, **avi**, **mov** and **wmv** - but you can override it as you wish. Should you not put any extension in the filename, Chimerox will infer it based on the codec. Default is `MP4V` (which would give you an **.mp4** file).
- `--meta "key:value"`: Add an additional metadata key and it's value in the file, like for example `--meta "title:My Abstract Video"`. You can use several `--meta` flags together.

### Resultion Presets

| Preset Name   | Width  | Height |
| ------------- | ------ | ------ |
| `--QVGA`      | 320    | 240    |
| `DEFAULT`     | 640    | 480    |
| `--QHD`       | 960    | 540    |
| `--XGA`       | 1024   | 768    |
| `--HD`        | 1366   | 768    |
| `--HDV`       | 1440   | 1080   |
| `--FHD`       | 1920   | 1080   |
| `--UXGA`      | 1600   | 1200   |
| `--WQHD`      | 2560   | 1440   |

Presets can be used as a flag `--WQHD` or as the resolution flag's value: `--resolution WQDG`. Make a video of any width and any height by using the `--dimensions` flag.

Also, use the `--portrait` flag with no value to swap WIDTH with HEIGHT.

> `python3 chimerox.py video.mp4 --FHD --portrait`
>
> The `video.mp4` file will be 1920 pixels tall.

### Video Content Settings

Customize the video with these flags:

- `--iota`: abstract structure seed
- `--omicron`: abstract quantities seed
- `--phase`: A number between -1 and 1
- `--threshold`: Amount of particles
- `--resonance`: Resonance
- `--entropy`: wave opacity, distortion strength, vortex chaos force etc.

I don't know what they do, and i specifically choose to have it be this way. I needed to create a test mass of videos, and i know that knowing how to tune the video's abstractionesses would make me spend time optimizing it, so i asked an AI to make so that the parameters exert control over everything in a chaotic way, and relate eachother to themselves, this way preventing a learning curve between numbers and the unique abstract result.

Only the `threshold` that i recommend to do not exceed 3000.

-----

Thanks Claude, Manus, and my past self