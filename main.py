from utils import read_in_json_file, create_new_files, plot_dry_and_wet_data
from quadrilateral_manipulation import split_up_quadrilateral_data


def main():

    #Read in the given json file
    quadrilateral_position_dict = read_in_json_file("given_information/simple_challange_data.json")

    #Split the given data in to dry (z > 0) and wet (z < 0) data 
    dry_quadrilateral_xyz_positions, wet_quadrilateral_xyz_positions = split_up_quadrilateral_data(quadrilateral_position_dict)

    #Create two new files identical in style to the original file read in
    create_new_files([dry_quadrilateral_xyz_positions, wet_quadrilateral_xyz_positions], ['dry_geometry', 'wet_geometry'])

    #Plot the two resulting data sets for visual confirmation of success
    plot_dry_and_wet_data([dry_quadrilateral_xyz_positions, wet_quadrilateral_xyz_positions], ['Dry Surface', 'Wet Surface'])


if __name__ == '__main__':

    main()
