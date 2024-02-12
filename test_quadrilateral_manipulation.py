import unittest
from quadrilateral_manipulation import split_up_quadrilateral_data, sort_mixed_quadrilaterals, arrange_coordinate_lists



class TestQuadrilateralManipulation(unittest.TestCase):

    def setUp(self):
        #Set up preconditions for the test
        self.quadrilateral_test_dict = {"q": [[0, 1, 2, 3], [0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]], 
                                        "p": [[-3.0, 0.0, 0.1], [-2.9, 0.0, 0.5], [-2.9, 0.5, 0.5], [-2.9, 0.5, 0.1], [-2.8, -0.5, 0.0],
                                            [-2.8, 0.0, -0.5], [-2.5, 0.0, 0.0], [-2.5, 0.5, 0.0], [-2.0, -2.5, 0.0], [-2.0, 0.0, -2.5], 
                                            [-2.0, 0.0, 0.0], [-2.0, 0.5, 0.5], [0.0, -2.9, -0.1], [0.1, -2.9, -0.5], [0.5, -2.9, -0.5], [0.5, -2.9, -0.1]
                                            ]
                                        }
        
        self.quadrilateral_test_data = [[-3.0, 0.0, 0.1], [-2.9, 0.0, 0.5], [-2.9, 0.5, 0.5], [-2.9, 0.5, -0.1]]
        self.quadrilateral_z_test_data = [0.1, 0.5, 0.5, -0.1]
        self.negative_number_count = sum(1 for i in self.quadrilateral_z_test_data if i < 0)
    
    #Test case for arrange_coordinate_lists
    def test_arrange_coordinate_lists(self):
        # return quad_xyz_coordinates, quad_z_coordinates, negative_number_positions, positive_number_positions
        self.assertEqual(arrange_coordinate_lists(self.quadrilateral_test_data, self.quadrilateral_z_test_data, self.negative_number_count),
                         ([[-2.9, 0.5, -0.1], [-3.0, 0.0, 0.1], [-2.9, 0.0, 0.5], [-2.9, 0.5, 0.5]], [-0.1, 0.1, 0.5, 0.5], [0], [1,2,3]))
    
    #Test case for sort_mixed_quadrilaterals
    def test_sort_mixed_quadrilaterals(self):
        self.assertEqual(sort_mixed_quadrilaterals(self.quadrilateral_test_data, self.quadrilateral_z_test_data, self.negative_number_count),
                         ([[-3.0, 0.0, 0.1], [-2.9, 0.0, 0.5], [-2.9, 0.5, 0.5], [-2.9, 0.5, 0], [-2.95, 0.25, 0]], 
                          [[-2.9, 0.5, -0.1], [-2.9, 0.5, 0], [-2.95, 0.25, 0]]))

    #Test case for split_up_quadrilateral_data
    def test_split_up_quadrilateral_data(self):
        self.assertEqual(split_up_quadrilateral_data(self.quadrilateral_test_dict),
                         ([[[-3.0, 0.0, 0.1], [-2.9, 0.0, 0.5], [-2.9, 0.5, 0.5], [-2.9, 0.5, 0.1]], [[-3.0, 0.0, 0.1], [-2.9, 0.0, 0.5], [-2.9, 0.5, 0.5], [-2.9, 0.5, 0.1]],
                           [[-2.5, 0.0, 0.0], [-2.5, 0.5, 0.0], [-2.8, -0.5, 0.0], [-2.8, -0.5, 0], [-2.5, 0.0, 0]], [[-2.0, 0.0, 0.0], [-2.0, 0.5, 0.5], [-2.0, -2.5, 0.0], [-2.0, -2.5, 0], [-2.0, 0.0, 0]]],
                           [[[-2.8, 0.0, -0.5], [-2.8, -0.5, 0], [-2.5, 0.0, 0]], [[-2.0, 0.0, -2.5], [-2.0, -2.5, 0], [-2.0, 0.0, 0]], [[0.0, -2.9, -0.1], [0.1, -2.9, -0.5], [0.5, -2.9, -0.5], [0.5, -2.9, -0.1]]]))


if __name__ == '__main__':
    unittest.main()