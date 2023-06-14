import os
import sys


import numpy as np
from tqdm import tqdm
from random import *


from generator import Generator
from gprMax.input_cmd_funcs import command

X = 0.4
Y = 0.2
Z = 0.001
# Adds an additional border to the edges (left + right)
XBorder = 0.0

# diameter: ~22.225 cm -> radius variance: 11 to 11.25
# generate 1 to 4 cylinders, randomly corroded
# for now it's 4.5 and 5.24 (ITU-R P.2040) for relative permittivity
# for now it's 1e-8 and 0.07 (ITU-R P.2040) for conductivity


def blockPrint():
    sys.stdout = open(os.devnull, 'w')


for i in tqdm(range(100)):
    rebar_count = randrange(1, 5)
    cylinder_size = round(uniform(0.011, 0.01125), 3)
    cylinder_gap = round(X - XBorder, 2) / (rebar_count + 1)

    blockPrint()

    message = command(
        'messages', 'n'
    )

    domain = command(
        'domain', X, Y, Z
    )

    dx_dy_dz = command(
        'dx_dy_dz', 0.001, 0.001, Z
    )

    time_window = command(
        'time_window', '2.4e-9'
    )

    concrete = command(
        'material', choice([4.5, 5.24]), choice(
            ['1e-8', 0.07]), 1, 0, 'concrete'
    )

    rebar = command(
        'material', 2, 0.056, 1, 0.01, 'rebar'
    )

    rebarcorrosion = command(
        'material', 40, '1.5e-6', 3.5, 0.3, 'rebarcorrosion'
    )

    waveform = command(
        'waveform', 'ricker', 1, '4.2e9', 'rickerwave'
    )

    hertzian_dipole = command(
        'hertzian_dipole', 'z', 0.01, round(Y - 0.05, 2), 0, 'rickerwave'
    )

    rx = command(
        'rx', 0.04, round(Y - 0.05, 2), 0
    )
 
    src_steps = command(
        'src_steps', 0.001, 0, 0
    )

    rx_steps = command(
        'rx_steps', 0.001, 0, 0
    )

    box = command(
        'box', 0, 0, 0, X, round(Y - 0.05, 2), Z, 'concrete'
    )

    geometricview = command(
        'geometry_view', 0, 0, 0, X, Y, Z, 0.001, 0.001, 0.001, 'RebarCorrosion_i' +
        str(i)+'_n'+str(rebar_count)+'_geo', 'n'
    )

    with open(os.path.join(
        'input-files',
        'RebarCorrosion_i{}_n{}_.in'.format(
              i,
              rebar_count)), 'w') as f:

        f.write('----- Dimensions\n\n')

        f.write(message+'\n')
        f.write(domain+'\n')
        f.write(dx_dy_dz+'\n')
        f.write(time_window+'\n\n')

        f.write('----- Materials\n\n')

        f.write(concrete+'\n')
        f.write(rebar+'\n')
        f.write(rebarcorrosion+'\n\n')

        f.write('----- GPR\n\n')

        f.write(waveform+'\n')
        f.write(hertzian_dipole+'\n')
        f.write(rx+'\n')
        f.write(src_steps+'\n')
        f.write(rx_steps+'\n\n')

        f.write('----- Objects\n\n')

        f.write(box+'\n\n')

        for i in range(rebar_count):
            f.write(str(i+1)+':\n')

            corrosionsize = 0.001

            if choice(['true', 'false']) == 'true':
                cylindercorrosion = command(
                    'cylinder', round(((i+1) * cylinder_gap + (XBorder / 2)), 2), round((Y - 0.05) / 2, 2), 0, round(
                    ((i+1) * cylinder_gap + (XBorder / 2)), 2), round((Y - 0.05) / 2, 2), Z, round(cylinder_size + corrosionsize, 3), 'rebarcorrosion', 'y'
                )

                f.write(cylindercorrosion+'\n')

                cylinder = command(
                    'cylinder', round(((i+1) * cylinder_gap + (XBorder / 2)), 2), round((Y - 0.05) / 2, 2), 0, round(
                    ((i+1) * cylinder_gap + (XBorder / 2)), 2), round((Y - 0.05) / 2, 2), Z, round(cylinder_size - corrosionsize, 3), 'rebar', 'y'
                )
            else:
                cylinder = command(
                    'cylinder', round(((i+1) * cylinder_gap + (XBorder / 2)), 2), round((Y - 0.05) / 2, 2), 0, round(
                    ((i+1) * cylinder_gap) + (XBorder / 2), 2), round((Y - 0.05) / 2, 2), Z, cylinder_size, 'rebar', 'y'
                )

            f.write(cylinder+'\n')

        f.write('\n'+'----- Misc'+'\n\n')

        f.write('--')
        f.write(geometricview+'\n')

        f.write('''
--python:
from gprMax.input_cmd_funcs import *
for i in range(1, 31):
    snapshot(0, 0, 0, '''+str(X)+''', '''+str(Y)+''', '''+str(Z)+''', 0.001, 0.001, 0.001, (i/10)*1e-9, 'snapshot' + str(i))
--end_python:''')


Generator(n_scans=360, in_dir='input-files/*.in', out_dir='output-files/')
