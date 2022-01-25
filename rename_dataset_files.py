#rename dataset files
import os

# DIRECTORY = "/home/elif/Documents/my_virtual_env/TFODCourse/BitirmeTezi/archive/Dataset/with_mask"
# DIRECTORY = "/home/elif/Documents/my_virtual_env/TFODCourse/BitirmeTezi/archive/Dataset/without_mask"
DIRECTORY = "/home/elif/Documents/my_virtual_env/TFODCourse/BitirmeTezi/archive/Dataset/mask_weared_incorrect"

for dirname, _, filenames in os.walk( DIRECTORY ):
    for filename in filenames:

        old_name = os.path.join(dirname, filename)
        new_name = old_name[:-4] + 'mwi' + old_name[-4:]
        os.rename(old_name, new_name)
        