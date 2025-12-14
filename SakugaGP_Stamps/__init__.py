bl_info = {
    "name" : "SakugaGP - Stamps",
    "author" : "Sadewoo (Spikysaurus)", 
    "description" : "Camera and Text Stamps for Grease Pencil",
    "blender" : (5, 0, 0),
    "version" : (0, 0, 0),
    "location" : "",
    "warning" : "",
    "doc_url": "https://spikysaurus.github.io/", 
    "tracker_url": "", 
    "category" : "Animation" 
}

import bpy
import bpy,math
from mathutils import Vector,Matrix

# --- PROPERTIES ---
class FunctionRunnerSettings(bpy.types.PropertyGroup):
    text_input: bpy.props.StringProperty(
        name="Input Text",
        description="",
        default=""
    )


# --- OPERATORS ---
class CameraStampOperator(bpy.types.Operator):
    bl_idname = "wm.camera_stamp"
    bl_label = "Camera Stamp"

    def execute(self, context):
        draw_camera_rectangle_gp5(stroke_radius=0.003)
        return {'FINISHED'}


class TextStampOperator(bpy.types.Operator):
    bl_idname = "wm.text_stamp"
    bl_label = "Text Stamp"

    def execute(self, context):
        custom_text = context.scene.function_runner_settings.text_input
        if custom_text == "": pass
        else:
            draw_auto_text(custom_text, spacing=1.5, stroke_radius=0.1,rotation_deg=90)
        return {'FINISHED'}


class RunTestOperator(bpy.types.Operator):
    bl_idname = "wm.run_test"
    bl_label = "Run Test"

    def execute(self, context):
#        run_test(context)
        return {'FINISHED'}


# --- PANEL ---
class FunctionRunnerPanel(bpy.types.Panel):
    bl_label = "Stamps"
    bl_idname = "VIEW3D_PT_function_runner"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SakugaGP'

    def draw(self, context):
        layout = self.layout
        settings = context.scene.function_runner_settings

        # Box with text input + second button
        col = layout.column(align=True)
        col.prop(settings, "text_input", text="Text")
        col.operator(TextStampOperator.bl_idname, text="Text Stamp")
        # Camera Stamp button
        col.operator(CameraStampOperator.bl_idname, text="Camera Stamp")

# --- REGISTER ---
classes = (
    FunctionRunnerSettings,
    CameraStampOperator,
    TextStampOperator,
    RunTestOperator,
    FunctionRunnerPanel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.function_runner_settings = bpy.props.PointerProperty(type=FunctionRunnerSettings)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.function_runner_settings

if __name__ == "__main__":
    register()




#CAMERA STAMP
def get_camera_frame_world(cam_obj, scene):
    corners_local = cam_obj.data.view_frame(scene=scene)
    return [cam_obj.matrix_world @ v for v in corners_local]

def draw_camera_rectangle_gp5(cam_obj=None,
                              gp_name="GP_CameraFrame",
                              layer_name="CameraFrame",
                              material_name="GP_Rect_Mat",
                              color=(1.0, 1.0, 0.0, 1.0),
                              stroke_radius=0.02):
    scene = bpy.context.scene
    cam_obj = scene.camera
#    if cam_obj is None or cam_obj.type != 'CAMERA':
#        raise ValueError("No active camera found.")

    corners_world = get_camera_frame_world(cam_obj, scene)

    gp_obj = ensure_gp_object(gp_name)
    layer = ensure_layer(gp_obj, layer_name)
    mat = ensure_material(gp_obj, material_name, color)

    # Ensure frame
    frame = None
    for f in layer.frames:
        if f.frame_number == scene.frame_current:
            frame = f
            break
    if frame is None:
        frame = layer.frames.new(scene.frame_current)

    drawing = frame.drawing

    # Create stroke
    drawing.add_strokes(sizes=[len(corners_world)])
    stroke = drawing.strokes[-1]
    stroke.cyclic = True
    stroke.material_index = gp_obj.data.materials.find(mat.name)

    # Assign points with new API
    for i, p in enumerate(corners_world):
        stroke.points[i].position = p
        stroke.points[i].radius = stroke_radius

    gp_obj.show_in_front = True

# TEXT STAMP

# Stick‑font strokes for A–Z, 0–9, and symbols
CHAR_STROKES = {
    "A": [
        [Vector((0,0,0)), Vector((0.5,1,0)), Vector((1,0,0))],        # main outline
        [Vector((0.25,0.5,0)), Vector((0.75,0.5,0))],                 # crossbar
        [Vector((0,0,0)), Vector((0.05,0.1,0))],                      # left serif
        [Vector((1,0,0)), Vector((0.95,0.1,0))]                       # right serif
    ],
    "B": [
        # Vertical spine
        [Vector((0,0,0)), Vector((0,1,0))],

        # Upper lobe (like a D from mid to top)
        [Vector((0,1,0))] +
        [Vector((0.5 + 0.5*math.cos(math.radians(a)),
                 0.75 + 0.25*math.sin(math.radians(a)), 0))
         for a in range(90, -91, -30)] +
        [Vector((0,0.5,0))],

        # Lower lobe (like a D from mid to bottom)
        [Vector((0,0.5,0))] +
        [Vector((0.5 + 0.5*math.cos(math.radians(a)),
                 0.25 + 0.25*math.sin(math.radians(a)), 0))
         for a in range(90, -91, -30)] +
        [Vector((0,0,0))]
    ],
    "C": [
        [
            Vector((0.6 + 0.7*math.cos(math.radians(a)),   # shift center left, radius wider
                    0.5 + 0.5*math.sin(math.radians(a)), 0))
            for a in range(60, 300, 5)  # arc from top to bottom, open on right
        ]
    ],
    "D": [
        # Vertical spine
        [Vector((0,0,0)), Vector((0,1,0))],

        # Curved right side (arc from top to bottom)
        [Vector((0,1,0))] +
        [Vector((0.5 + 0.5*math.cos(math.radians(a)),
                 0.5 + 0.5*math.sin(math.radians(a)), 0))
         for a in range(90, -91, -30)] +
        [Vector((0,0,0))]
    ],
    "E": [
        [Vector((0,0,0)), Vector((0,1,0))],                           # spine
        [Vector((0,1,0)), Vector((1,1,0))],                           # top bar
        [Vector((0,0.5,0)), Vector((0.7,0.5,0))],                     # middle bar
        [Vector((0,0,0)), Vector((1,0,0))]                            # bottom bar
    ],
    "F": [[Vector((0,0,0)), Vector((0,1,0)), Vector((1,1,0))],
          [Vector((0,0.5,0)), Vector((0.7,0.5,0))]],
    "G": [
        # Outer arc (like O but open on right)
        [
            Vector((0.5 + 0.5*math.cos(math.radians(a)),
                    0.5 + 0.5*math.sin(math.radians(a)), 0))
            for a in range(60, 380, 20)  # arc from top to bottom
        ],
        # Horizontal bar inside G
        [Vector((0.5,0.5,0)), Vector((1,0.5,0))]
    ],
    "H": [[Vector((0,0,0)), Vector((0,1,0))],
          [Vector((1,0,0)), Vector((1,1,0))],
          [Vector((0,0.5,0)), Vector((1,0.5,0))]],
    "I": [
        # Vertical stem
        [Vector((0.5,0,0)), Vector((0.5,1,0))],

        # Top horizontal bar
        [Vector((0.2,1,0)), Vector((0.8,1,0))],

        # Bottom horizontal bar
        [Vector((0.2,0,0)), Vector((0.8,0,0))]
    ],
     "J": [
        # Right vertical stem
        [Vector((0.85,1,0)), Vector((0.85,0.25,0))],

        # Bottom smooth curve (no duplicate start point)
        [Vector((0.85,0.25,0))] +
        [Vector((0.4 + 0.45*math.cos(math.radians(a)),
                 0.25 - 0.30*math.sin(math.radians(a)), 0))
         for a in range(15, 181, 15)] 
    ],
    "K": [
        [Vector((0,0,0)), Vector((0,1,0))],                      # vertical spine
        [Vector((0,0.5,0)), Vector((1,1,0))],                    # upper diagonal
        [Vector((0,0.5,0)), Vector((1,0,0))]                     # lower diagonal
    ],
    "L": [
        [Vector((0,1,0)), Vector((0,0,0)), Vector((1,0,0))]      # L shape
    ],
    "M": [
        [Vector((0,0,0)), Vector((0,1,0)), Vector((0.5,0.5,0)),  # left vertical + middle peak
         Vector((1,1,0)), Vector((1,0,0))]                       # right vertical
    ],
    "N": [
        [Vector((0,0,0)), Vector((0,1,0)), Vector((1,0,0)), Vector((1,1,0))]  # diagonal N
    ],
    "O": [
        [
            Vector((0.5 + 0.5*math.cos(math.radians(a)),
                    0.5 + 0.5*math.sin(math.radians(a)), 0))
            for a in range(0, 361, 15)  # full circle, 0° to 360° in 15° steps
        ]
    ],
    "P": [
        # Vertical spine
        [Vector((0,0,0)), Vector((0,1,0))],

        # Top loop (rotated half‑O, bulging to the right)
        [Vector((0,1,0))] +
        [
            Vector((
                0.5 + 0.5*math.cos(math.radians(a)),   # horizontal radius
                0.75 + 0.25*math.sin(math.radians(a)), # vertical radius
                0
            ))
            for a in range(90, -91, -15)  # sweep from top (90°) down to bottom (‑90°), rotated right
        ] +
        [Vector((0,0.5,0))]
    ],
    "Q": [
        # Outer circle (like O)
        [
            Vector((0.5 + 0.5*math.cos(math.radians(a)),
                    0.5 + 0.5*math.sin(math.radians(a)), 0))
            for a in range(0, 361, 15)  # full circle
        ],

        # Longer tail stroke
        [Vector((0.65,0.35,0)), Vector((1.0,0.0,0))]
    ],
    "R": [
        [Vector((0,0,0)), Vector((0,1,0)), Vector((1,1,0)), Vector((1,0.5,0)), Vector((0,0.5,0))], # P loop
        [Vector((0,0.5,0)), Vector((1,0,0))]                                                       # diagonal leg
    ],
    "S": [
        [Vector((1,1,0)), Vector((0,1,0)), Vector((0,0.5,0)),
         Vector((1,0.5,0)), Vector((1,0,0)), Vector((0,0,0))]    # zigzag S
    ],
    "T": [
        [Vector((0,1,0)), Vector((1,1,0))],                   # top bar
        [Vector((0.5,1,0)), Vector((0.5,0,0))]                # vertical stem
    ],
   "U": [
        # Left vertical stem (moved further left)
        [Vector((0.1,1,0)), Vector((0.1,0.3,0))],

        # Right vertical stem (moved further right)
        [Vector((0.9,1,0)), Vector((0.9,0.3,0))],

        # Bottom curved hook (wider arc connecting stems)
        [Vector((0.1,0.3,0))] +
        [Vector((0.5 + 0.4*math.cos(math.radians(a)),
                 0.3 + 0.3*math.sin(math.radians(a)), 0))
         for a in range(180, 360+1, 30)] +
        [Vector((0.9,0.3,0))]
    ],
    "V": [
        [Vector((0,1,0)), Vector((0.5,0,0)), Vector((1,1,0))]  # V shape
    ],
    "W": [
        [Vector((0,1,0)), Vector((0.25,0,0)), Vector((0.5,1,0)), Vector((0.75,0,0)), Vector((1,1,0))]
    ],
    "X": [
        [Vector((0,0,0)), Vector((1,1,0))],                   # diagonal /
        [Vector((1,0,0)), Vector((0,1,0))]                    # diagonal \
    ],
    "Y": [
        [Vector((0,1,0)), Vector((0.5,0.5,0)), Vector((1,1,0))],  # upper fork
        [Vector((0.5,0.5,0)), Vector((0.5,0,0))]                  # stem
    ],
    "Z": [
        [Vector((0,1,0)), Vector((1,1,0)), Vector((0,0,0)), Vector((1,0,0))]  # zigzag Z
    ],
    "1": [
        [Vector((0.5,0,0)), Vector((0.5,1,0))]                   # vertical line
    ],
    "2": [
        [
            Vector((0,1,0)),   # top left
            Vector((1,1,0)),   # top right
            Vector((1,0.5,0)), # mid right
            Vector((0,0,0)),   # bottom left
            Vector((1,0,0))    # bottom right
        ]
    ],
    "3": [
        [
            Vector((0,1,0)),   # top left
            Vector((1,1,0)),   # top right
            Vector((1,0.5,0)), # middle right
            Vector((0.5,0.5,0)), # middle left
            Vector((1,0.5,0)), # back to middle right (reinforce spine)
            Vector((1,0,0)),   # bottom right
            Vector((0,0,0))    # bottom left
        ]
    ],
    "4": [
        [Vector((0,1,0)), Vector((0,0.5,0)), Vector((1,0.5,0))], # crossbar
        [Vector((1,1,0)), Vector((1,0,0))]                       # vertical
    ],
    "5": [
        [Vector((1,1,0)), Vector((0,1,0)), Vector((0,0.5,0)),
         Vector((1,0.5,0)), Vector((1,0,0)), Vector((0,0,0))]    # zigzag 5
    ],
    "6": [
        [Vector((1,1,0)), Vector((0,1,0)), Vector((0,0,0)),
         Vector((1,0,0)), Vector((1,0.5,0)), Vector((0,0.5,0))]  # loop with tail
    ],
    "7": [
        [Vector((0,1,0)), Vector((1,1,0)), Vector((0.5,0,0))]    # angled 7
    ],
    "8": [
        [Vector((0,0,0)), Vector((0,1,0)), Vector((1,1,0)),
         Vector((1,0,0)), Vector((0,0,0))],                      # outer box
        [Vector((0,0.5,0)), Vector((1,0.5,0))]                   # middle bar
    ],
    "9": [
        [Vector((1,0,0)), Vector((1,1,0)), Vector((0,1,0)),
         Vector((0,0.5,0)), Vector((1,0.5,0))]                   # loop with tail
    ],
    "0": [
        # Outer O shape (ellipse arc)
        [
            Vector((
                0.5 + 0.5*math.cos(math.radians(a)),
                0.5 + 0.5*math.sin(math.radians(a)),
                0
            ))
            for a in range(0, 360, 15)  # full circle
        ] + [Vector((1,0.5,0))],  # close loop

        # Diagonal slash inside
        [
            Vector((0.2,0.2,0)),
            Vector((0.8,0.8,0))
        ]
    ],
    # Period
    ".": [
        [Vector((0.5,0,0)), Vector((0.5,0.1,0))]
    ],

    # Comma
    ",": [
        [Vector((0.5,0,0)), Vector((0.45,-0.15,0))]
    ],

    # Colon
    ":": [
        [Vector((0.5,0.8,0)), Vector((0.5,0.9,0))],
        [Vector((0.5,0.1,0)), Vector((0.5,0.2,0))]
    ],

    # Semicolon
    ";": [
        [Vector((0.5,0.8,0)), Vector((0.5,0.9,0))],
        [Vector((0.5,0.1,0)), Vector((0.45,-0.15,0))]
    ],

    # Dash / Minus
    "-": [
        [Vector((0.2,0.5,0)), Vector((0.8,0.5,0))]
    ],

    # Plus
    "+": [
        [Vector((0.2,0.5,0)), Vector((0.8,0.5,0))],
        [Vector((0.5,0.2,0)), Vector((0.5,0.8,0))]
    ],

    # Asterisk
    "*": [
        [Vector((0.5,0.2,0)), Vector((0.5,0.8,0))],
        [Vector((0.2,0.5,0)), Vector((0.8,0.5,0))],
        [Vector((0.25,0.25,0)), Vector((0.75,0.75,0))],
        [Vector((0.25,0.75,0)), Vector((0.75,0.25,0))]
    ],

    # Slash
    "/": [
        [Vector((0.2,0,0)), Vector((0.8,1,0))]
    ],

    # Backslash
    "\\": [
        [Vector((0.2,1,0)), Vector((0.8,0,0))]
    ],

    # Equals
    "=": [
        [Vector((0.2,0.65,0)), Vector((0.8,0.65,0))],
        [Vector((0.2,0.35,0)), Vector((0.8,0.35,0))]
    ],

    "!": [
        # Main vertical stroke (stops at 0.3 instead of 0.2)
        [
            Vector((0.5,0.4,0)),  # lower end of stroke
            Vector((0.5,1.0,0))   # top end of stroke
        ],

        # Dot at the bottom (separate, with gap)
        [
            Vector((0.5,0,0)),
            Vector((0.5,0.1,0))
        ]
    ],

    # Question
    "?": [
        [Vector((0.2,0.8,0)), Vector((0.5,1,0)), Vector((0.8,0.8,0)), Vector((0.5,0.6,0))],
        [Vector((0.5,0,0)), Vector((0.5,0.1,0))]
    ],

    # Parentheses
    "(": [
        [Vector((0.7,1,0)), Vector((0.3,0.5,0)), Vector((0.7,0,0))]
    ],
    ")": [
        [Vector((0.3,1,0)), Vector((0.7,0.5,0)), Vector((0.3,0,0))]
    ],

    # Brackets
    "[": [
        [Vector((0.7,1,0)), Vector((0.3,1,0)), Vector((0.3,0,0)), Vector((0.7,0,0))]
    ],
    "]": [
        [Vector((0.3,1,0)), Vector((0.7,1,0)), Vector((0.7,0,0)), Vector((0.3,0,0))]
    ],

    # Curly braces
    "{": [
        [Vector((0.7,1,0)), Vector((0.5,0.8,0)), Vector((0.5,0.2,0)), Vector((0.7,0,0))]
    ],
    "}": [
        [Vector((0.3,1,0)), Vector((0.5,0.8,0)), Vector((0.5,0.2,0)), Vector((0.3,0,0))]
    ]
}
def ensure_gp_object(name="GP_ManualText"):
    gp_obj = bpy.context.active_object

    # Check if it's a Grease Pencil
    if gp_obj and gp_obj.type == 'GREASEPENCIL':
        gp_data = gp_obj.data   # this is the Grease Pencil datablock

    else:
        print("No active Grease Pencil object selected.")
    return gp_obj

def ensure_layer(gp_obj, layer_name="TextLayer"):
    gp_data = gp_obj.data
    layer= gp_data.layers.active
    return layer

def ensure_material(gp_obj, name="GP_Text_Mat", color=(1,1,1,1)):
    mat = gp_obj.active_material
    return mat

def get_camera_frame_size(cam_obj, scene):
    corners = cam_obj.data.view_frame(scene=scene)
    width = (corners[1] - corners[0]).length
    height = (corners[3] - corners[0]).length
    return width, height
def draw_auto_text(text="HELLO<br>WORLD", spacing=1.5, line_height=1.0, line_spacing=0.3, stroke_radius=0.02, rotation_deg=0):
    scene = bpy.context.scene
    cam = scene.camera
    if cam is None:
        raise ValueError("No active camera found.")

    gp_obj = ensure_gp_object()
    layer = ensure_layer(gp_obj)
    mat = ensure_material(gp_obj)

    # Ensure frame
    frame = None
    for f in layer.frames:
        if f.frame_number == scene.frame_current:
            frame = f
            break
    if frame is None:
        frame = layer.frames.new(scene.frame_current)
    

    drawing = frame.drawing

    # Split text into lines using <br>
    lines = text.split("<br>")

    # Camera frame size
    cam_w, cam_h = get_camera_frame_size(cam, scene)
    char_width = spacing
    text_height = 1.0
    max_line_width = max(len(line) * char_width for line in lines)
    scale_x = cam_w / max_line_width
    scale_y = cam_h / (len(lines) * line_height)
    scale = min(scale_x, scale_y) * 2

     # Rotation matrix (around Z axis)
    rot_mat = Matrix.Rotation(math.radians(rotation_deg), 4, 'X')
    
    # Draw each line with spacing
    y_offset = 0.0
    for line_index, line in enumerate(lines):
        line_width = len(line) * char_width * scale
        x_offset = -line_width / 2.0

        for ch in line:
            strokes = CHAR_STROKES.get(ch.upper())
            if not strokes:
                x_offset += char_width * scale
                continue
            for seg in strokes:
                drawing.add_strokes(sizes=[len(seg)])
                stroke = drawing.strokes[-1]
                
                stroke.material_index = gp_obj.data.materials.find(mat.name)
                stroke.cyclic = False
                for i, p in enumerate(seg):
                    local_pos = Vector((x_offset, -y_offset, 0)) + p * scale
                    # Apply rotation
                    local_pos = rot_mat @ local_pos
                    stroke.points[i].position = local_pos
                    stroke.points[i].radius = stroke_radius * scale
            x_offset += char_width * scale

        # move down for next line with extra spacing
        y_offset += (line_height + line_spacing) * scale

    # Position GP object in front of camera and align rotation
#    gp_obj.location = cam.location + cam.matrix_world.to_quaternion() @ Vector((0,0,-2))
#    gp_obj.rotation_euler = cam.rotation_euler
#    gp_obj.show_in_front = True
