#Pieces are defined here
import numpy as np

PIECES = {
    #Squares
    "square_2": np.array([
        [1,1],
        [1,1]
    ]),
    "square_3": np.array([
        [1,1,1],
        [1,1,1],
        [1,1,1]
    ]),
    #Bars or line shapes
    "bar_2": np.array([
        [1,1]
    ]),
    "bar_3": np.array([
        [1,1,1]
    ]),
    "bar_4": np.array([
        [1,1,1,1]
    ]),
    "bare_5": np.array([
        [1,1,1,1,1]
    ]),
    "vertical_bar_2": np.array([
        [1],
        [1]
    ]),
    "vertical_bar_3": np.array([
        [1],
        [1],
        [1]
    ]),
    "vertical_bar_4": np.array([
        [1],
        [1],
        [1],
        [1]
    ]),
    "vertical_bar_5": np.array([
        [1],
        [1],
        [1],
        [1],
        [1]
    ]),
    #Regular L shapes
    "L_small": np.array([
        [1,0],
        [1,1]
    ]),
    "L_small_left": np.array([
        [1,1],
        [1,0]
    ]),
    "L_small_right": np.array([
        [0,1],
        [1,1]
    ]), 
    "L_small_upside_down": np.array([
        [1,1],
        [0,1]
    ]),
    "L_large": np.array([
        [1,0],
        [1,0],
        [1,1]
    ]),
    "L_large_left": np.array([
        [1,1],
        [1,0],
        [1,0]
    ]),
    "L_large_right": np.array([
        [0,1],
        [0,1],
        [1,1]
    ]),  
    "L_large_upside_down": np.array([
        [1,1],
        [0,1],
        [0,1]
    ]),
    "L_large_horizontal": np.array([
        [1,1,1],
        [1,0,0]
    ]),
    "L_large_horizontal_right": np.array([
        [1,1,1],
        [0,0,1]
    ]),
    #Long L shapes
    "L_long": np.array([
        [1,0,0,],
        [1,0,0],
        [1,1,1],
    ]),
    "L_long_left": np.array([
        [1,1,1],
        [1,0,0],
        [1,0,0],
    ]),
    "L_long_upside_down": np.array([
        [1,1,1],
        [0,0,1],
        [0,0,1],
    ]),
    "L_long_right": np.array([
        [0,0,1],
        [0,0,1],
        [1,1,1]
    ]),
    #T shapes
    "T_shape": np.array([
        [1,1,1],
        [0,1,0]
    ]), 
    "T_shape_left": np.array([
        [1,0],
        [1,1],
        [1,0]
    ]),
    "T_shape_right": np.array([
        [0,1],
        [1,1],
        [0,1]
    ]),
    "T_shape_upside_down": np.array([
        [0,1,0],
        [1,1,1]
    ]),
    #Z shapes
    "Z_shape": np.array([
        [1,1,0],
        [0,1,1]
    ]),
    "Z_shape_left": np.array([
        [0,1,1],
        [1,1,0]
    ]),
    "Z_shape_vertical": np.array([
        [1,0],
        [1,1],
        [0,1]
    ]),
    "Z_shape_vertical_flipped": np.array([
        [0,1],
        [1,1],
        [1,0]
    ]),
    #Diagonal shapes
    "diagonal_2": np.array([
        [1,0],
        [0,1]
    ]),
    "diagonal_2_flipped": np.array([
        [0,1],
        [1,0]
    ]),
    "diagonal_3": np.array([
        [1,0,0],
        [0,1,0],
        [0,0,1]
    ]),
    "diagonal_3_flipped": np.array([
        [0,0,1],
        [0,1,0],
        [1,0,0]
    ])
}