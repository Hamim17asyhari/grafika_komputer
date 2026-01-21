def create_box(width, height, depth, color):
    """
    Membuat Balok (Box) dengan dimensi tertentu
    """
    box = Mesh("Box")
    hw, hh, hd = width/2, height/2, depth/2 # Half Width, Height, Depth
    
    # Vertices
    # Front
    box.add_vertex(-hw, -hh, -hd) # 0
    box.add_vertex(hw, -hh, -hd)  # 1
    box.add_vertex(hw, hh, -hd)   # 2
    box.add_vertex(-hw, hh, -hd)  # 3
    # Back
    box.add_vertex(-hw, -hh, hd)  # 4
    box.add_vertex(hw, -hh, hd)   # 5
    box.add_vertex(hw, hh, hd)    # 6
    box.add_vertex(-hw, hh, hd)   # 7

    # Faces (Using the same color for all sides for simplicity, or slightly varied)
    # Using 'color' argument.
    box.add_face((0, 1, 2, 3), color) # Front
    box.add_face((5, 4, 7, 6), color) # Back
    box.add_face((4, 0, 3, 7), color) # Left
    box.add_face((1, 5, 6, 2), color) # Right
    box.add_face((3, 2, 6, 7), color) # Top
    box.add_face((4, 5, 1, 0), color) # Bottom
    
    return box
