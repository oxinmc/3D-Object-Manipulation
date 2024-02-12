import json
import os
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt



def read_in_json_file(filename):

    """
    Read the contents of a json file in as an object

    Args:
        filename (str): The name of the file to be read in.

    Returns:
        quadrilateral_position_dict(dict): The contents of the json file in a dictionary object.

    Raises:
        TypeError: If 'filename' is not a string
    """

    if not isinstance(filename, (str)):
        raise TypeError("'filename' argument must be a string")

    with open(filename, "r", encoding="utf-8") as f:
        quadrilateral_position_dict = json.loads(f.read())

    return(quadrilateral_position_dict)


def save_json_file(filename, quadrilateral_dict_for_saving):

    """
    Save a dict object in a json file

    Args:
        filename (str): The name of the file to be saved.
        quadrilateral_dict_for_saving (dict): The dictionary object to be saved.

    Returns:
        None

    Raises:
        TypeError: If 'filename' is not a string
        TypeError: If 'quadrilateral_dict_for_saving' is not a dict
    """
    
    if not isinstance(filename, (str)):
        raise TypeError("'filename' argument must be a string")
    elif not isinstance(quadrilateral_dict_for_saving, (dict)):
        raise TypeError("'quadrilateral_dict_for_saving' argument must be a dict")

    if not os.path.exists('resulting_files'):
        os.makedirs('resulting_files')
    
    with open(f'resulting_files/{filename}.json', 'w') as f:
        json.dump(quadrilateral_dict_for_saving, f)


def next_and_previous_index(index, max_index):

    """
    Given an index find the previous, and next index. Includes wraparound, e.g. if len(list) = 4,
    and index == 3, next index will equal 0

    Args:
        index (int): A given index in a list.
        max_index (int): The maximum index value of that list.

    Returns:
        next_index (int): The index value of the next object in a list.
        prev_index (int): The index value of the previous object in a list.

    Raises:
        TypeError: If either 'index' or 'max_index' is not an integer.
    """

    if not isinstance(index, (int)):
        raise TypeError("'index' argument must be a string")
    elif not isinstance(max_index, (int)):
        raise TypeError("'max_index' argument must be a string")

    #Deals with wraparound
    if index == max_index: #len(quad_xyz_coordinates) will always be 4, so max index is 3
        next_index = 0
        prev_index = index - 1
    else:
        next_index = index + 1
        prev_index = index - 1

    return(next_index, prev_index)


def create_new_files(data_objects_for_saving, data_object_filenames):

    """
    Takes a list of lists (+ associated filename) and creates a dict object, which is then saved to a json file.
    This function can take any number of lists for saving, as long as it comes with an associated name.

    Args:
        data_objects_for_saving (list): A list of lists, where every list within takes the shape of - [[-3.0, 0.0, 0.1], [-2.9, 0.0, 0.5], [-2.9, 0.5, 0.5], [-2.9, 0.5, 0.1]].
        data_object_filenames (list): The name to be given to the file saved from each list given.

    Returns:
        None

    Raises:
        TypeError: If either 'data_objects_for_saving' or 'data_object_filenames' is not a list.
        TypeError: If 'data_objects_for_saving[0][0]' is not a list.
        TypeError: If 'data_object_filenames[0]' is not a string.
    """

    if not isinstance(data_objects_for_saving, (list)):
        raise TypeError("'data_objects_for_saving' argument must be a list")
    elif not isinstance(data_object_filenames, (list)):
        raise TypeError("'data_object_filenames' argument must be a list")

    for data_set,filename in zip(data_objects_for_saving, data_object_filenames):

        if not isinstance(data_set[0], (list)):
            raise TypeError("'data_objects_for_saving' must contain a list of lists")
        elif not isinstance(filename, (str)):
            raise TypeError("'data_object_filenames' list must only contain strings")

        q_for_dict = []
        p_for_dict = []
        position_identifier = {} #For assigning the position of p lists to q dict

        for quadrilateral in data_set: #[[-3.0, 0.0, 0.1], [-2.9, 0.0, 0.5], [-2.9, 0.5, 0.5], [-2.9, 0.5, 0.1]]
            q_position = []
            for point in quadrilateral: #[-3.0, 0.0, 0.1]

                if point not in p_for_dict:

                    position_identifier[str(point)] = len(p_for_dict) #This is run before appending, so that position starts at 0
                    p_for_dict.append(point)

                q_position.append(position_identifier[str(point)])

            q_for_dict.append(q_position)

        quadrilateral_dict_for_saving = {'q':q_for_dict, 'p':p_for_dict}
        save_json_file(filename, quadrilateral_dict_for_saving)


def plot_dry_and_wet_data(quadrilateral_xyz_positions, figure_suptitle):

    #Test assumption: The vertices are connected in the order provided. Otherwise, we will get a self-intersecting polygon.

    """
    Plots two lists of 3D data on seperate figures.

    Args:
        quadrilateral_xyz_positions is a list containing two lists:
            dry_quadrilateral_xyz_positions (list), wet_quadrilateral_xyz_positions (list): 
                Both of these are lists, of lists, where the embedded list contains another four lists, ech with three float numbers, 
                representing the 4 corners of a quadrilateral, e.g. [[[1,2,3], [1,2,3], [1,2,3], [1,2,3]], [...], [...], ...].
                **  As some of the original quadrilaterals get slices, it is not uncommon that some of these inner lists may contain
                    as loas as three or as high as 5 corner positions (no longer technically quadrilaterals)
        figure_suptitle (list): List containing strings corresponding to the plots for each dataset.

    Returns:
        None

    Raises:
        TypeError: If either 'quadrilateral_xyz_positions' is not a list, or does not contain lists.
        TypeError: If either 'figure_suptitle' is not a list, or does not contain strings.
    """

    if not isinstance(quadrilateral_xyz_positions, (list)):
        raise TypeError("'quadrilateral_xyz_positions' argument must be a list")
    elif not isinstance(figure_suptitle, (list)):
        raise TypeError("'figure_suptitle' argument must be a list")

    axis_limits = 8
    colours = ['red', 'blue']

    for position_data, suptitle, colour in zip(quadrilateral_xyz_positions, figure_suptitle, colours):
        
        if not isinstance(position_data, (list)):
            raise TypeError("'quadrilateral_xyz_positions' argument must contain lists")
        elif not isinstance(suptitle, (str)):
            raise TypeError("'figure_suptitle' argument must contain strings")

        fig = plt.figure()
        fig.suptitle(suptitle)
        ax = fig.add_subplot(projection='3d')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.add_collection3d(Poly3DCollection(position_data, facecolor=colour)) # list of position data
        ax.set_ylim3d(-axis_limits, axis_limits)
        ax.set_xlim3d(-axis_limits, axis_limits)
        ax.set_zlim3d(-axis_limits, axis_limits)

    plt.show()

    

