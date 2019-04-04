from PIL import Image
import cv2
from pathlib import Path
import pandas
from tqdm import tqdm
import numpy as np
import os
import shutil
import sys
class change_and_save(object):
    """Function resizes the spatial resolution of the image and then stores the output in the OUTPUT FOLDER
        -----------------------------------------------------Parameters-------------------------------------------------------
                        IM_FOLDER:Path to folder that contains all the images (type is PosixPath or WindowsPath)
                        OUTPUT_FOLDER:Path to folder that crops will be stored in (type is PosixPath or WindowsPath)
                        IM_OUT:Name of folder in which new images should be stored, under OUTPUT_FOLDER (type is string)
                        images_prefix= prefix of all output resized images ( type string)
                        pre_res:The original resolution to be entered by the user (type integer)
                        final_res:The final resolution in which it is to be converted (type is int)
                        width= width of the image in pixels, to be entered by the user ( type int, None by default)
                        height= height of the image in pixels, to be entered by the user (type int, None by default)
                        images_ext:Extension with which crops should be saved with (type is string) Eg:'.png'"""
    
    def __init__(self,IM_FOLDER=Path.cwd()/'Images',
                 OUTPUT_FOLDER=Path.cwd(),
                 IM_OUT='Images',
                 images_prefix=None,
                 width=None,
                 pre_res= None,
                 final_res=None,
                 height=None,
                 images_ext='.png'):
            self.IM_FOLDER=IM_FOLDER
            self.OUTPUT_FOLDER=OUTPUT_FOLDER
            self.IM_OUT=IM_OUT
            self.images_prefix= images_prefix
            self.images_ext=images_ext
            self.width=width
            self.height=height
            self.pre_res=pre_res
            self.final_res=final_res
    def open_image(self,img_path):                                                                  #Reads and returns image from img_path
            img=cv2.imread(img_path.__str__())
            if img is not None:
                return img
            else:
                print("\n ERROR! image not read, exiting the code")
                sys.exit()
                
       
    def change_resolution(self,img):                                                                       #iterates through list of images
            # given initial and final ppi's we can resize pixels by multiplying them by respective factors
            factor= self.final_res / self.pre_res
            self.height=(np.shape(img))[0]
            self.width= (np.shape(img))[1]            
            img2 = cv2.resize(img,(int(self.width*factor), int(self.height*factor)), Image.BICUBIC)
            if img2 is not None:
                yield img2
            else:
                print("\n ERROR! image not resized, exiting the code")
                sys.exit()
                
            
    def make_dir(self,dir):                                                                         #creates directory, if it doesnt exist
        if((dir).exists()==False):
                print("Output file",dir," doesn't exist.\nCreating output directory.")
                Path.mkdir(dir,parents=True, exist_ok=False)
    
    def save_final_image(self,img2,image_name):                                                      #saves crop of an image with name as image_name
        location=self.OUTPUT_FOLDER/self.IM_OUT
        self.make_dir(location)
        cv2.imwrite((location/image_name).__str__(),img2)
    
    
    def make_name(self,name):                                                                       #returns name of crop
        return(self.images_prefix+name+self.images_ext)
    
    def process(self): #first function to be made
        img_path_list = [pth for pth in self.IM_FOLDER.iterdir()]  #modify to search for png ,jpg , etc
        self.make_dir(self.OUTPUT_FOLDER)
        print("Resizing and saving the new images")
        print("\n Do you want to delete the original Images  ?")
        ch=input("\n Type y/n") 
        
        if ch=='y':
            for img_path in tqdm(img_path_list):
                img=self.open_image(img_path)
                img_number=1
                for img2 in(self.change_resolution(img)):
                        self.save_final_image(img2,self.make_name(img_path.stem+'new'+str(img_number)))
                        img_number+=1
                        os.remove(img_path) 
        else:
            for img_path in tqdm(img_path_list):
                img=self.open_image(img_path)
                img_number=1
                for img2 in(self.change_resolution(img)):
                        self.save_final_image(img2,self.make_name(img_path.stem+'new'+str(img_number)))
                        img_number+=1
                
###################################################    SAMPLE      ########################################################

