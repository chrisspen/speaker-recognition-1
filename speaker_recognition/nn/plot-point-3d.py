#!/usr/bin/python2

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import argparse, sys

stdin_fname = '$stdin$'


def get_args():
    description = "plot points into graph. x and y seperated with white space in one line, or just y's"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-i', '--input', help='input data file, "-" for stdin, default stdin', default='-')
    parser.add_argument('-o', '--output', help='output image', default='')
    parser.add_argument('--show', help='show the figure after rendered', action='store_true')
    parser.add_argument('-t', '--title', help='title of the graph', default='')
    parser.add_argument('--xlabel', help='x label', default='x')
    parser.add_argument('--ylabel', help='y label', default='y')
    parser.add_argument('--zlabel', help='z label', default='z')
    parser.add_argument('--xlim', help='xlim')
    parser.add_argument('--ylim', help='ylim')
    parser.add_argument('--zlim', help='zlim')

    parser.add_argument('--annotate-maximum', help='annonate maximum value in graph', action='store_true')
    parser.add_argument('--annotate-minimum', help='annonate minimum value in graph', action='store_true')
    parser.add_argument('--xkcd', help='xkcd style', action='store_true')

    args = parser.parse_args()

    if (not args.show) and len(args.output) == 0:
        raise Exception("at least one of --show and --output/-o must be specified")
    if args.xlim:
        args.xlim = map(float, args.xlim.rstrip().split(','))
    if args.ylim:
        args.ylim = map(float, args.ylim.rstrip().split(','))
    if args.zlim:
        args.zlim = map(float, args.zlim.rstrip().split(','))

    return args


def filter_valid_range(points, rect):
    """rect = (min_x, max_x, min_y, max_y)"""
    ret = []
    for x, y in points:
        if x >= rect[0] and x <= rect[1] and y >= rect[2] and y <= rect[3]:
            ret.append((x, y))
    if len(ret) == 0:
        ret.append(points[0])
    return ret


def do_plot(data_x, data_y, data_z, args):
    fig = plt.figure(figsize=(16.18, 10))
    projection = '2d'
    if len(data_z) > 0:
        projection = '3d'
    ax = fig.add_axes((0.1, 0.2, 0.8, 0.7), projection=projection)
    if projection == '2d':
        ax.scatter(data_x, data_y)
    else:
        ax.scatter(data_x, data_y, data_z)
    if args.xlim:
        ax.set_xlim(args.xlim)
    if args.ylim:
        ax.set_ylim(args.ylim)
    if args.zlim:
        ax.set_zlim3d(args.zlim)
    if args.xlim or args.ylim or args.zlim:
        pass
        ax.set_aspect('equal')
    else:
        ax.set_aspect('equal', 'datalim')
    #ax.spines['right'].set_color('none')
    #ax.spines['left'].set_color('none')
    #plt.xticks([])
    #plt.yticks([])

    if args.annotate_maximum or args.annotate_minimum:
        max_x, min_x = max(data_x), min(data_x)
        max_y, min_y = max(data_y), min(data_y)
        x_range = max_x - min_x
        y_range = max_y - min_y
        x_max, y_max = data_y[0], data_y[0]
        x_min, y_min = data_x[0], data_y[0]

        rect = ax.axis()

        for i in xrange(1, len(data_x)):
            if data_y[i] > y_max:
                y_max = data_y[i]
                x_max = data_x[i]
            if data_y[i] < y_min:
                y_min = data_y[i]
                x_min = data_x[i]
        if args.annotate_maximum:
            text_x, text_y = filter_valid_range([(x_max + 0.05 * x_range, y_max + 0.025 * y_range), (x_max - 0.05 * x_range, y_max + 0.025 * y_range),
                                                 (x_max + 0.05 * x_range, y_max - 0.025 * y_range), (x_max - 0.05 * x_range, y_max - 0.025 * y_range)], rect)[0]
            ax.annotate('maximum ({:.3f},{:.3f})'.format(x_max, y_max), xy=(x_max, y_max), xytext=(text_x, text_y), arrowprops=dict(arrowstyle='->'))
        if args.annotate_minimum:
            text_x, text_y = filter_valid_range([(x_min + 0.05 * x_range, y_min - 0.025 * y_range), (x_min - 0.05 * x_range, y_min - 0.025 * y_range),
                                                 (x_min + 0.05 * x_range, y_min + 0.025 * y_range), (x_min - 0.05 * x_range, y_min + 0.025 * y_range)], rect)[0]
            ax.annotate('minimum ({:.3f},{:.3f})'.format(x_min, y_min), xy=(x_min, y_min), xytext=(text_x, text_y), arrowprops=dict(arrowstyle='->'))

    ax.set_xlabel(args.xlabel)
    ax.set_ylabel(args.ylabel)
    if projection == '3d':
        ax.set_zlabel(args.zlabel)

    fig.text(0.5, 0.05, args.title, ha='center')
    if args.output != '':
        plt.savefig(args.output)

    if args.show:
        plt.show()


def main():
    args = get_args()
    if args.input == stdin_fname:
        fin = sys.stdin
    else:
        fin = open(args.input)

    data_x = []
    data_y = []
    data_z = []
    data_format = -1
    for lineno, line in enumerate(fin.readlines()):
        line = [float(i) for i in line.rstrip().split()]
        line_data_format = -1
        x, y, z = None, None, None
        if len(line) == 0:
            continue
        if len(line) == 2:
            line_data_format = 0
            x, y = line
        elif len(line) == 1:
            line_data_format = 1
            x, y = lineno, line[0]
        elif len(line) == 3:
            x, y, z = line
            line_data_format = 2
        else:
            raise RuntimeError('Can not parse input data at line {}'.format(lineno + 1))

        if data_format == -1:
            data_format = line_data_format
        else:
            if line_data_format != data_format:
                raise RuntimeError('data format is not consistent, at line {}' \
                        . format(lineno + 1))
        data_x.append(x)
        data_y.append(y)
        if z != None:
            data_z.append(z)
    print('len=', len(data_x))
    if args.input != stdin_fname:
        fin.close()

    if len(data_x) == 1:
        return

    if args.xkcd:
        with plt.xkcd():
            do_plot(data_x, data_y, data_z, args)
    else:
        do_plot(data_x, data_y, data_z, args)


if __name__ == '__main__':
    main()
