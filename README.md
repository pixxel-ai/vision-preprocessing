# CHANGE SPATIAL RESOLUTION AND CROP #
### code to change spatial resolution of Images and crop Images and Masks ###
                (The code involves three python files as stated below )



*****************************************************************************************************************************



#### Files involved :- ####

* ##### resize.py #####
    Class *change_and_save* changes the spatial resolution of the images.
      
     It asks for corresponding deletion of original images from the user from the original image folder.
    
    
     The Parameters involved are :- 
    * *IM_FOLDER* : Path to folder that contains all the images (type is PosixPath or WindowsPath)
    * *OUTPUT_FOLDER* : Path to folder that crops will be stored in (type is PosixPath or WindowsPath)
    * *IM_OUT* : Name of folder in which new images should be stored, under OUTPUT_FOLDER (type is string)
    * *images_prefix* : Prefix of all output resized images (type string)
    * *pre_res* : The original resolution to be entered by the user (type integer)
    * *final_res* : The final resolution in which it is to be converted (type is int)
    * *width* : Width of the image in pixels, to be entered by the user ( type int, None by default)
    * *height* : height of the image in pixels, to be entered by the user (type int, None by default)
    * *images_ext* : Extension with which crops should be saved with (type is string) Eg:'.png'
    
        
       Functions involved are ( names are self-explanatory ) :-
    * *open_image* 
    * *change_resolution* : changes the resolution by respective multiplication of dimensions by the factor desired
    * *make_dir*
    * *save_final_image*
    * *process* : iterates over the image files in the input folder,
                  also asks for user's choice to delete the original images or not 

* ##### cropping.py #####
    Class *crop_and_save* creates crops 
    To crop an image (and the masks) into width_division*height_division number of images and store the output to             OUTPUT_FOLDER
    The Parameters involved are :-
    *  *IM_FOLDER*:Path to folder that contains all the images (type is PosixPath or WindowsPath)
    *  *MASK_FOLDER*:Path to folder that contains all the masks (type is PosixPath or WindowsPath)
    *  *OUTPUT_FOLDER* : Path to folder that crops will be stored in (type is PosixPath or WindowsPath)
    *  *IM_OUT* : Name of folder in which cropped images should be stored, under OUTPUT_FOLDER (type is string)
    *  *MASK_OUT* : Name of folder in which cropped masks should be stored, under OUTPUT_FOLDER (type is string)
    *  *width_division* : Number of divisions to be put along width of the image (type is int)
    *  *height_division* : Number of divisions to be put along height of the image (type is int)
    *  *size* : Desired dimension of the output cropped images (type is int)
    *  *pre_resize* : Dimension that original image should be resized to before cropping (typr is (int,int)) default is None,                       meaning no resizing will occur
    *  *resize_to* : Dimension of final output image after cropping (type is (int,int)) default is None, meaning no resizing                       will occur
    *  *images_prefix* : Prefix of all output Image crops (type is string)
    *  *images_ext* : Extension with which crops should be saved with (type is string) Eg:'.png'
      Functions involved are (names are self explanatory ) :-
    * *open_image* 
    * *crop_image* : crops the input image using basic mathematics by counting the number of overlaps which would be created
    * *make_dir* : makes an output directory if it is already not existing
    * *save_image_crop*
    * *save_mask_crop*
    * *make_name* : to generate names for the final images
    * *presize* : in case dont want to execute spatial resolution
    * *resize* : to resize the final crop
    * *process* : iterates over the images and masks to crop, resize and save them
    
* ##### cropandresize.py #####
    The file to combine the functionalities of both other files. It firsts implements spatial resolution on the images (using an object of change_and_save) and then passes it on along with the masks for cropping (to cropping.py).
    

*****************************************************************************************************************************



### MODULES/PACKAGES USED ###
  * **pathlib** : for retrieving and assigning paths to directories and images
  * **PIL** :  for opening, manipulating, and saving different image file formats
  * **cv2** : to solve computer vision problems and to integrate with other libraries that use Numpy  
  * **pandas** : for data manipulation and analysis
  * **tqdm** : for progress bars
  * **numpy** :  for Scientific Computing of various data types
  * **os** : for using operating system dependent functionality (like deletion of original images)
  
  Some changes and updates are still in progress for better results and added features.
  * **sys** : for using exit() function
    

