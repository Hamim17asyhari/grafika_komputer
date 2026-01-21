import math

class Vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def to_tuple(self):
        return (self.x, self.y, self.z)

    def __repr__(self):
        return f"V({self.x:.2f}, {self.y:.2f}, {self.z:.2f})"

class Mesh:
    """
    Representasi Objek 3D (Point 1 Project)
    Menyimpan Vertices (Titik) dan Faces (Poligon).
    """
    def __init__(self, name="Object"):
        self.name = name
        self.vertices = [] # List of Vector3
        self.faces = []    # List of tuples (v_index1, v_index2, v_index3, color)
        self.position = Vector3(0, 0, 0)
        self.rotation = Vector3(0, 0, 0)
        self.scale = Vector3(1, 1, 1)

    def add_vertex(self, x, y, z):
        self.vertices.append(Vector3(x, y, z))

    def add_face(self, indices, color="white"):
        self.faces.append((indices, color))

class Engine3D:
    """
    Mesin Utama untuk menangani Transformasi dan Proyeksi
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Point 3: Viewing - Kamera 'virtual' ada di (0,0,0), layar ada di depan
        self.fov = 400  # Field of View scalar
        self.light_dir = Vector3(0, 0, -1) # Cahaya datang dari depan (Point 4: Cahaya)

    def rotate(self, coord, rotation):
        """
        Point 2: Transformasi Geometris (Rotasi)
        Menggunakan matriks rotasi standar untuk X, Y, Z.
        """
        rx, ry, rz = rotation.x, rotation.y, rotation.z
        x, y, z = coord.x, coord.y, coord.z

        # Rotasi Z
        nx = x * math.cos(rz) - y * math.sin(rz)
        ny = x * math.sin(rz) + y * math.cos(rz)
        x, y = nx, ny

        # Rotasi Y
        nx = x * math.cos(ry) + z * math.sin(ry)
        nz = -x * math.sin(ry) + z * math.cos(ry)
        x, z = nx, nz

        # Rotasi X
        ny = y * math.cos(rx) - z * math.sin(rx)
        nz = y * math.sin(rx) + z * math.cos(rx)
        y, z = ny, nz

        return Vector3(x, y, z)

    def transform_vertex(self, vertex, mesh):
        """
        Menggabungkan Scaling, Rotation, dan Translation
        """
        # 1. Scale
        x = vertex.x * mesh.scale.x
        y = vertex.y * mesh.scale.y
        z = vertex.z * mesh.scale.z
        
        # 2. Rotate
        rotated = self.rotate(Vector3(x, y, z), mesh.rotation)
        
        # 3. Translate (Pindah posisi objek global)
        final_x = rotated.x + mesh.position.x
        final_y = rotated.y + mesh.position.y
        final_z = rotated.z + mesh.position.z

        return Vector3(final_x, final_y, final_z)

    def calculate_normal(self, v1, v2, v3):
        # Hitung Normal Permukaan untuk Lighting (Point 4)
        # Vector A = v2 - v1
        ax, ay, az = v2.x - v1.x, v2.y - v1.y, v2.z - v1.z
        # Vector B = v3 - v1
        bx, by, bz = v3.x - v1.x, v3.y - v1.y, v3.z - v1.z
        
        # Cross Product
        nx = ay * bz - az * by
        ny = az * bx - ax * bz
        nz = ax * by - ay * bx
        
        # Normalize
        length = math.sqrt(nx*nx + ny*ny + nz*nz)
        if length == 0: return Vector3(0, 0, 0)
        return Vector3(nx/length, ny/length, nz/length)

    def project(self, vertex, perspective=True):
        """
        Point 3: Proyeksi 3D ke 2D
        """
        # Jika perspektif, bagi x dan y dengan z
        # Kita geser Z agar tidak divide by zero (z + kamera distance)
        factor = self.fov / (vertex.z + 4) if perspective else 50
        
        x = vertex.x * factor + self.width / 2
        y = -vertex.y * factor + self.height / 2 # Y positif ke atas di 3D, ke bawah di Canvas
        return (x, y)

    def calculate_shade(self, normal, base_color):
        """
        Point 4: Warna & Ilusi Kedalaman (Cahaya Dasar)
        Menghitung brightness berdasarkan sudut permukaan terhadap cahaya.
        """
        # Dot product normal dengan light_dir
        # Normal vector should be normalized. Light dir is (0,0,-1) usually for viewer-facing light.
        # Let's assume light comes from slightly top-left-front for better 3D effect: (-0.5, -0.5, -1)
        light = Vector3(-0.5, -1, -1)
        l_len = math.sqrt(light.x**2 + light.y**2 + light.z**2)
        lx, ly, lz = light.x/l_len, light.y/l_len, light.z/l_len
        
        dot = normal.x * lx + normal.y * ly + normal.z * lz
        
        # Ambil nilai positif 
        # Contrast Enhancement: 
        # 1. Increase Ambient light slightly (0.1 -> 0.3) to make colors pop
        # 2. Use a power curve to make highlights sharper
        intensity = max(0.3, dot * -1) 
        
        # Simple Tone Mapping for "Contrast"
        # intensity = pow(intensity, 0.8) 
        
        return intensity

def adjust_color_brightness(hex_color, factor):
    """
    Menggelapkan warna hex berdasarkan factor (0.0 - 1.0)
    """
    if not hex_color.startswith('#'): return hex_color # Fallback for 'red', 'blue' etc
    
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    
    r = int(r * factor)
    g = int(g * factor)
    b = int(b * factor)
    
    return f"#{r:02x}{g:02x}{b:02x}"


# Helper function to create standard shapes
def create_cube(size):
    cube = Mesh("Cube")
    s = size / 2
    # Define 8 Vertices
    # Depan
    cube.add_vertex(-s, -s, -s) # 0
    cube.add_vertex(s, -s, -s)  # 1
    cube.add_vertex(s, s, -s)   # 2
    cube.add_vertex(-s, s, -s)  # 3
    # Belakang
    cube.add_vertex(-s, -s, s)  # 4
    cube.add_vertex(s, -s, s)   # 5
    cube.add_vertex(s, s, s)    # 6
    cube.add_vertex(-s, s, s)   # 7

    # Define 6 Faces (Counter-Clockwise order is standard)
    # Front
    cube.add_face((0, 1, 2, 3), "#FF5733") # Orange
    # Back
    cube.add_face((5, 4, 7, 6), "#33FF57") # Green
    # Left
    cube.add_face((4, 0, 3, 7), "#3357FF") # Blue
    # Right
    cube.add_face((1, 5, 6, 2), "#F333FF") # Purple
    # Top
    cube.add_face((3, 2, 6, 7), "#FFFF33") # Yellow
    # Bottom
    cube.add_face((4, 5, 1, 0), "#33FFFF") # Cyan
    
    return cube

def create_grid(size, divisions):
    """
    Membuat grid lantai (Visualisasi Plane XZ)
    """
    grid = Mesh("Grid")
    step = size / divisions
    half = size / 2
    
    # Warna Gray
    color = "#444444"
    
    # Grid lines are actually just edges. But our engine renders FACES.
    # To render lines efficiently in this face-based engine is tricky without a specific line renderer.
    # We will make thin quads or just a large plane. 
    # Let's just make a large Chessboard Plane for simplicity and visual 'Scene' aspect.
    
    for i in range(divisions):
        for j in range(divisions):
            x = -half + i * step
            z = -half + j * step
            
            # 4 vertices for this cell
            idx = len(grid.vertices)
            grid.add_vertex(x, 0, z)          # 0
            grid.add_vertex(x + step, 0, z)   # 1
            grid.add_vertex(x + step, 0, z + step) # 2
            grid.add_vertex(x, 0, z + step)   # 3
            
            # Checker pattern (Wood Style)
            # Color A: Light Wood (#D7CCC8), Color B: Dark Wood (#8D6E63)
            c = "#D7CCC8" if (i+j)%2 == 0 else "#8D6E63"
            # Reverse winding to Point UP (0, 1, 0)
            grid.add_face((idx, idx+3, idx+2, idx+1), c)
            
    return grid

def create_box(width, height, depth, color):
    """
    Membuat Balok (Box) dengan dimensi tertentu dan warna tunggal
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

    # Faces (Counter-Clockwise)
    box.add_face((0, 1, 2, 3), color) # Front
    box.add_face((5, 4, 7, 6), color) # Back
    box.add_face((4, 0, 3, 7), color) # Left
    box.add_face((1, 5, 6, 2), color) # Right
    box.add_face((3, 2, 6, 7), color) # Top
    box.add_face((4, 5, 1, 0), color) # Bottom
    
    return box
