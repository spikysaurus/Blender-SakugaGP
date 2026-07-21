bl_info = {
    "name" : "SakugaGP - Stamps",
    "author" : "Sadewoo (Spikysaurus)", 
    "description" : "Addon for Inserting Text directly into Grease Pencil and Draw Outline of Active Camera",
    "blender" : (5, 0, 0),
    "version" : (0, 2, 1),
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

class CameraStampOperator(bpy.types.Operator):
    bl_idname = "wm.camera_stamp"
    bl_label = "Camera Stamp"

    def execute(self, context):
        draw_camera_rectangle_gp5()
        return {'FINISHED'}

# --- Helpers ---
def get_camera_frame_world(cam_obj, scene):
    corners_local = cam_obj.data.view_frame(scene=scene)
    return [cam_obj.matrix_world @ v for v in corners_local]

def ensure_gp_object(name="GP_CameraFrame"):
    gp_obj = bpy.data.objects.get(name)
    if gp_obj is None:
        gp_data = bpy.data.grease_pencils.new(name)
        gp_obj = bpy.data.objects.new(name, gp_data)
        bpy.context.scene.collection.objects.link(gp_obj)
    return gp_obj

def ensure_layer(gp_obj, layer_name="CameraFrame"):
    gp_data = gp_obj.data
    layer = gp_data.layers.get(layer_name)
    if layer is None:
        layer = gp_data.layers.new(layer_name)
    return layer

def ensure_material(gp_obj, material_name="GP_Rect_Mat", color=(1,1,0,1)):
    mat = bpy.data.materials.get(material_name)
    if mat is None:
        mat = bpy.data.materials.new(material_name)
        mat.grease_pencil.color = color
    if mat.name not in gp_obj.data.materials:
        gp_obj.data.materials.append(mat)
    return mat

def draw_camera_rectangle_gp5():
    scene = bpy.context.scene
    cam = scene.camera
    gp_obj = bpy.context.active_object
    if not (cam and cam.type == 'CAMERA' and gp_obj and gp_obj.type == 'GREASEPENCIL'):
        return {'CANCELLED'}

    # Camera corners in world space → GP local space
    corners_world = [cam.matrix_world @ v for v in cam.data.view_frame(scene=scene)]
    corners_local = [gp_obj.matrix_world.inverted() @ p for p in corners_world]

    # Active layer/frame
    layer = gp_obj.data.layers.active
    frame = layer.active_frame
    if not frame:
        return {'CANCELLED'}
    drawing = frame.drawing

    # Active material slot
    mat_index = gp_obj.active_material_index

    # Brush radius using unprojected size
    brush = bpy.context.tool_settings.gpencil_paint.brush
    if brush:
        # Use unprojected_size but scale down for visual match
        stroke_radius = brush.unprojected_size * 0.06
    else:
        stroke_radius = 0.02


    # Create stroke
    drawing.add_strokes(sizes=[len(corners_local)])
    stroke = drawing.strokes[-1]
    stroke.cyclic = True
    stroke.material_index = mat_index
    for i, p in enumerate(corners_local):
        stroke.points[i].position = p
        stroke.points[i].radius = stroke_radius

    gp_obj.show_in_front = True

    # Reproject + select new stroke + set opacity
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.grease_pencil.select_all(action='DESELECT')
    stroke.select = True
#    bpy.ops.grease_pencil.set_uniform_thickness(thickness=brush.unprojected_size)
    bpy.ops.grease_pencil.set_uniform_opacity(opacity_stroke=1.0, opacity_fill=1.0)
    bpy.ops.grease_pencil.reproject(type='FRONT')
    return {'FINISHED'}


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

class MainSettings(bpy.types.PropertyGroup):
    text_input: bpy.props.StringProperty(
        name="Text Input",
        default=""
    )
    text_align: bpy.props.EnumProperty(
        name="Alignment",
        items=[
            ('LEFT', "Left", "Align text to the left", 'ALIGN_LEFT',0),
            ('CENTER', "Center", "Align text to the center", 'ALIGN_CENTER',1),
            ('RIGHT', "Right", "Align text to the right", 'ALIGN_RIGHT',2),
        ],
        default='LEFT'
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

class TextStampOperator(bpy.types.Operator):
    bl_idname = "wm.text_stamp"
    bl_label = "Text Stamp"

    def execute(self, context):
        settings = context.scene.function_runner_settings
        custom_text, align = settings.text_input, settings.text_align
        font_size = context.scene.text_font_size_settings.font_size_input
        font_path = context.scene.text_font_size_settings.font_file_path

        if not custom_text:
            return {'CANCELLED'}

        gp_obj = context.active_object
        if not gp_obj or gp_obj.type != 'GREASEPENCIL':
            self.report({'ERROR'}, "Select a Grease Pencil object first!")
            return {'CANCELLED'}

        # Ensure Object mode
        if context.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')

        # Add temporary text object with original rotation
        rotation_rad = (math.radians(90), 0.0, 0.0)
        bpy.ops.object.text_add(location=(0,0,0), rotation=rotation_rad)
        temp_text = context.active_object
        temp_text.name = "Temp_Text_Source"
        temp_text.data.body = custom_text
        temp_text.data.size = font_size
        temp_text.data.align_x = align

        # Reuse active material from Grease Pencil object
        if gp_obj.active_material:
            # Save reference to the default material created with the text
            default_mat = temp_text.active_material

            # Clear slots and assign GP material
            temp_text.data.materials.clear()
            temp_text.data.materials.append(gp_obj.active_material)

            # Delete the default material from Blender file if it exists
            if default_mat and default_mat != gp_obj.active_material:
                bpy.data.materials.remove(default_mat)

        # Apply font file if valid
        if font_path and os.path.isfile(font_path):
            try:
                temp_text.data.font = bpy.data.fonts.load(font_path)
            except Exception as e:
                self.report({'WARNING'}, f"Could not load font file: {e}")

        # Convert to GP object
        bpy.ops.object.convert(target='GREASEPENCIL')
        temp_gp = context.active_object

        # After conversion, Blender duplicates the material — fix that:
        if gp_obj.active_material:
            # Grab the duplicate material created during conversion
            dup_mat = temp_gp.active_material
            # Clear slots and assign the original GP material
            temp_gp.data.materials.clear()
            temp_gp.data.materials.append(gp_obj.active_material)
            # Remove the duplicate from the file if it’s not the same
            if dup_mat and dup_mat != gp_obj.active_material:
                bpy.data.materials.remove(dup_mat)


        # Copy strokes from Converted Layer
        src_layer = temp_gp.data.layers.get("Converted Layer")
        if src_layer and src_layer.active_frame:
            # Go into edit mode on temp GP
            context.view_layer.objects.active = temp_gp
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.grease_pencil.select_all(action='SELECT')
            bpy.ops.grease_pencil.copy()

            # Switch to target GP object
            bpy.ops.object.mode_set(mode='OBJECT')
            context.view_layer.objects.active = gp_obj
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.grease_pencil.select_all(action='DESELECT')
            # Paste into active layer/frame, preserving world transform
            bpy.ops.grease_pencil.paste(type='ACTIVE', keep_world_transform=True)
            bpy.ops.object.mode_set(mode='OBJECT')

        # Remove Converted Layer and temp GP object
        if src_layer:
            temp_gp.data.layers.remove(src_layer)
        bpy.data.objects.remove(temp_gp, do_unlink=True)

        # Reproject + uniform opacity
        context.view_layer.objects.active = gp_obj
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.grease_pencil.stroke_material_set()
        bpy.ops.grease_pencil.reproject(type="FRONT")
        bpy.ops.grease_pencil.set_uniform_opacity(opacity_stroke=1.0, opacity_fill=1.0)
        gp_obj.select_set(True)
        context.view_layer.objects.active = gp_obj
        # Clean up temp curves
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
class MainPanel(bpy.types.Panel):
    bl_label = "Stamps"
    bl_idname = "VIEW3D_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SakugaGP'

    def draw(self, context):
        layout = self.layout
        settings = context.scene.function_runner_settings
        font_size_settings = context.scene.text_font_size_settings
        
        box = layout.box()
        col = box.column(align=True)
        col.label(text="Text Stamp",icon="FILE_TEXT")
        col.prop(font_size_settings, "font_file_path", text="Font")
        col.prop(settings, "text_align", text="Align")
        row = col.row(align=True)
        row.label(text="Size:")
        row.prop(font_size_settings, "font_size_input", text="", slider=False)
        col.textbox(settings, "text_input", placeholder="Type your text here")
        
        col.separator()
        obj = bpy.context.active_object
        if obj.type == "GREASEPENCIL":
            col.operator(TextStampOperator.bl_idname, text="Insert Text into GPencil", icon="OUTLINER_DATA_GREASEPENCIL")
        col.operator(TextStampObjOperator.bl_idname, text="Add Text as Object", icon="OBJECT_DATA")
        if obj.type == "GREASEPENCIL":
            box = layout.box()
            col = box.column(align=True)
            col.label(text="Camera Stamp",icon="CAMERA_DATA")
            box.operator(CameraStampOperator.bl_idname, text="Draw Outline of Camera", icon="MATPLANE")

# --- REGISTER ---
classes = (
    MainSettings,
    TextFontSizeSettings,
    CameraStampOperator,
    TextStampOperator,
    TextStampObjOperator,
    RunTestOperator,
    MainPanel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.function_runner_settings = bpy.props.PointerProperty(type=MainSettings)
    bpy.types.Scene.text_font_size_settings = bpy.props.PointerProperty(type=TextFontSizeSettings)
     
def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.function_runner_settings
    del bpy.types.Scene.text_font_size_settings

if __name__ == "__main__":
    register()

