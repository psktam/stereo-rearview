import numpy as np
import matplotlib.pyplot as plt
import cv2


# noinspection PyArgumentList
class StereoViewerMain(object):

    def __init__(self, cam_index_left, cam_index_right, num_disparities=16, blocksize=15):
        self.cam_left_ind = cam_index_left
        self.cam_right_ind = cam_index_right

        self.left_cam = None
        self.right_cam = None

        self.disparity_generator = cv2.StereoBM_create(numDisparities=num_disparities,
                                                       blockSize=blocksize)

    def open_eyes(self):
        if self.left_cam is None or not self.left_cam.isOpened():
            self.left_cam = cv2.VideoCapture(self.cam_left_ind)
        if self.right_cam is None or not self.right_cam.isOpened():
            self.right_cam = cv2.VideoCapture(self.cam_right_ind)

    def shut_eyes(self):
        if self.left_cam is not None and self.left_cam.isOpened():
            self.left_cam.release()
        if self.right_cam is not None and self.right_cam.isOpened():
            self.right_cam.release()

    def acquire_scene(self):
        ret_left, img_left = self.left_cam.read()
        ret_right, img_right = self.right_cam.read()

        img_left = cv2.cvtColor(img_left, cv2.COLOR_BGR2GRAY)
        img_right = cv2.cvtColor(img_right, cv2.COLOR_BGR2GRAY)

        return ret_left and ret_right, img_left, img_right

    def construct_depth_map(self, img_left, img_right):
        """
        This method constructs the depth map from two images.

        :param img_left:
        :param img_right:
        :return:
        """
        disparities = self.disparity_generator.compute(img_left, img_right)
        return disparities

    def make_triptych(self, generate_plots=True):
        _, left, right = self.acquire_scene()
        disp = self.construct_depth_map(left, right)

        if generate_plots:
            fig = plt.figure()
            axe1 = fig.add_subplot(131)
            axe2 = fig.add_subplot(132)
            axe3 = fig.add_subplot(133)

            axe1.imshow(left)
            axe2.imshow(right)
            dmap = axe3.imshow(disp)
            cbar = fig.colorbar(dmap)

        return left, right, disp
