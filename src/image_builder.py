import os
import cv2

class ImageBuilderApi(object):
    def __init__(self, mapper):
        self.mapper = mapper

    def _merge_images(self,image1,image2):
        merged_image = cv2.addWeighted(image1,1.0,image2,1.0,0)
        return merged_image

    def merge(self,image_seq):
        modified_image = None
        for image in image_seq:
            current_mapped_image = self.mapper.get_threshold_array(image)
            if modified_image == None:
                modified_image = current_mapped_image
            else:
                modified_image = self._merge_images(modified_image, current_mapped_image)
        return modified_image


class ImageBuilder(object):
    VALID_EXTENSIONS = ['jpg','jpeg','png']
    def __init__(self,image_builder_api):
        self.image_builder_api = image_builder_api

    def _valid_image(self, filename):
        extension = filename.split('.')[-1]
        if ( extension in self.VALID_EXTENSIONS ):
            return True
        else:
            print('%s is not a valid image' % extension)
            return False

    def _load_images(self, source_folder):
        working_dir = os.getcwd()
        if (0 == len ( [ f for f in os.listdir(source_folder) if self._valid_image(f) ])):
            raise Exception('No image files with extension png. jpg or jpeg found')

        for afile in os.listdir(source_folder):
            if self._valid_image(afile):
                path_to_file = os.path.join(working_dir, source_folder, afile)
                yield cv2.imread(path_to_file, 1)

    def build(self,source_folder, output_file):
        if (not os.path.exists(source_folder)):
            print("Source folder %s does not exist or is not accessable" % source_folder)
            raise Exception("Source folder %s does not exist or is not accessable" % source_folder)
        image_seq = self._load_images(source_folder)
        merged_image = self.image_builder_api.merge(image_seq)
        cv2.imwrite(output_file,merged_image)


def main():
    ImageBuilder().run()

if __name__ == "__main__":
    main()