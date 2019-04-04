from cropping import crop_and_save
from resize import change_and_save
from pathlib import Path




OUTPUT=Path("/home/abhishek/Documents/pixxel/imgprocessing")  
IM=Path.cwd()/'MyImages'
change_object=change_and_save(IM_FOLDER=IM,
                        OUTPUT_FOLDER=OUTPUT,
                        IM_OUT='Resized_Images',
                        pre_res=1,
                        final_res=2,
                        images_prefix='spacenet',
                        images_ext='.png')
"""count=multiprocessing.cpu_count()
print( " \n You have {0:1d} CPU's ".format(count))
pool= Pool(processes= count )
pool.map(change_object.process)"""
change_object.process()


OUTPUT2=Path("/home/abhishek/Documents/pixxel/imgprocessing")  

MASK=Path.cwd()/'Masks'
def co_mask(img_path):      #function that returns path of corresponding mask, when given path of image
        return(Path.cwd()/'Resized_Images'/img_path.name)#Path(img_path.parent)/'Masks'/img_path.name)

crop_object=crop_and_save(IM_FOLDER=Path.cwd()/'Resized_Images',
                          MASK_FOLDER=Path.cwd()/'Resized_Images',
                          OUTPUT_FOLDER=OUTPUT2,
                          IM_OUT='Images',
                          MASK_OUT='Masks',
                          co_mask=co_mask,
                          width_division=3,
                          height_division=3,
                          size=500,
                          images_prefix='spacenet',
                          resize_to=(500,500),
                          images_ext='.png')
crop_object.process()