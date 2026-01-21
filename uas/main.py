import tkinter as tk
import math
from engine_3d import Engine3D, create_cube, create_grid, create_box, Vector3, adjust_color_brightness, Mesh

class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini Scene Edukatif - 3D Engine Python")
        self.width = 800
        self.height = 600
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="white")
        self.canvas.pack()

        # --- Engine ---inti mengatur 3d
        self.engine = Engine3D(self.width, self.height)

        # --- Scene ---
        self.objects = []
        self.room = Mesh("Bedroom")

        def add_to_room(mesh, offset_x, offset_y, offset_z):
            start_idx = len(self.room.vertices)
            for v in mesh.vertices:
                mx = v.x * mesh.scale.x + offset_x
                my = v.y * mesh.scale.y + offset_y
                mz = v.z * mesh.scale.z + offset_z
                self.room.add_vertex(mx, my, mz)

            for indices, color in mesh.faces:
                new_indices = tuple(i + start_idx for i in indices)
                self.room.add_face(new_indices, color)

        # ================= FLOOR =================
        floor = create_grid(10, 8)
        floor.scale = Vector3(62, 1, 62)
        add_to_room(floor, 0, -100, 0)

        # ================= COLORS =================
        c_wall_blue = "#448AFF"
        c_trim_blue = "#2962FF"
        c_wood      = "#FFAB91"
        c_sheet     = "#29B6F6"
        c_pillow    = "#81D4FA"
        c_white     = "#FFFFFF"
        c_black     = "#212121"

        # ================= WALLS =================
        wall_left = create_box(10, 400, 600, c_wall_blue)
        add_to_room(wall_left, -300, 100, 0)

        trim_top_l = create_box(40, 40, 640, c_trim_blue)
        add_to_room(trim_top_l, -300, 300, 0)

        trim_bot_l = create_box(40, 40, 640, c_trim_blue)
        add_to_room(trim_bot_l, -300, -90, 0)

        wall_right = create_box(600, 400, 10, c_wall_blue)
        add_to_room(wall_right, 0, 100, -300)

        trim_top_r = create_box(640, 40, 40, c_trim_blue)
        add_to_room(trim_top_r, 0, 300, -300)

        trim_bot_r = create_box(640, 40, 40, c_trim_blue)
        add_to_room(trim_bot_r, 0, -90, -300)

        # ================= BED =================
        bed_w, bed_h, bed_d = 180, 50, 220
        bed = create_box(bed_w, bed_h, bed_d, c_wood)
        add_to_room(bed, 100, -75, -100)

        mattress = create_box(bed_w-20, 20, bed_d-20, c_sheet)
        add_to_room(mattress, 100, -45, -100)

        p_w, p_h, p_d = 60, 15, 40
        pillow1 = create_box(p_w, p_h, p_d, c_pillow)
        add_to_room(pillow1, 60, -30, -170)

        pillow2 = create_box(p_w, p_h, p_d, c_pillow)
        add_to_room(pillow2, 140, -30, -170)

        headboard = create_box(bed_w, 80, 20, c_wood)
        add_to_room(headboard, 100, -60, -210)

        # ================= TV =================
        tv_cab = create_box(100, 60, 200, c_wood)
        add_to_room(tv_cab, -220, -70, 0)

        tv = create_box(20, 50, 80, c_black)
        add_to_room(tv, -220, -15, 0)

        # ================= DECOR =================
        window_frame = create_box(200, 150, 15, c_white)
        add_to_room(window_frame, -50, 150, -295)

        painting = create_box(15, 120, 200, c_white)
        add_to_room(painting, -290, 150, 50)

        door = create_box(100, 250, 10, c_white)
        add_to_room(door, 200, 25, -295)

        # ================= TRANSFORM =================
        self.room.position = Vector3(0, 50, 400)
        self.room.rotation = Vector3(0.5, 0.75, 0)
        self.room.scale = Vector3(1, 1, 1)

        self.objects.append(self.room)
        self.target_obj = self.room

        # ================= UI =================
        self.info_text = tk.Label(
            root,
            text="""
[KONTROL]
WASD   : Rotasi
Q/E    : Zoom
Arrows : Geser
R      : Refleksi

[MODE]
Solid Polygon Only
""",
            bg="white",
            fg="black",
            font=("Consolas", 10),
            justify="left"
        )
        self.info_text.place(x=10, y=10)

        root.bind("<Key>", self.handle_input)
        self.update()

    def handle_input(self, event):
        key = event.keysym.upper()

        if key == 'W': self.target_obj.rotation.x -= 0.1
        elif key == 'S': self.target_obj.rotation.x += 0.1
        elif key == 'A': self.target_obj.rotation.y -= 0.1
        elif key == 'D': self.target_obj.rotation.y += 0.1
#skala
        elif key == 'Q':
            self.target_obj.scale.x *= 1.1
            self.target_obj.scale.y *= 1.1
            self.target_obj.scale.z *= 1.1

        elif key == 'E':
            self.target_obj.scale.x *= 0.9
            self.target_obj.scale.y *= 0.9
            self.target_obj.scale.z *= 0.9

#translasi
        elif key == 'UP': self.target_obj.position.y += 10
        elif key == 'DOWN': self.target_obj.position.y -= 10
        elif key == 'LEFT': self.target_obj.position.x -= 10
        elif key == 'RIGHT': self.target_obj.position.x += 10
#miror
        elif key == 'R':
            self.target_obj.scale.x *= -1

    def update(self):
        self.canvas.delete("all")
        faces_to_draw = []

        for mesh in self.objects:
            transformed_verts = [
                self.engine.transform_vertex(v, mesh)
                for v in mesh.vertices
            ]

            for face_indices, color in mesh.faces:
                v1 = transformed_verts[face_indices[0]]
                v2 = transformed_verts[face_indices[1]]
                v3 = transformed_verts[face_indices[2]]

                normal = self.engine.calculate_normal(v1, v2, v3)

                if normal.z > 0:
                    intensity = self.engine.calculate_shade(normal, None)
                    final_color = adjust_color_brightness(color, intensity)

                    avg_z = (v1.z + v2.z + v3.z) / 3
                    faces_to_draw.append({
                        "z": avg_z,
                        "indices": face_indices,
                        "color": final_color,
                        "verts": transformed_verts
                    })

        faces_to_draw.sort(key=lambda f: f["z"], reverse=True)

        for face in faces_to_draw:
            points = []
            for idx in face["indices"]:
                v3d = face["verts"][idx]
                x, y = self.engine.project(v3d, True)
                points.extend([x, y])

            self.canvas.create_polygon(
                points,
                fill=face["color"],
                outline="black"
            )

        self.root.after(16, self.update)


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
