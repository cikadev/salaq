import os


class Meshroom:
    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir

    def execute(self):
        os.system("~/Projects/meshroom/meshroom_photogrammetry --input {} --output {}".format(self.input_dir,
                                                                                              self.output_dir))
