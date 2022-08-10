import PIL.Image

from dfpy.steps.step import Step


class Image(Step):
    """Outputs an image from a file
    """
    def __init__(self, filename, color_space='HSV', shape=None, name="Image"):
        """Creates an Image.

        :param string filename: filename of the image
        :param string color_space: color space of the step output (HSV or RGB)
        :param tuple of ints shape: shape of the image (the image is resized if necessary)
        :param string name: name of the step
        """

        super().__init__(shape=shape, static=True, name=name)

        self._filename = filename

        self._image = PIL.Image.open(filename)
        self._image = self._image.convert(color_space)

        if shape is not None:
            self._image = self._image.resize(shape)
        else:
            self._shape = self._image.size

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, filename):
        self._filename = filename

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, image):
        self._image = image
