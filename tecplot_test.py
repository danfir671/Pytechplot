import tecplot as tp
from tecplot.constant import *
import pandas as pd
import sys
import os
import logging
import matplotlib.pyplot as plt

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

import sys
if '-c' in sys.argv:
    tp.session.connect()

tp.new_layout()

# trying to define the path
path = os.getcwd()
datafile = os.path.join(path, 'data_oneram6wing', 'OneraM6_SU2_RANS.plt')
dataset = tp.data.load_tecplot(datafile)

# Get the active frame and its plot
page = tp.active_page()
page.name = 'Slices'
frame = page.active_frame()
frame.plot_type = tp.constant.PlotType.Cartesian3D
plot = frame.plot()

Pressure_Coefficient = dataset.zone(1).values(11)[:]
x = dataset.zone(1).values(0)[:]
y = dataset.zone(1).values(1)[:]

Y = pd.Series(y)
Ymin = Y.min() + 0.01
Ymax = Y.max() - 0.03
yc = (Y - Y.min()) / (Y.max() - Y.min())

# Set contour variables & colormap
plot.contour(1).variable_index = 1
plot.contour(1).colormap_name = 'Small Rainbow'

# Show contour and slices
plot.show_contour = False
plot.show_slices = True

# Set slices properties
y_positions = [Ymin, Ymax / 4, Ymax / 2, 3 * Ymax / 4, Ymax]
slices_num = 0

for i, y1 in enumerate(y_positions):
    slice_ = plot.slice(i)
    slice_.show = True
    slice_.slice_source = tp.constant.SliceSource.SurfaceZones
    slice_.orientation = tp.constant.SliceSurface.YPlanes
    slice_.origin.y = y1
    slice_.edge.show = False
    slice_.mesh.show = True
    slice_.mesh.color = plot.contour(1)
    slice_.mesh.line_thickness = 0.8
    slices_num = slices_num + 1

# Extract slices
extracted_slices = plot.slices(0, 1, 2, 3, 4).extract(transient_mode=tp.constant.TransientOperationMode.AllSolutionTimes)

# Matplotlib plot
for i, extracted_slice in enumerate(extracted_slices):
    x_slice = extracted_slice.values('X')
    y_slice = extracted_slice.values('Y')
    field_data = extracted_slice.values('Pressure Coefficient')

    plt.figure()
    plt.contourf(x_slice, y_slice, field_data, cmap='viridis')
    plt.colorbar(label='Pressure Coefficient')
    plt.title(f'Tecplot Slice {i+1} Plot')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.show()


