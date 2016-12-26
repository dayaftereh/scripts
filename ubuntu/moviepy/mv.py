#!/usr/bin/python

TEST_FILE = '/home/lasse/Videos/GOPR4308.MP4'
TEST_FILE_2 = '/home/lasse/Videos/GOPR4397.MP4'
TEST_FILE_3 = '/home/lasse/Videos/GOPR4409.MP4'

import argparse

import cut
import fps
import speed


def args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='the path to the input file', required=True)

    options = parser.add_mutually_exclusive_group(required=True)
    options.add_argument('--cut', help="operation for cutting a move", action="store_true")
    options.add_argument('--speed', help="operation for speed up or slow down a move", action="store_true")
    options.add_argument('--fps', help="operation for changing the frames per second of a move", action="store_true")

    cut_options = parser.add_argument_group('cutting')
    cut_options.add_argument('--end', help="the end time of the part (format: hh:mm:ss.sss)")
    cut_options.add_argument('--start', help="the start time of the part (format: hh:mm:ss.sss)")

    fps_options = parser.add_argument_group('frame per seconds')
    fps_options.add_argument('--rate', help="the fps rate of the output file", type=float)

    speed_options = parser.add_argument_group('speed up / slow down')
    speed_options.add_argument('--factor', help="the speed factor of the output file", type=float)

    return parser


def cutting(args):
    input = args.input
    start = args.start
    end = args.end
    cut.from_to(input, start, end)


def frame_per_seconds(args):
    rate = args.rate
    input = args.input
    fps.transcode(input, str(rate))


def speed_change(args):
    input = args.input
    factor = args.factor
    speed.change(input, float(factor))


def main():
    parser = args_parser()
    args = parser.parse_args()

    if args.cut:
        cutting(args)
    elif args.fps:
        frame_per_seconds(args)
    elif args.speed:
        speed_change(args)


if __name__ == '__main__':
    main()
