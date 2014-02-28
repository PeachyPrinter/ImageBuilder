import unittest
import os
import sys
import cv2

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..','src'))

from mapper import Mapper

class MapperTest(unittest.TestCase):
    test_data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'TestData')

    def test_given_an_image_point_map_returned(self):
        img = cv2.imread(os.path.join(self.test_data_path,'SimpleTestImage1.png'),1)
        expected = [i for i in range(0,20)]
        colour = [255,255,255]
        threshold = 0
        mapper = Mapper(colour,threshold)
        actual = mapper.get_points(img)
        self.assertEquals(expected,actual)

    def test_given_an_image_with_non_complete_points_a_point_map_returned(self):
        img = cv2.imread(os.path.join(self.test_data_path,'SimpleTestImage4.png'),1)
        expected = [-1,-1] + [i for i in range(2,9)] + [-1,-1] + [i for i in range(11,18)] + [-1,-1]
        colour = [255,255,255]
        threshold = 0
        mapper = Mapper(colour,threshold)
        actual = mapper.get_points(img)
        self.assertEquals(expected,actual)

    def test_given_an_image_with_no_points_a_point_map_returned(self):
        img = cv2.imread(os.path.join(self.test_data_path,'SimpleTestImage5.png'),1)
        expected = [-1 for i in range(0,20)]
        colour = [255,255,255]
        threshold = 0
        mapper = Mapper(colour,threshold)
        actual = mapper.get_points(img)
        self.assertEquals(expected,actual)

    def test_given_an_colour_image_and_specific_colour_a_point_map_returned(self):
        img = cv2.imread(os.path.join(self.test_data_path,'SimpleTestImage2.png'),1)
        expected = [i for i in range(0,20)]
        colour = [255,128,0]
        threshold = 0
        mapper = Mapper(colour,threshold)
        actual = mapper.get_points(img)
        self.assertEquals(expected,actual)

    def test_given_a_threshold_items_in_threshold_work_for_red(self):
        img = cv2.imread(os.path.join(self.test_data_path,'RedThresholdTest.png'),1)
        threshold = 20
        expected = [0,0,0,-1,-1] 
        colour = [128,128,128]
        mapper = Mapper(colour, threshold)
        actual = mapper.get_points(img)
        self.assertEquals(expected,actual)

    def test_given_a_threshold_items_in_threshold_work_for_green(self):
        img = cv2.imread(os.path.join(self.test_data_path,'GreenThresholdTest.png'),1)
        threshold = 20
        expected = [0,0,0,-1,-1] 
        colour = [128,128,128]
        mapper = Mapper(colour, threshold)
        actual = mapper.get_points(img)
        self.assertEquals(expected,actual)

    def test_given_a_threshold_items_in_threshold_work_for_blue(self):
        img = cv2.imread(os.path.join(self.test_data_path,'BlueThresholdTest.png'),1)
        threshold = 20
        expected = [0,0,0,-1,-1] 
        colour = [128,128,128]
        mapper = Mapper(colour, threshold)
        actual = mapper.get_points(img)
        self.assertEquals(expected,actual)

    def test_a_threshold_can_be_changed(self):
        img = cv2.imread(os.path.join(self.test_data_path,'GreenThresholdTest.png'),1)
        initial_threshold = 20
        new_threshold = 21
        expected = [0,0,0,0,0] 
        colour = [128,128,128]
        mapper = Mapper(colour, initial_threshold)
        mapper.set_threshold(new_threshold)
        actual = mapper.get_points(img)
        self.assertEquals(expected,actual)

    def test_a_colour_can_be_changed(self):
        img = cv2.imread(os.path.join(self.test_data_path,'GreenThresholdTest.png'),1)
        threshold = 20
        initial_expected = [0,0,0,-1,-1] 
        initial_colour = [128,128,128]
        new_expected = [-1,-1,-1,-1,-1]
        new_colour = [64,64,64]
        mapper = Mapper(initial_colour, threshold)
        initial_result = mapper.get_points(img)
        self.assertEquals(initial_expected,initial_result)

        mapper.set_colour(new_colour)
        new_result = mapper.get_points(img)
        self.assertEquals(new_expected,new_result)


unittest.main()