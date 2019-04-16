from cropping import CropAndSave
from convenience_functions import find_number_in_string
from pathlib import Path

IM_FOLDER = Path('/Users/akash/Desktop/AI/Pixxel/Roads/Datasets/GANModel Data/mass_IMAGES_TEST copy')
MSK_FOLDER = Path('/Users/akash/Desktop/AI/Pixxel/Roads/Datasets/GANModel Data/mass_MASKS_TEST copy')


def get_mask_name__(im_path, MSK_FOLDER=MSK_FOLDER, prefix='M_', suffix='.png'):
    name = (prefix + str(find_number_in_string(im_path)) + suffix)
    return MSK_FOLDER / name

def get_mask_name(im_path, MSK_FOLDER=MSK_FOLDER, prefix='M_', suffix='.png'):
    name = im_path.stem + suffix
    return MSK_FOLDER / name


#%%
processor = CropAndSave(IM_FOLDER=IM_FOLDER,
                        MASK_FOLDER=MSK_FOLDER,
                        OUTPUT_FOLDER=Path.cwd(),
                        IM_OUT='IM_OUT',
                        MASK_OUT='MSK_OUT',
                        get_mask_from_image=get_mask_name,
                        width_division=4,
                        height_division=3,
                        size=1500,
                        # spatial_resolution_in=1,
                        # spatial_resolution_out=1,
                        pre_resize=None,
                        resize_to=None,
                        images_prefix=None,
                        images_ext='.png',
                        delete_files_after_processing=True,
                        import_only='Buildings',
                        export_as='Buildings')



#%%
processor.process()

