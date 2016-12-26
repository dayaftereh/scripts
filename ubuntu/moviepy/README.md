# MoviePy

**MoviePy** is build on top of [FFmpeg](https://www.ffmpeg.org) to manipulate move files match more effective.
The scripts can cut, change the speed or frame rate of movies.
**MoviePy** calls **FFmpeg** for the manipulation.

## Requirements

* Tested on Ubuntu 16.04
* [FFmpeg](https://www.ffmpeg.org) needs to be installed

## Usage

The following show the usage of all available functions from **MoviePy**.

```
#> ./mv.py
usage: mv.py [-h] -i INPUT (--cut | --speed | --fps) [--end END]
                [--start START] [--rate RATE] [--factor FACTOR]
   
   optional arguments:
     -h, --help            show this help message and exit
     -i INPUT, --input INPUT
                           the path to the input file
     --cut                 operation for cutting a move
     --speed               operation for speed up or slow down a move
     --fps                 operation for changing the frames per second of a move
   
   cutting:
     --end END             the end time of the part (format: hh:mm:ss.sss)
     --start START         the start time of the part (format: hh:mm:ss.sss)
   
   frame per seconds:
     --rate RATE           the fps rate of the output file
   
   speed up / slow down:
     --factor FACTOR       the speed factor of the output file
```

### Cutting

**MoviePy** allows to cut a move file in parts.
The following shows the usage for cutting:
```
#> ./mv.py --cut -i /path/to/file --start 00:00:30 --end 00:01:25
```

### Frames per Seconds

With **MoviePy** it is possible to change the fps rate of the input file.
The following command shows how to change the fps rate.
```
#> ./mv.py --fps -i /path/to/file --rate 24
```

### Change Speed

The last function of **MoviePy** is to change the speed of the input file.
The next command shows the usage of the function.
```
#> ./mv.py --speed -i /path/to/file --factor 2.25
```