$fn = 48;

union() {
	translate(v = [0, 0, 0]) {
		rotate(a = 180, v = [100.0, 100.0, 141.4213562373095]) {
			cylinder(center = false, h = 141.4213562373095, r = 25.0000000000);
		}
	}
	translate(v = [100, 0, 0]) {
		rotate(a = 180, v = [0.0, 0.0, 100.0]) {
			cylinder(center = false, h = 50.0, r = 25.0000000000);
		}
	}
	translate(v = [100, 0, 50]) {
		rotate(a = 180, v = [-100.0, 100.0, 141.4213562373095]) {
			cylinder(center = false, h = 141.4213562373095, r = 25.0000000000);
		}
	}
	translate(v = [0, 100, 50]) {
		rotate(a = 180, v = [1, 0, 0]) {
			cylinder(center = false, h = 50.0, r = 25.0000000000);
		}
	}
}
/***********************************************
*********      SolidPython code:      **********
************************************************
 
"""Library with extensions for solidpython.

Author: Landon Carter (lcarter@mit.edu)
"""

import solid
import numpy as np


def cylinder_from_to(diameter, xyz1, xyz2):
    """Defines a cylinder of diameter from xyz1 to xyz2

    Args:
        diameter: The diameter of the cylinder (float)
        xyz1: The coordinates of the center of one face (list)
        xyz2: The coordinates of the center of the other face (list)

    Returns:
        A solid.cylinder which is the cylinder of diam d from xyz1 to xyz2.
    """
    length = np.linalg.norm(np.array(xyz2) - np.array(xyz1))
    axis_vec = np.array(xyz2) - np.array(xyz1)
    z_vec = np.array((0, 0, length))
    half_axis_vec = z_vec + axis_vec
    if np.linalg.norm(half_axis_vec) == 0:
        half_axis_vec = np.array([1, 0, 0])
    cyl = solid.translate(xyz1)(
        solid.rotate(180, list(half_axis_vec))(
            solid.cylinder(h=length, r=(diameter/2.), center=False)
        )
    )

    return cyl


a = cylinder_from_to(50, [0,0,0], [100,100,0])
b = cylinder_from_to(50, [100,0,0], [100,00,50])
c = cylinder_from_to(50, [100,0,50], [0,100,50])
d = cylinder_from_to(50, [0,100,50], [0,100,0])

everything = solid.union()([a, b, c, d])

solid.scad_render_to_file(everything, "out.scad", file_header='$fn = 48;') 
 
************************************************/
