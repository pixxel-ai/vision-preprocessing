import cv2
from pathlib import Path
import pandas
from tqdm import tqdm
import numpy as np

class crop_and_save(object):
    """Function crops an image into width_division*height_division number of images and stores the output to OUTPUT_FOLDER
        -----------------------------------------------------Parameters-------------------------------------------------------
                        IM_FOLDER:Path to folder that contains all the images (type is PosixPath or WindowsPath)
                        MASK_FOLDER:Path to folder that contains all the masks (type is PosixPath or WindowsPath)
                        OUTPUT_FOLDER:Path to folder that crops will be stored in (type is PosixPath or WindowsPath)
                        IM_OUT:Name of folder in which cropped images should be stored, under OUTPUT_FOLDER (type is string)
                        MASK_OUT:Name of folder in which cropped masks should be stored, under OUTPUT_FOLDER (type is string)
                        width_division:Number of divisions to be put along width of the image (type is int)
                        height_division:Number of divisions to be put along height of the image (type is int)
                        size:Desired dimension of the output cropped images (type is int)
                        pre_resize:Dimension that original image should be resized to before cropping (typr is (int,int)) default is None, meaning no resizing will occur
                        resize_to:Dimension of final output image after cropping (type is (int,int)) default is None, meaning no resizing will occur
                        images_prefix:Prefix of all output Image crops (type is string)
                        images_ext:Extension with which crops should be saved with (type is string) Eg:'.png'"""
    
    def __init__(self,IM_FOLDER=Path.cwd()/'Images',
                 MASK_FOLDER=Path.cwd()/'Masks',
                 OUTPUT_FOLDER=Path.cwd(),
                 IM_OUT='Images',
                 MASK_OUT='Masks',
                 co_mask=Path('Mask'),
                 width_division=5,
                 height_division=None,
                 size=150,
                 pre_resize=None,
                 resize_to=None,
                 images_prefix=None,
                 images_ext='.png'):
            self.IM_FOLDER=IM_FOLDER
            self.MASK_FOLDER=MASK_FOLDER
            self.OUTPUT_FOLDER=OUTPUT_FOLDER
            self.IM_OUT=IM_OUT
            self.MASK_OUT=MASK_OUT
            self.co_mask=co_mask
            self.width_division=width_division
            if(height_division):
                self.height_division=height_division
            else:
                self.height_division=width_division
            self.size=size
            self.resize_to=resize_to
            self.pre_resize=pre_resize
            self.images_prefix=images_prefix
            self.images_ext=images_ext
        
    def open_image(self,img_path):                                                                  #Reads and returns image from img_path
            img=cv2.imread(img_path.__str__())
            return img
       
    def crop_image(self,img):                                                                       #iterates through list of crops generated from image
            #col_division equals width division
            #row_division equals height division
            delta_row=(self.size*self.height_division-(np.shape(img))[0])/(self.height_division-1)   #overlap between crops along height
            delta_col=(self.size*self.width_division-(np.shape(img))[1])/(self.width_division-1)   #overlap between crops along width
            if delta_row<0 or delta_col<0:
                print()
            for row in range(self.height_division):
                    for col in range(self.width_division):
                        start_row=int(row*(self.size -delta_row))
                        start_col=int(col*(self.size -delta_col))
                        yield(img[start_row:start_row+self.size,start_col:start_col+self.size,:]) 
                    #crop = cv2.resize(crop,(resize_to,resize_to))
   
    def make_dir(self,dir):                                                                         #creates directory, if it doesnt exist
        if((dir).exists()==False):
                print("Output file",dir," doesn't exist.\nCreating output directory.")
                Path.mkdir(dir,parents=True, exist_ok=False)
    
    def save_image_crop(self,crop,image_name):                                                      #saves crop of an image with name as image_name
        location=self.OUTPUT_FOLDER/self.IM_OUT
        self.make_dir(location)
        cv2.imwrite((location/image_name).__str__(),crop)
    
    def save_mask_crop(self,crop,image_name):                                                       #saves crop of a mask
        location=self.OUTPUT_FOLDER/self.MASK_OUT
        self.make_dir(location)
        cv2.imwrite((location/(image_name)).__str__(),crop)
    
    def make_name(self,name):                                                                       #returns name of crop
        return(self.images_prefix+name+self.images_ext)

    def presize(self,img):
        if(self.pre_resize):
            return cv2.resize(img,(self.pre_resize))
        return img
    
    def resize(self,img):
        if(self.resize_to):
            return cv2.resize(img,(self.resize_to))
        return img

    def process(self):
        img_path_list = [pth for pth in self.IM_FOLDER.iterdir()]  #modify to search for png ,jpg , etc
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
            mask_path=self.co_mask(img_path)        # Sets corresponding mask path for given image path 
            mask=self.open_image(mask_path)            # Loads corresponding mask of image
            mask=self.presize(mask)
            crop_number=1
            for crop in(self.crop_image(mask)):
                    crop=self.resize(crop)
                    self.save_mask_crop(crop,self.make_name(img_path.stem+'crop'+str(crop_number)))
                    crop_number+=1

###################################################    SAMPLE      ########################################################


IM=Path.cwd()/'Images'