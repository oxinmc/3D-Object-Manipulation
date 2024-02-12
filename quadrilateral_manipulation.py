from utils import next_and_previous_index
from sympy import Plane, Line3D, Point3D


def arrange_coordinate_lists(quad_xyz_coordinates, quad_z_coordinates, negative_number_count):

    """
    Receives 3D positional data for a quadrilateral that is positioned on both sides of the z=0 plane, i.e. at least one z
    coordinate is < 0. This quadrilateral is then arranged based on how many 'z' values it contains < 0, so that all coordinate
    lists get equal treatment. For example, if 'negative_number_count' == 1, all values in 'quad_xyz_coordinates' are moved along
    (like in a conveyor belt) so that the negative value has an index of 0.
    This is all so that when the z=0 intersection points are calculated, these points will be appended to the correct position in
    the list of dry & wet quadrilaterals, as corner positions in the list are important when defining the shape of a quadrilateral.

    Args:
        quad_xyz_coordinates (list): The four corner positions in 3D for the quadrilateral e.g. [[-3.08, 0.0, -0.23], [-3.02, 0.0, 0.14], [-2.97, 0.52, 0.13], [-3.04, 0.52, -0.24]]
        quad_z_coordinates (list): The four 'z' position coordinates of the quadrilateral e.g. [-0.23, 0.14, 0.13, -0.24]
        negative_number_count (int): A count of the number of negative 'z' position coordinates.

    Returns:
        quad_xyz_coordinates (list): The same argument given to this function, but ordered relative to the number of negative values present in this list.
        quad_z_coordinates (list): The same argument given to this function, but ordered relative to the number of negative values present in this list.
        negative_number_positions (list): A list of integers, corresponding to the index of negative numbers in quad_z_coordinates.
        positive_number_positions (list): A list of integers, corresponding to the index of positive numbers in quad_z_coordinates.

    Raises:
        None
        ** None needed as argument checks are conducted in function 'sort_mixed_quadrilaterals', which calls this function.
            (If, hypothetically, this function was more openly called from other locations, then it may become neccessary to check args)
    """

    negative_number_positions = [e for e,i in enumerate(quad_z_coordinates) if i < 0] #Find negative number indexes

    if negative_number_count == 1: #Only one negative z value

        index = negative_number_positions[0]
        if index != 0: #If the one negative value's index isn't zero, move list sideways so that it is
            quad_xyz_coordinates = [quad_xyz_coordinates[index]] + quad_xyz_coordinates[index+1:] + quad_xyz_coordinates[:index] #Shift numbers over in list so negative value always comes first
            quad_z_coordinates = [quad_z_coordinates[index]] + quad_z_coordinates[index+1:] + quad_z_coordinates[:index] #Shift numbers over in list so negative value always comes first
            negative_number_positions = [e for e,i in enumerate(quad_z_coordinates) if i < 0]
        positive_number_positions = [i for i in [0,1,2,3] if i not in negative_number_positions]
    
    elif negative_number_count == 3: #Three negative z value, e.g. one positive value

        positive_number_positions = [i for i in [0,1,2,3] if i not in negative_number_positions]
        index = positive_number_positions[0]
        if index != 0: #If the one positive value's index isn't zero, move list sideways so that it is
            quad_xyz_coordinates = [quad_xyz_coordinates[index]] + quad_xyz_coordinates[index+1:] + quad_xyz_coordinates[:index] #Shift numbers over in list so negative value always comes first
            quad_z_coordinates = [quad_z_coordinates[index]] + quad_z_coordinates[index+1:] + quad_z_coordinates[:index] #Shift numbers over in list so negative value always comes first
            negative_number_positions = [e for e,i in enumerate(quad_z_coordinates) if i < 0]
            positive_number_positions = [i for i in [0,1,2,3] if i not in negative_number_positions]

    else: #Two negative z-values
        # positive_number_positions is returned in reverse order
        positive_number_positions = [i for i in [3,2,1,0] if i not in negative_number_positions]


    return(quad_xyz_coordinates, quad_z_coordinates, negative_number_positions, positive_number_positions)


def sort_mixed_quadrilaterals(quad_xyz_coordinates, quad_z_coordinates, negative_number_count):

    """
    Receives 3D positional data for a quadrilateral that is positioned on both sides of the z=0 plane. The quadrilateral is then
    sliced along this plane, returning two lists of positional data, one for the z > 0 points (dry) and one for the z < 0 points
    (wet). This is achieved by first identifying how many of the quadrilaterals points lie under the z=0 plane, depending on the
    number, a number of line equations will be concocted, and then from this the intersection of these lines and the z=0 plane is 
    calculated. These two intersection points are then appended to wet and dry data lists (with the points already identified to 
    these lists), successfully slicing the original quadrilateral into two new shapes (triangle, quadrilateral, or pentagon).

    Args:
        quad_xyz_coordinates (list): The four corner positions in 3D for the quadrilateral e.g. [[-3.08, 0.0, -0.23], [-3.02, 0.0, 0.14], [-2.97, 0.52, 0.13], [-3.04, 0.52, -0.24]]
        quad_z_coordinates (list): The four 'z' position coordinates of the quadrilateral e.g. [-0.23, 0.14, 0.13, -0.24]
        negative_number_count (int): A count of the number of negative 'z' position coordinates.

    Returns:
        dry_component (list):
        wet_component (list):

    Raises:
        TypeError: If 'quad_xyz_coordinates' is not a list.
        TypeError: If 'quad_z_coordinates' is not a list.
        TypeError: If 'negative_number_count' is not an integer.
        TypeError: If 'quad_z_coordinates' is not a list.
        TypeError: If 'quad_xyz_coordinates[0][0]' is not an int or float.
        TypeError: If 'quad_z_coordinates[0]' is not an int or float.
    """

    if not isinstance(quad_xyz_coordinates, (list)):
        raise TypeError("'quad_xyz_coordinates' argument must be a list")
    elif not isinstance(quad_z_coordinates, (list)):
        raise TypeError("'quad_z_coordinates' argument must be a list")
    elif not isinstance(negative_number_count, (int)):
        raise TypeError("'negative_number_count' argument must be an int")
    
    if not isinstance(quad_xyz_coordinates[0][0], (int, float)):
        raise TypeError("'quad_xyz_coordinates' argument must be a list")
    elif not isinstance(quad_z_coordinates[0], (int, float)):
        raise TypeError("'quad_z_coordinates' argument must be a list")

    Z_PLANE_CONST = Plane(Point3D(-100,-100,0), Point3D(-100,100,0), Point3D(100,100,0)) #Define large z=0 plane as constant for calculating intersections
    quad_xyz_coordinates, quad_z_coordinates, negative_number_positions, positive_number_positions = arrange_coordinate_lists(quad_xyz_coordinates, quad_z_coordinates, negative_number_count)

    if negative_number_count == 1: #Only one negative point -> Negative: z_coord[index]

        #Find coordinates lying either side of z=0 plane (2 positive + 1 negative)
        index = negative_number_positions[0]
        next_index = positive_number_positions[2]
        prev_index = positive_number_positions[0]

        wet_component = [quad_xyz_coordinates[index]]
        dry_component = [quad_xyz_coordinates[index] for index in positive_number_positions]

        point_1 = Point3D(quad_xyz_coordinates[index][0], quad_xyz_coordinates[index][1], quad_xyz_coordinates[index][2]) #Negative point
        point_2 = Point3D(quad_xyz_coordinates[next_index][0], quad_xyz_coordinates[next_index][1], quad_xyz_coordinates[next_index][2])
        point_3 = Point3D(quad_xyz_coordinates[prev_index][0], quad_xyz_coordinates[prev_index][1], quad_xyz_coordinates[prev_index][2])
        line_1, line_2 = Line3D(point_1, point_2), Line3D(point_1, point_3)


    elif negative_number_count == 2:

        #Find coordinates lying either side of z=0 plane (2 positive + 2 negative)
        index_1 = negative_number_positions[0]
        index_2 = negative_number_positions[1]
        next_index_1, prev_index_1 = next_and_previous_index(index_1, (len(quad_z_coordinates)-1))
        next_index_2, prev_index_2 = next_and_previous_index(index_2, (len(quad_z_coordinates)-1))

        dry_component = [quad_xyz_coordinates[index] for index in positive_number_positions]

        point_1 = Point3D(quad_xyz_coordinates[index_1][0], quad_xyz_coordinates[index_1][1], quad_xyz_coordinates[index_1][2]) #Negative point 1
        point_2 = Point3D(quad_xyz_coordinates[index_2][0], quad_xyz_coordinates[index_2][1], quad_xyz_coordinates[index_2][2]) #Negative point 2

        if index_2 == (index_1+1): #Two negative points, one after the other (index_2 after index_1), e.g. index: 0,1 or 1,2 or 2,3

            wet_component = [quad_xyz_coordinates[index_2], quad_xyz_coordinates[index_1]]

            point_3 = Point3D(quad_xyz_coordinates[prev_index_1][0], quad_xyz_coordinates[prev_index_1][1], quad_xyz_coordinates[prev_index_1][2]) #Positive point 1
            point_4 = Point3D(quad_xyz_coordinates[next_index_2][0], quad_xyz_coordinates[next_index_2][1], quad_xyz_coordinates[next_index_2][2]) #Positive point 2
            line_1, line_2 = Line3D(point_1, point_3), Line3D(point_2, point_4)

        else: #Two negative points, wraparound, e.g. index: 0,3

            wet_component = [quad_xyz_coordinates[index_2], quad_xyz_coordinates[index_1]]

            point_3 = Point3D(quad_xyz_coordinates[next_index_1][0], quad_xyz_coordinates[next_index_1][1], quad_xyz_coordinates[next_index_1][2]) #Positive point 1
            point_4 = Point3D(quad_xyz_coordinates[prev_index_2][0], quad_xyz_coordinates[prev_index_2][1], quad_xyz_coordinates[prev_index_2][2]) #Positive point 2
            line_1, line_2 = Line3D(point_1, point_3), Line3D(point_2, point_4)
        

    else: # 3 negative points

        #Find coordinates lying either side of z=0 plane (1 positive + 2 negative)
        index = positive_number_positions[0]
        next_index = negative_number_positions[2]
        prev_index = negative_number_positions[0]
        
        dry_component = [quad_xyz_coordinates[index]]
        wet_component = [quad_xyz_coordinates[index] for index in negative_number_positions]

        point_1 = Point3D(quad_xyz_coordinates[index][0], quad_xyz_coordinates[index][1], quad_xyz_coordinates[index][2]) #Negative point
        point_2 = Point3D(quad_xyz_coordinates[next_index][0], quad_xyz_coordinates[next_index][1], quad_xyz_coordinates[next_index][2])
        point_3 = Point3D(quad_xyz_coordinates[prev_index][0], quad_xyz_coordinates[prev_index][1], quad_xyz_coordinates[prev_index][2])
        line_1, line_2 = Line3D(point_1, point_2), Line3D(point_1, point_3)

    '''
    Each orientation where a quadrilateral crosses the z=0 plane, creates two equations of a line between neighbouring dry and wet
    points, so to split these quadrilaterals into dry and wet sections, we need to find where these lines intersect the z=0 plane.
    These intersection coordinates are then appended to the dry and wet lists as their border points.
    '''
    for line in [line_1, line_2]:

        intersection = Z_PLANE_CONST.intersection(line)
        x_coord = float(intersection[0][0])
        y_coord = float(intersection[0][1])

        dry_component.append([x_coord, y_coord, 0])
        wet_component.append([x_coord, y_coord, 0])

    return(dry_component, wet_component)



def split_up_quadrilateral_data(quadrilateral_position_dict):
    
    """
    Given a dictionary, with keys 'q' (list of quadrilaterals) and 'p' (list of points in 3D space), map all corner positions to
    each quadrilateral and filter into 3 buckets:
    -   All positional z-components are > 0: Append to list of dry quadrilaterals.
    -   All positional z-components are < 0: Append to list of wet quadrilaterals.
    -   The z-components are a mix of > 0 and < 0: Send to 'sort_mixed_quadrilaterals' function to split quadrilateral into 
        positive and negative components, and then append resulting components to corresponding list.

    Args:
        quadrilateral_position_dict (dict): The given json file, theprimary source of all data.

    Returns:
        dry_quadrilateral_xyz_positions (list): All 3D coordinates for the 2D shapes existing above the z=0 plane.
        wet_quadrilateral_xyz_positions (list): All 3D coordinates for the 2D shapes existing below the z=0 plane.

    Raises:
        TypeError: If 'filename' is not a string
        KeyError: If 'p' or 'q' does not exist in 'quadrilateral_position_dict'
    """

    if not isinstance(quadrilateral_position_dict, (dict)):
        raise TypeError("'quadrilateral_position_dict' argument must be a dict")
    
    try:
        test = quadrilateral_position_dict['q']  #See if key exists
    except KeyError:
        raise KeyError("The key 'q' does not exist in the dictionary 'quadrilateral_position_dict'")
    try:
        test = quadrilateral_position_dict['p']  #See if key exists
    except KeyError:
        raise KeyError("The key 'p' does not exist in the dictionary 'quadrilateral_position_dict'")

    p_data = quadrilateral_position_dict['p']
    q_data = quadrilateral_position_dict['q']

    dry_quadrilateral_xyz_positions = []
    wet_quadrilateral_xyz_positions = []

    for quad_ints in q_data:

        quad_xyz_coordinates = [p_data[int(quad_ints[0])], p_data[int(quad_ints[1])], p_data[int(quad_ints[2])], p_data[int(quad_ints[3])]]
        quad_z_coordinates = [float(p_data[int(quad_ints[0])][2]), float(p_data[int(quad_ints[1])][2]), float(p_data[int(quad_ints[2])][2]), float(p_data[int(quad_ints[3])][2])]

        if all(i > 0 for i in quad_z_coordinates): #All Z positions are positive: dry quadrilateral
            dry_quadrilateral_xyz_positions.append(quad_xyz_coordinates)
        elif all(i < 0 for i in quad_z_coordinates): #All Z positions are positive: dry quadrilateral
            wet_quadrilateral_xyz_positions.append(quad_xyz_coordinates)
        else: #Z positions are a mix of positive and negative: dry/wet quadrilateral
            negative_number_count = sum(1 for i in quad_z_coordinates if i < 0)
            
            dry_component, wet_component = sort_mixed_quadrilaterals(quad_xyz_coordinates, quad_z_coordinates, negative_number_count)
            dry_quadrilateral_xyz_positions.append(dry_component)
            wet_quadrilateral_xyz_positions.append(wet_component)

    return (dry_quadrilateral_xyz_positions, wet_quadrilateral_xyz_positions)

