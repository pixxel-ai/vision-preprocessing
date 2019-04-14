import cv2
from pathlib import Path
from tqdm import tqdm
import numpy as np
from convenience_functions import delete_file, is_file
from transformations import *


class CropAndSave(object):

    """Function crops an image into width_division*height_division number of images and stores the output to OUTPUT_FOLDER
        -----------------------------------------------------Parameters-------------------------------------------------------
                        IM_FOLDER: Path to folder that contains all the images (type is PosixPath or WindowsPath)
                        MASK_FOLDER: Path to folder that contains all the masks (type is PosixPath or WindowsPath)
                        OUTPUT_FOLDER: Path to folder that crops will be stored in (type is PosixPath or WindowsPath)
                        IM_OUT: Name of folder in which cropped images should be stored, under OUTPUT_FOLDER (type is string)
                        MASK_OUT: Name of folder in which cropped masks should be stored, under OUTPUT_FOLDER (type is string)
                        width_division: Number of divisions to be put along width of the image (type is int)
                        height_division: Number of divisions to be put along height of the image (type is int)
                        size: Size of each crop before resizing
                        pre_resize: (width, height) Dimension that original image should be resized to before cropping (type : (int,int)) default is None, meaning no resizing will occur
                        resize_to: Dimension of final output image after cropping (type is (int,int)) default is None, meaning no resizing will occur
                        images_prefix: Prefix of all output Image crops (type is string)
                        images_ext: Extension with which crops should be saved with (type is string) Eg:'.png'
                        spatial_resolution_in: Spatial resolution of images in the dataset
                        spatial_resolution_out: The spatial resolution to which the images will be rescaled to
                        delete_filer_after_processing: If `True`, all the original files will be deleted after they have been processed
                        import_only:
                            'Roads' : Read only pixels of value = 1 for each mask
                            'Buildings' : Read only pixels of value = 2 for each mask
                        export_as:
                            'Roads' : Convert all non zero pixel values to 1 before saving each mask
                            'Buildings' : Convert all non zero pixel values to 2 before saving each mask
                        """

    def __init__(self, IM_FOLDER=Path.cwd()/'Images',
                 MASK_FOLDER=Path.cwd()/'Masks',
                 OUTPUT_FOLDER=Path.cwd(),
                 IM_OUT='Images',
                 MASK_OUT='Masks',
                 get_mask_from_image=Path('Mask'),
                 width_division=5,
                 height_division=None,
                 size=150,
                 spatial_resolution_in=None,
                 spatial_resolution_out=None,
                 pre_resize=None,
                 resize_to=None,
                 images_prefix=None,
                 images_ext='.png',
                 delete_files_after_processing: bool = False,
                 import_only='Roads',
                 export_as='Roads'):
            self.IM_FOLDER = IM_FOLDER
            self.MASK_FOLDER = MASK_FOLDER
            self.OUTPUT_FOLDER = OUTPUT_FOLDER
            self.IM_OUT = IM_OUT
            self.MASK_OUT = MASK_OUT
            self.get_mask_from_image = get_mask_from_image
            self.width_division = width_division
            if height_division:
                self.height_division = height_division
            else:
                self.height_division = width_division
            self.size = size
            self.resize_to = resize_to

            self.pre_resize = pre_resize
            if spatial_resolution_in is not None and spatial_resolution_out is not None:
                if spatial_resolution_in == spatial_resolution_out:
                    pass
                else:
                    self.pre_resize = 'spatial'
                    self.spatial_scale_factor = spatial_resolution_in / spatial_resolution_out

            self.images_prefix = images_prefix if images_prefix is not None else ''
            self.images_ext = images_ext
            self.delete_after_processing = delete_files_after_processing

            self.export_as = export_as
            self.import_only = import_only
            self.transformer = Transformer()

            if import_only == 'Roads':
                self.transformer.transforms.append(extract_roads)
            elif import_only == 'Buildings':
                self.transformer.transforms.append(extract_buildings)

            if export_as == 'Roads':
                self.transformer.transforms.append(convert_to_roads)
            elif export_as == 'Buildings':
                self.transformer.transforms.append(convert_to_buildings)

        
    @staticmethod
    def open_image(img_path, is_mask=False):   # Reads and returns image from img_path
            if is_mask:
                mask = cv2.imread(img_path.__str__(), cv2.IMREAD_GRAYSCALE)
                return mask
            img=cv2.imread(img_path.__str__())
            return img
       
    def crop_image(self,img):  # iterates through list of crops generated from image
            #col_division equals width division
            #row_division equals height division
            if self.height_division > 1:
                overlap_rows=(self.size*self.height_division-(np.shape(img))[0])/(self.height_division-1)   #overlap between crops along height
            elif self.height_division == 1:
                overlap_rows = 0
            else:
                raise ValueError('Height division cannot be negative')

            if self.width_division > 1:
                overlap_column=(self.size*self.width_division-(np.shape(img))[1])/(self.width_division-1)   #overlap between crops along width
            elif self.width_division == 1:
                overlap_column = 0
            else:
                raise ValueError('Width division cannto be negative')

            if overlap_rows<0 or overlap_column<0:
                raise ArithmeticError('Crop overlaps are negative. Please reconsider the cropping and size parameters specified')
            if self.height_division == 1 and self.width_division == 1:
                return img
            else:
                for row in range(self.height_division):
                        for col in range(self.width_division):
                            start_row=int(row*(self.size - overlap_rows))
                            start_col=int(col*(self.size - overlap_column))
                            yield(img[start_row:start_row+self.size,start_col:start_col+self.size,:])


    @staticmethod
    def make_dir(directory):                                                                         #creates directory, if it doesnt exist
        if (directory).exists()==False:
                print("Output file", directory, " doesn't exist.\nCreating output directory.")
                Path.mkdir(directory, parents=True, exist_ok=False)
    
    def save_image_crop(self,crop,image_name):                                                      #saves crop of an image with name as image_name
        location=self.OUTPUT_FOLDER/self.IM_OUT
        self.make_dir(location)
        cv2.imwrite((location/image_name).__str__(),crop)
        if is_file(location/image_name):
            return True
        else:
            raise IOError
    
    def save_mask_crop(self,crop,image_name):                                                       #saves crop of a mask
        location=self.OUTPUT_FOLDER/self.MASK_OUT
        self.make_dir(location)
        crop = self.transformer(crop)
        # noinspection PyRedundantParentheses
        cv2.imwrite((location/(image_name)).__str__(),crop)
        if is_file(location/image_name):
            return True
        else:
            raise IOError
    
    def make_name(self,name):                                                                       #returns name of crop
        return self.images_prefix + name + self.images_ext

    def presize(self,img):
        if self.pre_resize == 'spatial':
            self.pre_resize = (int(img.shape[1] * self.spatial_scale_factor), int(img.shape[0] * self.spatial_scale_factor))
        if self.pre_resize:
            return cv2.resize(img,self.pre_resize)
        return img
    
    def resize(self,img):
        if(self.resize_to):
            return cv2.resize(img,self.resize_to)
        return img

    def process(self):
        img_path_list = [pth for pth in self.IM_FOLDER.iterdir()]  # modify to search for png ,jpg , etc
        self.make_dir(self.OUTPUT_FOLDER)
        print("Cropping and saving images and masks from corresponding folders")
        for img_path in tqdm(img_path_list):
            img=self.open_image(img_path)            # Loads image
            img= self.presize(img)
            crop_number=1
            for crop in(self.crop_image(img)):
                    crop= self.resize(crop)
                    self.save_image_crop(crop,self.make_name(img_path.stem+'crop'+str(crop_number)))
                    crop_number+=1
            mask_path=self.get_mask_from_image(img_path)        # Sets corresponding mask path for given image path
            mask=self.open_image(mask_path, is_mask=True)            # Loads corresponding mask of image
            mask=self.presize(mask)
            crop_number=1
            for crop in(self.crop_image(mask)):
                    crop=self.resize(crop)
                    self.save_mask_crop(crop,self.make_name(img_path.stem+'crop'+str(crop_number)))
                    crop_number+=1
            if self.delete_after_processing:
                delete_file(img_path)
                delete_file((mask_path))
