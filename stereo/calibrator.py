import Tkinter as tk
import tkMessageBox as tmb
from tkFileDialog import askopenfilename

import cv2
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class _ToolboxEntry(tk.Frame):

    def __init__(self, master, label_text, minval, maxval):
        tk.Frame.__init__(self, master)
        self.title = label_text
        self.label = tk.Label(self, text=label_text + ": ")
        self.slider = tk.Scale(self, from_=minval, to=maxval, command=self.scale_cb, orient=tk.HORIZONTAL, length=300)
        self.entry = tk.Entry(self)

        self.label.grid(row=0, column=0)
        self.slider.grid(row=0, column=1)
        self.entry.grid(row=0, column=5)

    def scale_cb(self, newval):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, str(newval))

    @property
    def value(self):
        try:
            return float(self.entry.get())
        except ValueError:
            tmb.showerror("Invalid value for {}".format(self.title),
                          "The value for {} must be a number.".format(self.title))
            return float('nan')


class Calibrator(object):

    def __init__(self):
        self.root = tk.Tk()
        self.toolbar = tk.Frame(self.root)
        # Populate toolbar
        self.prefilter_level_adjuster = _ToolboxEntry(self.toolbar, "prefilter_size", 5, 255)
        self.prefilter_cap_adjuster = _ToolboxEntry(self.toolbar, "prefilter_cap", 1, 63)
        self.min_disparity_adjuster = _ToolboxEntry(self.toolbar, "min_disparity", -128, 128)
        self.disp_range_adjuster = _ToolboxEntry(self.toolbar, "disparity_range", 32, 128)
        self.uniqueness_ratio_adjuster = _ToolboxEntry(self.toolbar, "uniqueness_ratio", 0, 100)
        self.texture_thresh_adjuster = _ToolboxEntry(self.toolbar, "texture_threshold", 0, 100)
        self.speckle_size_adjuster = _ToolboxEntry(self.toolbar, "speckle_size", 0, 1000)
        self.speckle_range_adjuster = _ToolboxEntry(self.toolbar, "speckle_range", 0, 31)

        # Now add the plot frame(s)
        self.plotter_frame = tk.Frame(self.root)
        self.left_image_fig = plt.figure(figsize=(5.0, 5.0))
        self.left_image_canvas = FigureCanvasTkAgg(self.left_image_fig, self.root)
        self.left_image_widget = self.left_image_canvas.get_tk_widget()

        self.right_image_fig = plt.figure(figsize=(5.0, 5.0))
        self.right_image_canvas = FigureCanvasTkAgg(self.right_image_fig, self.root)
        self.right_image_widget = self.right_image_canvas.get_tk_widget()

        self.disparity_fig = plt.figure(figsize=(10.0, 10.0))
        self.disparity_canvas = FigureCanvasTkAgg(self.disparity_fig, self.root)
        self.disparity_widget = self.disparity_canvas.get_tk_widget()

        self.imload_button = tk.Button(text="load images", command=self.load_images)

        self.toolbar.grid(row=0, column=0, columnspan=6)
        self.prefilter_level_adjuster.grid(row=0)
        self.prefilter_cap_adjuster.grid(row=1)
        self.min_disparity_adjuster.grid(row=2)
        self.disp_range_adjuster.grid(row=3)
        self.uniqueness_ratio_adjuster.grid(row=4)
        self.texture_thresh_adjuster.grid(row=5)
        self.speckle_size_adjuster.grid(row=6)
        self.speckle_range_adjuster.grid(row=7)

        self.root.mainloop()

        # Internal accounting
        self.left_image = None
        self.right_image = None

    def load_images(self):
        # First, load the left side image
        left_image_name = askopenfilename(parent=self.root, message="Select the left-side image")
        self.left_image = cv2.imread(left_image_name)

        right_image_name = askopenfilename(parent=self.root, message="Select the right-side image")
        self.right_image = cv2.imread(right_image_name)

