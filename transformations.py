#%%
import numpy as np
import cv2
import matplotlib.pyplot as plt
from pathlib import Path

#%%
class Transformer(object):
    """
    This class applies a list of functions (transforms) to any given image / mask
    Transforms will be applied in the order they are passed in the list
    A transform function is assumed to behave like so:
        transform( image_object ) -> image_object
        where the returned image_object is of the same size as the original image_object

    :returns: A callable instance of a class that applies all the transforms to the passed image_object

    Example usage :
    img = cv2.imread(file_path)
    transformer = Transformer([extract_roads, convert_to_roads])
    img = transformer(img)

    """
    def __init__(self, transforms: list=[]):
        """
        :param transforms: List of functions to be applied to image on calling class.
        """
        self.transforms = transforms

    def __call__(self, img):

        for transformation in self.transforms:
            img = transformation(img)

        return img.astype(np.int)

#%%
def extract_roads(mask):
    """
    Takes as input a Mask, and Sets all non-road pixels to Zero.
    A Roads pixel is defined as a Pixel with value = 1
    :param mask: Mask. Type : numpy.ndarray
    :return: Mask with Roads only
    """
    return extract_number_from_image(mask, 1)

def extract_buildings(mask):
    """
    Takes as input a Mask, and Sets all non-building pixels to Zero.
    A Building pixel is defined as a Pixel with value = 2
    :param mask: Mask. Type : numpy.ndarray
    :return: Mask with Buildings only
    """
    return extract_number_from_image(mask, 2)

def extract_number_from_image(img: np.ndarray, number: int =1):
    return (img == number) * number

def convert_to_roads(mask):
    """
    Equalize all values in mask to Road-pixels
    A Road-pixel has value 1
    :param mask: Mask to equalize
    :return: Returns equalized mask

    """
    return (mask != 0)

def convert_to_buildings(mask):
    """
    Equalize all values in mask to Road-pixels
    A Road-pixel has value 1
    :param mask: Mask to equalize
    :return: Returns equalized mask

    """
    return (mask != 0) * 2

#%%
if __name__ == '__main__':
    # mask_path = Path('TMP/23729080_15.png')
    mask_path = Path('MSK_OUT/I_5crop4.png')
    if mask_path.is_file():
        mask = cv2.imread(str(mask_path), cv2.IMREAD_GRAYSCALE)
        transformer = Transformer([return_as_roads])
        plt.imshow(transformer(mask))
        plt.show()
