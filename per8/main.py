import tkinter as tk
import math

class Transformer3D:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini Project Transformasi 3D")
        self.width = 800
        self.height = 600
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg="black")
        self.canvas.pack()

        # Konfigurasi Awal
        self.vertices = [
            [-50, -50, -50], [50, -50, -50], [50, 50, -50], [-50, 50, -50], # Depan
            [-50, -50, 50], [50, -50, 50], [50, 50, 50], [-50, 50, 50]      # Belakang
        ]
        self.edges = [
            (0,1), (1,2), (2,3), (3,0), # Sisi Depan
            (4,5), (5,6), (6,7), (7,4), # Sisi Belakang
            (0,4), (1,5), (2,6), (3,7)  # Penghubung
        ]
        
        # Simpan state asli untuk reset
        self.original_vertices = [v[:] for v in self.vertices]

        self.angle_x = 0
        self.angle_y = 0
        self.angle_z = 0
        self.scale_val = 1.0
        self.translate_x = 0
        self.translate_y = 0
        self.translate_z = 0
        self.is_reflected_x = False

        # Membuat Panel Kontrol
        self.create_controls()
        
        # Loop rendering
        self.draw()

    def create_controls(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        # Translasi
        tk.Label(control_frame, text="TRANSLASI (Geser):").grid(row=0, column=0, sticky="w")
        tk.Button(control_frame, text="← X", command=lambda: self.translate(-10, 0, 0)).grid(row=0, column=1)
        tk.Button(control_frame, text="X →", command=lambda: self.translate(10, 0, 0)).grid(row=0, column=2)
        tk.Button(control_frame, text="↑ Y", command=lambda: self.translate(0, -10, 0)).grid(row=0, column=3)
        tk.Button(control_frame, text="Y ↓", command=lambda: self.translate(0, 10, 0)).grid(row=0, column=4)

        # Rotasi
        tk.Label(control_frame, text="ROTASI (Putar):").grid(row=1, column=0, sticky="w")
        tk.Button(control_frame, text="Rot X", command=lambda: self.rotate('x')).grid(row=1, column=1)
        tk.Button(control_frame, text="Rot Y", command=lambda: self.rotate('y')).grid(row=1, column=2)
        tk.Button(control_frame, text="Rot Z", command=lambda: self.rotate('z')).grid(row=1, column=3)

        # Skala
        tk.Label(control_frame, text="SKALA (Ukuran):").grid(row=2, column=0, sticky="w")
        tk.Button(control_frame, text="Perbesar (+)", command=lambda: self.scale(1.1)).grid(row=2, column=1)
        tk.Button(control_frame, text="Perkecil (-)", command=lambda: self.scale(0.9)).grid(row=2, column=2)

        # Refleksi
        tk.Label(control_frame, text="REFLEKSI (Cermin):").grid(row=3, column=0, sticky="w")
        tk.Button(control_frame, text="Refleksi X", command=self.reflect_x).grid(row=3, column=1)

        # Reset
        tk.Button(control_frame, text="RESET", command=self.reset, bg="red", fg="white").grid(row=0, column=6, rowspan=4, padx=20)


    def translate(self, dx, dy, dz):
        self.translate_x += dx
        self.translate_y += dy
        self.translate_z += dz
        self.draw()

    def rotate(self, axis):
        if axis == 'x': self.angle_x += 0.1
        elif axis == 'y': self.angle_y += 0.1
        elif axis == 'z': self.angle_z += 0.1
        self.draw()

    def scale(self, factor):
        self.scale_val *= factor
        self.draw()

    def reflect_x(self):
        self.is_reflected_x = not self.is_reflected_x
        self.draw()

    def reset(self):
        self.angle_x = 0
        self.angle_y = 0
        self.angle_z = 0
        self.scale_val = 1.0
        self.translate_x = 0
        self.translate_y = 0
        self.translate_z = 0
        self.is_reflected_x = False
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        
        # Titik tengah canvas
        cx, cy = self.width / 2, self.height / 2

        # Transformasi vertices
        transformed_vertices = []
        for v in self.vertices:
            x, y, z = v[0], v[1], v[2]

            # 1. Refleksi (jika aktif)
            if self.is_reflected_x:
                x = -x

            # 2. Skala
            x *= self.scale_val
            y *= self.scale_val
            z *= self.scale_val

            # 3. Rotasi X
            rotate_x = self.angle_x
            y_new = y * math.cos(rotate_x) - z * math.sin(rotate_x)
            z_new = y * math.sin(rotate_x) + z * math.cos(rotate_x)
            y, z = y_new, z_new

            # 3. Rotasi Y
            rotate_y = self.angle_y
            x_new = x * math.cos(rotate_y) + z * math.sin(rotate_y)
            z_new = -x * math.sin(rotate_y) + z * math.cos(rotate_y)
            x, z = x_new, z_new

            # 3. Rotasi Z
            rotate_z = self.angle_z
            x_new = x * math.cos(rotate_z) - y * math.sin(rotate_z)
            y_new = x * math.sin(rotate_z) + y * math.cos(rotate_z)
            x, y = x_new, y_new

            # 4. Translasi
            x += self.translate_x
            y += self.translate_y
            z += self.translate_z

            # Proyeksi ke 2D (Perspective Projection sederhana)
            # Menambahkan offset Z agar objek tidak menghilang saat z < 0
            # tapi untuk simplifikasi, saya gunakan proyeksi ortografis + translasi pusat
            # Agar terlihat 3D, kita gunakan sedikit efek perspektif
            
            # Simulasi perspektif sederhana
            depth = 400
            factor = depth / (depth + z + 200) # +200 untuk mendorong objek menjauh dari 'kamera'
            
            screen_x = cx + x 
            screen_y = cy + y 
            
            # Opsional: Gunakan factor untuk efek perspektif yang lebih kuat
            # screen_x = cx + x * factor
            # screen_y = cy + y * factor

            transformed_vertices.append((screen_x, screen_y))

        # Gambar Edges
        for edge in self.edges:
            p1 = transformed_vertices[edge[0]]
            p2 = transformed_vertices[edge[1]]
            self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill="cyan", width=2)

        # Gambar Label Sumbu (opsional, untuk referensi)
        self.canvas.create_text(50, 20, text="Gunakan Tombol di Bawah", fill="white", anchor="w")
        status = f"Scale: {self.scale_val:.2f} |  Reflect X: {'ON' if self.is_reflected_x else 'OFF'}"
        self.canvas.create_text(50, 40, text=status, fill="yellow", anchor="w")

if __name__ == "__main__":
    root = tk.Tk()
    app = Transformer3D(root)
    root.mainloop()
