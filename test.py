from cropping import crop_and_save
from convenience_functions import find_number_in_string
from pathlib import Path

IM_FOLDER = Path('/Users/akash/Desktop/AI/Pixxel/Roads/Datasets/GANModel Data/Test_Cropped_Images')
MSK_FOLDER = Path('/Users/akash/Desktop/AI/Pixxel/Roads/Datasets/GANModel Data/Test_Cropped_Masks')


def get_mask_name(im_path, MSK_FOLDER=MSK_FOLDER, prefix='M_', suffix='.png'):
    name = (prefix + str(find_number_in_string(im_path)) + suffix)
    return MSK_FOLDER / name




#%%
processor = crop_and_save(IM_FOLDER=IM_FOLDER,
                         MASK_FOLDER=MSK_FOLDER,
                         OUTPUT_FOLDER=Path.cwd(),
                         IM_OUT='IM_OUT',
                         MASK_OUT='MSK_OUT',
                         co_mask=get_mask_name,
                         width_division=2,
                         height_division=None,
                         size=64,
                         spatial_resolution_in=1,
                         spatial_resolution_out=2,
                         pre_resize=None,
                         resize_to=None,
                         images_prefix=None,
                         images_ext='.png')



#%%
processor.process()

