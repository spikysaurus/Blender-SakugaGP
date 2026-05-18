bl_info = {
    "name" : "SakugaGP - Stamps",
    "author" : "Sadewoo (Spikysaurus)", 
    "description" : "Camera and Text Stamps for Grease Pencil",
    "blender" : (5, 0, 0),
    "version" : (0, 2, 0),
    "location" : "",
    "warning" : "",
    "doc_url": "https://spikysaurus.github.io", 
    "tracker_url": "", 
    "category" : "Animation" 
}

import bpy
import math
import os
import platform
from mathutils import Vector, Matrix

# --- CROSS-PLATFORM FONT RETRIEVAL ENGINE ---
def get_default_font_directory():
    # Read path from Blender's Preferences > File Paths > Data > Fonts
    prefs_path = bpy.context.preferences.filepaths.font_directory
    if prefs_path and os.path.exists(prefs_path):
        return prefs_path
        
    # Hardware environment architecture fallbacks
    sys_type = platform.system()
    if sys_type == "Windows":
        return r"C:\Windows\Fonts"
    elif sys_type == "Darwin": # macOS
        return "/Library/Fonts"
    else: # Linux
        return "/usr/share/fonts"

# --- PROPERTIES ---
class FunctionRunnerSettings(bpy.types.PropertyGroup):
    text_input: bpy.props.StringProperty(
        name="Input Text",
        description="",
        default=""
    )

class TextFontSizeSettings(bpy.types.PropertyGroup):
    font_size_input: bpy.props.FloatProperty(
        name="Text Font Size",
        description="Adjust the size of the stamped text geometry",
        default=1.0,   
        min=0.1,       
        max=20.0,      
        soft_min=0.1,
        soft_max=20.0
    )
    font_file_path: bpy.props.StringProperty(
        name="Font File",
        description="Select a .ttf or .otf vector font file path",
        default=get_default_font_directory(), # Sets system folder root dynamically
        subtype='FILE_PATH'
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
        font_size = context.scene.text_font_size_settings.font_size_input
        font_path = context.scene.text_font_size_settings.font_file_path
        
        if custom_text == "": 
            return {'CANCELLED'}
        
        text_content = custom_text
        location = (0.0, 0.0, 0.0)
        rotation_rad = (math.radians(90), 0.0, 0.0)

        target_gp_obj = context.active_object

        if not target_gp_obj or target_gp_obj.type != 'GREASEPENCIL':
            self.report({'ERROR'}, "Select a Grease Pencil object first!")
            return {'CANCELLED'}

        if context.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')

        bpy.ops.object.select_all(action='DESELECT')

        # Add and configure text object
        bpy.ops.object.text_add(location=location, rotation=rotation_rad)
        temp_text_obj = context.active_object
        temp_text_obj.name = "Temp_Text_Source"
        temp_text_obj.data.body = text_content
        temp_text_obj.data.size = font_size

        # Apply Font File configuration
        if font_path and os.path.exists(font_path) and os.path.isfile(font_path):
            try:
                loaded_font = bpy.data.fonts.load(font_path)
                temp_text_obj.data.font = loaded_font
            except Exception as e:
                self.report({'WARNING'}, f"Could not load custom font file: {e}")

        # Convert text curve to modern Grease Pencil V3 object block
        bpy.ops.object.convert(target='GREASEPENCIL')
        temp_gp_obj = context.active_object
 
        bpy.data.materials.remove(temp_gp_obj.active_material)
        bpy.ops.object.material_slot_remove()
            
        temp_gp_obj.select_set(True)
        target_gp_obj.select_set(True)
        context.view_layer.objects.active = target_gp_obj
        
        # Join operations fuse stroke geometry together automatically
        
        bpy.ops.object.join()
        
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.grease_pencil.stroke_material_set()

        # CLEAN UP UNUSED DATABLOCKS
        for text_data in bpy.data.curves:
            if text_data.name.startswith("Temp_Text_Source") and text_data.users == 0:
                bpy.data.curves.remove(text_data)

        return {'FINISHED'}

class TextStampObjOperator(bpy.types.Operator):
    bl_idname = "wm.text_stamp_obj"
    bl_label = "Text Stamp Object"

    def execute(self, context):
        custom_text = context.scene.function_runner_settings.text_input
        font_size = context.scene.text_font_size_settings.font_size_input
        font_path = context.scene.text_font_size_settings.font_file_path
        
        if custom_text == "": 
            return {'CANCELLED'}
        
        text_content = custom_text
        location = (0.0, 0.0, 0.0)
        rotation_rad = (math.radians(90), 0.0, 0.0)

        if context.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
        
        bpy.ops.object.select_all(action='DESELECT')

        # Add and configure text object
        bpy.ops.object.text_add(location=location, rotation=rotation_rad)
        temp_text_obj = context.active_object
        temp_text_obj.name = "txt_" + custom_text
        temp_text_obj.data.body = text_content
        temp_text_obj.data.size = font_size
        
        # Apply custom font to pure 3D Text Object too
        if font_path and os.path.exists(font_path) and os.path.isfile(font_path):
            try:
                loaded_font = bpy.data.fonts.load(font_path)
                temp_text_obj.data.font = loaded_font
            except Exception as e:
                self.report({'WARNING'}, f"Could not load custom font file: {e}")
        
        return {'FINISHED'}

class RunTestOperator(bpy.types.Operator):
    bl_idname = "wm.run_test"
    bl_label = "Run Test"
    def execute(self, context):
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
        font_size_settings = context.scene.text_font_size_settings
        
        col = layout.column(align=True)
        col.prop(settings, "text_input", text="Text")
        col.prop(font_size_settings, "font_file_path", text="Font")
        col.prop(font_size_settings, "font_size_input", text="Font Size", slider=True)
        
        col.separator()
        col.operator(TextStampOperator.bl_idname, text="Add Text into GP")
        col.operator(TextStampObjOperator.bl_idname, text="Add Text Object")
        col.operator(CameraStampOperator.bl_idname, text="Camera Stamp")

# --- REGISTER ---
classes = (
    FunctionRunnerSettings,
    TextFontSizeSettings,
    CameraStampOperator,
    TextStampOperator,
    TextStampObjOperator,
    RunTestOperator,
    FunctionRunnerPanel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.function_runner_settings = bpy.props.PointerProperty(type=FunctionRunnerSettings)
    bpy.types.Scene.text_font_size_settings = bpy.props.PointerProperty(type=TextFontSizeSettings)
     
def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.function_runner_settings
    del bpy.types.Scene.text_font_size_settings

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
    if mat is None:
        
        return {'CANCELLED'} 
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
