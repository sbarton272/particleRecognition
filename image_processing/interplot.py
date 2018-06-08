from ncempy.io import dm
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from matplotlib.widgets import Slider, Button, RadioButtons
import ipywidgets as widgets

def interplot(image):
    """Plots images represented as numpy arrays with a slider bar to contol the range if the image's histogram"""
    if type(image) != np.ndarray:
        raise RuntimeError('Input must be np.ndarray')
    slider_range = [image.min(),image.max()]
    def imm(image, irange):
        fig, ax = plt.subplots(figsize=(10,10))
        ax.imshow(image, cmap = 'gray', clim = irange)
        ax.axis('off')
    def slide(x):
        imm(image,x)
    x = widgets.IntRangeSlider(value = slider_range,min = slider_range[0],max = slider_range[1],continuous_update = False)
    widgets.interact(slide,x=x)


def open_dm3(dm3FileList, imageNum):
    image = dm.dmReader(dm3FileList[imageNum])
    print(dm3FileList[imageNum])
    return image['data']
