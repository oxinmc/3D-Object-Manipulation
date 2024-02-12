# Project Name:
Challenge


## Author & Date:
Oxin McKittrick (07/02/24)


## Description:
The purpose of this code is to read in a two-key dictionary from a json file found at 'given_information/simple_challange_data.json', take the quadrilateral data within, split it into two categories, dry quadrilaterals (z > 0) and wet quadrilaterals (z < 0), then save these respective categories in the same format as the original data, and graph the 2 resulting datasets for confirmation of success. This code is run via 'main.py'.

Quadrilaterals where all corners are > 0 or < 0 are easy to categorise, the only complication comes when a portion of corners are located at both sides of the z = 0 line. Some assumptions were made, and tested to be true:
- For each quadrilateral, its list of coordinates are connected in the order provided, otherwise we will get a self-intersecting polygon.
- No z-coordinate has the value of z = 0.
Those quadrilaterals that exist across the z=0 plane are tackled via the functions in the 'quadrilateral_manipulation.py' file. These functions assess the number of points either side of the plane, to which a number of line equations will be concocted, then the intersection of these lines with the z=0 plane is calculated. These two intersection points (where z = 0) are appended to wet and dry data lists (with the points in the quadrilateral that have already been identified to these lists), successfully slicing the original quadrilateral into two new shapes along the z = 0 plane(potentially: triangle, quadrilateral, or pentagon).

The resulting dry and wet coordinate lists are then saved in the same format as the .json file they originate from, with a 'q' key in the dictionary dictating the coordinates of each corner in a given quadrilateral, and the 'p' key being a list of unique coordinates. These files are saved in the 'resulting_files' folder, under 'dry_geometry.json' and 'wet_geometry.json'.
In addition, two complimentary graphs are produced temporarily to visualise the work achieved.
Ignoring the printing of the graphs, this program was measured to have an execution time ~ 11 seconds.

This code also has a number of general purpose utility functions outlined in 'utils.py', for example, plotting and readin/writing json files. The two auxiliary function files ('quadrilateral_manipulation.py' & 'utils.py') have corresponding test files ('test_quadrilateral_manipulation.py' & 'test_utils.py') that were run as changes were implemented to the code to maintain confidence that the code was continuing to function without error.

[Note: Git was used for version control on this project.]


## File Structure (+ Explantion):
- Solution
    - given_information -> (info give with this project)
        - GIVEN_README.md
        - simple_challange_data.json
    - resulting_files -> (files created by the running of this program)
        - dry_geometry.json -> (all data with z > 0)
        - wet_geometry.json -> (all data with z < 0)
    - main.py -> (the main entry point in this project and the the central hub of the code)
    - README.md -> (Provides essential information about the project to users and other developers)
    - quadrilateral_manipulation.py -> (file dedicated to the functions for altering quadrilateral data as is necessary)
    - requirements.txt -> (specifies the dependencies required by the project)
    - test_quadrilateral_manipulation.py -> (file for testing the functions within quadrilateral_manipulation.py)
    - test_utils.py -> (file for testing the functions within utils.py)
    - utils.py -> (contains utility functions that may be used across the project)


## How to run:
This code can be executed from the 'main.py' file, and requires no user input outside of starting the program. Once in the correct directory, this can be done via the terminal with:
python .\main.py

After execution the program wil remain running as long as the plots are not closed.


## Installation:
Written on Python 3.9.1
Any required installations are outlined in the 'requirements.txt' file, and can be installed using:
pip install -r requirements.txt

