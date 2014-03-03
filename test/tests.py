import unittest
import os
import sys
import cv2
import numpy
from numpy import array, uint8
from mock import patch
from testhelpers import TestHelpers


sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..','src'))

from mapper import Mapper
from image_builder import ImageBuilder, ImageBuilderApi

class MapperTest(unittest.TestCase, TestHelpers):
    test_data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_data')

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

    def test_get_threshold_array_given_an_image_point(self):
        img = cv2.imread(os.path.join(self.test_data_path,'SimpleTestImage1.png'),1)
        def test(x,y):
            if x == y: 
                return 255
            else:
                return 0
        expected = [[test(x,y) for x in range(0,20)] for y in range(0,20)]
        
        colour = [255,255,255]
        threshold = 0
        mapper = Mapper(colour,threshold)
        actual = mapper.get_threshold_array(img)
        self.assertNumpyArrayEquals(expected,actual)

    def test_given_an_colour_image_and_specific_colour_a_point_map_returned(self):
        img = cv2.imread(os.path.join(self.test_data_path,'SimpleTestImage2.png'),1)
        def test(x,y):
            if x == y: 
                return 255
            else:
                return 0
        expected = [[test(x,y) for x in range(0,20)] for y in range(0,20)]
        colour = [255,128,0]
        threshold = 0
        mapper = Mapper(colour,threshold)
        actual = mapper.get_threshold_array(img)
        self.assertNumpyArrayEquals(expected,actual)

class ImageBuilderApiTest(unittest.TestCase, TestHelpers):
    test_image_1 = array([[[255, 255, 255],[0, 0, 0],[  0,   0,   0]]], dtype=uint8)
    test_image_2 = array([[[0, 0, 0],[255, 255, 255],[  0,   0,   0]]], dtype=uint8)
    test_image_3 = array([[[0, 0, 0],[0, 0, 0],[255, 255, 255]]], dtype=uint8)

    @patch('mapper.Mapper')
    def test_given_an_empty_seq_should_return_None(self, mock_mapper):
        iba = ImageBuilderApi(mock_mapper)
        result = iba.merge([])
        self.assertEquals(None, result)
        self.assertFalse(mock_mapper.called)

    @patch('mapper.Mapper')
    def test_given_an_image_seq_of_one_should_return_image(self, mock_mapper):
        mock = mock_mapper.return_value
        mock.get_threshold_array.return_value = self.test_image_1
        iba = ImageBuilderApi(mock)
        
        result = iba.merge([self.test_image_2])
        
        self.assertNumpyArrayEquals(self.test_image_1, result)
        self.assertEquals(1, mock.get_threshold_array.call_count)

    @patch('mapper.Mapper')
    def test_given_an_image_seq_of_many_should_merged_image(self, mock_mapper):
        expected_image = [[[255, 255, 255],[255, 255, 255],[255, 255, 255]]]
        list_of_return_values= [self.test_image_1,self.test_image_2,self.test_image_3]
        def side_effect(self):
            return list_of_return_values.pop()
        mock = mock_mapper.return_value
        mock.get_threshold_array.side_effect = side_effect

        iba = ImageBuilderApi(mock)
        
        result = iba.merge([self.test_image_1,self.test_image_2,self.test_image_3])
        
        self.assertNumpyArrayEquals(expected_image, result)
        self.assertEquals(3, mock.get_threshold_array.call_count)

class ImageBuilderTest(unittest.TestCase):
    test_data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_data')
    source_image_path = os.path.join(test_data_path, 'source_images')
    test_output_file = 'out.png'
    stub_image_builder_api = None
    test_image_1 = array([[[255, 255, 255],[0, 0, 0],[  0,   0,   0]]], dtype=uint8)
    
    def setUp(self):
        if os.path.exists(self.test_output_file):
            os.remove(self.test_output_file)

    def test_ImageBuilder_should_throw_exception_if_bad_directory_found(self):
        source_folder = "does_not_exist"
        passed = False
        
        try:
            image_builder = ImageBuilder(None)
            image_builder.build(source_folder, self.test_output_file)
        except:
            passed = True

        self.assertTrue(passed)

    def test_ImageBuilder_should_throw_exception_if_no_images(self):
        source_folder = os.path.dirname(os.path.abspath(__file__))

        try:
            image_builder = ImageBuilder(None)
            image_builder.build(source_folder, self.test_output_file)
            passed = False
        except Exception as ex:
            passed = True

        self.assertTrue(passed)

    @patch('image_builder.ImageBuilderApi')
    def test_ImageBuilder_should_call_ImageBuilderAPI_with_file_seq(self, mock_api):
        mock_image_builder_api = mock_api.return_value
        mock_image_builder_api.merge.return_value = self.test_image_1

        image_builder = ImageBuilder(mock_image_builder_api)
        image_builder.build(self.source_image_path, self.test_output_file)

        self.assertEquals(1, mock_image_builder_api.merge.call_count)
        self.assertEquals(3, len(list(mock_image_builder_api.merge.call_args_list[0][0][0])))
        self.assertTrue(os.path.exists(self.test_output_file))
        




unittest.main()