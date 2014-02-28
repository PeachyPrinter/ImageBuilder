import os

class ImageBuilder(object):
    
    def __init__(self, source_folder, output_file, mapper):
        if (not os.path.exists(source_folder)):
            print("Source folder %s does not exist or is not accessable" % source_folder)
            raise Exception("Source folder %s does not exist or is not accessable" % source_folder)
        images = self.load_images(source_folder)

    def load_images(self, source_folder):
        raise Exception("No Images")

    def run(self):
        pass


def main():
    ImageBuilder().run()

if __name__ == "__main__":
    main()