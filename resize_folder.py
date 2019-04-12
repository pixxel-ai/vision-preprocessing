from pathlib import Path
import numpy as np
import cv2
from tqdm import tqdm
from .transformations import convert_to_roads

# from pathos.multiprocessing import ProcessingPool as Pool, cpu_count
# distribute_process = Pool(cpu_count())


class ResizeFolder(object):
    def __init__(self, image_folder, mask_folder,
                 output_img_folder, output_mask_folder,
                 rename_func, height, width):
        self.IM_FOLDER = Path(image_folder)
        self.MSK_FOLDER = Path(mask_folder)
        self.OUTPUT_IMG = Path(output_img_folder)
        self.OUTPUT_MSK = Path(output_mask_folder)
        self.OUTPUT_IMG.mkdir(exist_ok=True)
        self.OUTPUT_MSK.mkdir(exist_ok=True)

        self.rename_func = rename_func
        self.height = height
        self.width = width


    def open_image(self, PATH, is_mask=False):
        if is_mask:
            mask = cv2.imread(str(PATH), cv2.IMREAD_GRAYSCALE)
            mask = convert_to_roads(mask).astype(np.uint8)
            return mask
        else:
            return cv2.imread(str(PATH))


    def save_image(self, image, img_path, is_mask=False):
        name = self.rename_func(img_path)
        if is_mask:
            cv2.imwrite(str(self.OUTPUT_MSK / name), image)
        else:
            cv2.imwrite(str(self.OUTPUT_IMG / name), image)


    def resize_image(self, image):
        return cv2.resize(image, (self.width, self.height))


    def process_images(self):
        for img_path in tqdm(self.IM_FOLDER.iterdir()):
            self.process_one_item(img_path)


    def process_masks(self):
        for mask_path in tqdm(self.MSK_FOLDER.iterdir()):
            self.process_one_item(mask_path, is_mask=True)


    def process_one_item(self, img_path, is_mask=False):
        img = self.open_image(img_path, is_mask)
        img = self.resize_image(img)
        self.save_image(img, img_path, is_mask)
        return True
