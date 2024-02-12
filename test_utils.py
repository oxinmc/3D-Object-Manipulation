import unittest
import os
import json
from utils import next_and_previous_index, create_new_files



class TestUtilsGeneral(unittest.TestCase):
    
    #Test case for next_and_previous_index
    def test_next_and_previous_index(self):
        self.assertEqual(next_and_previous_index(3, 3), (0,2))
        self.assertEqual(next_and_previous_index(2, 3), (3,1))


class TestUtilsJSONFileCreation(unittest.TestCase):

    def setUp(self):
        #Set up preconditions for the test
        self.quadrilateral_test_data = [[[-3.0, 0.0, 0.1], [-2.9, 0.0, 0.5], [-2.9, 0.5, 0.5], [-2.9, 0.5, 0.1]],
                                        [[-3.0, 0.0, 0.1], [-2.9, 0.0, 0.5], [-2.9, 0.5, 0.5], [-2.9, 0.5, 0.1]],
                                        [[-2.8, -0.5, 0.0], [-2.8, 0.0, -0.5], [-2.5, 0.0, 0.0], [-2.5, 0.5, 0.0]],
                                        [[-2.0, -2.5, 0.0], [-2.0, 0.0, -2.5], [-2.0, 0.0, 0.0], [-2.0, 0.5, 0.5]],
                                        [[0.0, -2.9, -0.1], [0.1, -2.9, -0.5], [0.5, -2.9, -0.5], [0.5, -2.9, -0.1]]]
        self.filename = 'test_data'

        self.expected_result = {"q": [[0, 1, 2, 3], [0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]], 
                                "p": [[-3.0, 0.0, 0.1], [-2.9, 0.0, 0.5], [-2.9, 0.5, 0.5], [-2.9, 0.5, 0.1], [-2.8, -0.5, 0.0],
                                      [-2.8, 0.0, -0.5], [-2.5, 0.0, 0.0], [-2.5, 0.5, 0.0], [-2.0, -2.5, 0.0], [-2.0, 0.0, -2.5], 
                                      [-2.0, 0.0, 0.0], [-2.0, 0.5, 0.5], [0.0, -2.9, -0.1], [0.1, -2.9, -0.5], [0.5, -2.9, -0.5], [0.5, -2.9, -0.1]
                                      ]
                                }

    def tearDown(self):
        #Clean up any resources created during the test (if needed)
        if os.path.exists(f'resulting_files/{self.filename}.json'):
            os.remove(f'resulting_files/{self.filename}.json')

    def test_create_new_files(self):
        #Call the function to create the JSON file
        create_new_files([self.quadrilateral_test_data], [self.filename])

        #Check if the file was created
        self.assertTrue(os.path.exists(f'resulting_files/{self.filename}.json'))

        #Read the contents of the file and check if it matches the test data
        with open(f'resulting_files/{self.filename}.json', 'r') as file:
            file_data = json.load(file)
            self.assertEqual(file_data, self.expected_result)


if __name__ == '__main__':
    unittest.main()