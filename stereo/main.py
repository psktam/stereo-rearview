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
        if self.left_cam is not None and not self.left_cam.isOpen():
            self.left_cam = cv2.VideoCapture(self.cam_left_ind)
        if self.right_cam is not None and not self.right_cam.isOpen():
            self.right_cam = cv2.VideoCapture(self.cam_right_ind)

    def shut_eyes(self):
        if self.left_cam is not None and self.left_cam.isOpen():
            self.left_cam.release()
        if self.right_cam is not None and self.right_cam.isOpen():
            self.right_cam.release()

    def acquire_scene(self):
        ret_left, img_left = self.left_cam.read()
        ret_right, img_right = self.right_cam.read()

        return ret_left and ret_right, img_left, img_right

    def construct_depth_map(self, img_left, img_right):
        """
        This method constructs the depth map from two images.

        :param img_left:
        :param img_right:
        :return:
        """
        disparities = self.disparity_generator.compute(img_left, img_right)
