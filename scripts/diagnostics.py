from itertools import product

import matplotlib.pyplot as plt
import cv2

import stereo.main as sm


def generate_many_comparisons(num_disparities, blocksizes, target_dir):
    """
    This function tests the generation of disparity maps for given num_disparities and
    blocksizes.

    :param num_disparities: a list of num-disparities to try
    :param blocksizes: a list of block sizes to try
    :param target_dir: Where all the test images will get dumped
    :return:
    """
    combos = product(num_disparities, blocksizes)
    stereo_viewer = sm.StereoViewerMain(cam_index_left=1, cam_index_right=0,
                                        num_disparities=0, blocksize=0)
    stereo_viewer.open_eyes()
    for x in range(100):
        stereo_viewer.acquire_scene()

    for num_disp, bsize in combos:
        stereo_viewer.disparity_generator = cv2.StereoBM_create(numDisparities=num_disp,
                                                                blockSize=bsize)
        left, right, disparity = stereo_viewer.make_triptych(generate_plots=False)

        fig = plt.figure(figsize=(27.0, 8.5))
        fig.suptitle("Num disparities: {nd}, Blocksize: {bs}".format(nd=num_disp, bs=bsize))
        axe_left = fig.add_subplot(131)
        axe_right = fig.add_subplot(132)
        axe_disp = fig.add_subplot(133)

        axe_left.imshow(left)
        axe_right.imshow(right)
        axe_disp.imshow(disparity)

        generated_name = "ndis_{}_bsize_{}".format(num_disp, bsize)
        image_filename = "{tdir}_{gen}.png".format(tdir=target_dir, gen=generated_name)
        fig.savefig(image_filename)

        plt.close(fig)


if __name__ == '__main__':
    generate_many_comparisons(range(16, 16 * 20, 16), range(15, 201, 2), 'test_images/')