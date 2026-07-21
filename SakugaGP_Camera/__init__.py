bl_info = {
    "name" : "SakugaGP - Camera",
    "author" : "Sadewoo (Spikysaurus)", 
    "description" : "Addon for Camera Mirror/Rotations in Camera View, Camera Overscan and Import Animation Template",
    "blender" : (5, 0, 0),
    "version" : (0, 1, 1),
    "location" : "",
    "warning" : "",
    "doc_url": "https://spikysaurus.github.io/", 
    "tracker_url": "", 
    "category" : "Animation" 
}

import bpy,math,os
from bpy.app.handlers import persistent
from bpy.types import (
    Panel,
    Operator,
    PropertyGroup,
)
from bpy.props import (
    EnumProperty,
    BoolProperty,
    IntProperty,
    FloatProperty,
    StringProperty,
    PointerProperty,
)

def string_to_icon(value):
    if value in bpy.types.UILayout.bl_rna.functions["prop"].parameters["icon"].enum_items.keys():
        return bpy.types.UILayout.bl_rna.functions["prop"].parameters["icon"].enum_items[value].value
    return string_to_int(value)

@persistent
def depsgraph_update_pre_handler_172E3(dummy):
    cam = bpy.context.scene.camera.data
    x = None
    if cam is not None:
        x = False
    else:
        x = True
    camera['sna_check_camera'] = x  
def sna_update_sna_rotation_slider_BF78B(self, context):
    sna_updated_prop = self.sna_rotation_slider
    bpy.data.objects[str(bpy.context.scene.camera.name)].rotation_euler.y = bpy.context.scene.sna_rotation_slider


class sna_add_to_view3d_pt_tools_active(bpy.types.Panel):
    bl_label = ""
    bl_idname = "camera"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "SakugaGP"
    def draw_header(self, context):
        layout = self.layout
        layout.popover('wm.camera_popover', text='Camera', icon_value=string_to_icon('CAMERA_DATA'))
   
    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(context.scene.camera.data, "show_passepartout", text="", icon_value=string_to_icon("OUTLINER_OB_CAMERA"))
        row.prop(context.scene.camera.data, "passepartout_alpha", text="")

        row = col.row(align=True)
        row.operator("wm.reset_camera_rotation", text="", icon_value=string_to_icon("LOOP_BACK"))
        row.prop(context.scene, "sna_rotation_slider", text="")

        grid = col.row(align=True)
        grid.operator(
            "wm.select_active_camera",
            text="",
            icon_value=string_to_icon("RESTRICT_SELECT_OFF")
        )
        grid.operator("wm.mirror_camera_horizontally", text="X")
        grid.operator("wm.mirror_camera_vertically", text="Y")
        grid.operator("wm.rotate_counter_clockwise_acaed", text="L")
        grid.operator("wm.rotate_clockwise", text="R")
        
        

class SNA_OT_Select_Active_Camera(bpy.types.Operator):
    bl_idname = "wm.select_active_camera"
    bl_label = "Select Active Camera"
    bl_description = "Select the Active Camera for current scene (Scene Properties > Camera)"
    bl_options = {"REGISTER","UNDO"}

    def execute(self, context):
        bpy.context.view_layer.objects.active = bpy.context.scene.camera
        bpy.ops.object.mode_set(mode='OBJECT')
        for i in bpy.data.objects:
            i.select_set(False)
        bpy.context.scene.camera.select_set(True)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
    

class SNA_OT_Mirror_Camera_Horizontally(bpy.types.Operator):
    bl_idname = "wm.mirror_camera_horizontally"
    bl_label = "Mirror Camera Horizontally"
    bl_description = "Invert X Scale"
    bl_options = {"REGISTER"}

    def execute(self, context):
        cam = bpy.context.scene.camera
        #bpy.ops.view3d.view_center_cursor()
        if cam.scale.x == 1.0:
            cam.scale.x = -1.0
        else :
            cam.scale.x = 1.0
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Mirror_Camera_Vertically(bpy.types.Operator):
    bl_idname = "wm.mirror_camera_vertically"
    bl_label = "Mirror Camera Vertically"
    bl_description = "Invert Y Scale"
    bl_options = {"REGISTER","UNDO"}

    def execute(self, context):
        cam = bpy.context.scene.camera
        if cam.scale.y == 1.0:
            cam.scale.y = -1.0
        else :
            cam.scale.y = 1.0
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Reset_Camera_Rotation(bpy.types.Operator):
    bl_idname = "wm.reset_camera_rotation"
    bl_label = "Reset Camera Rotation"
    bl_description = "Reset Camera Rotation to 0"
    bl_options = {"REGISTER"}

    def execute(self, context):
        bpy.context.scene.sna_rotation_slider = 0.0
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)

class SNA_OT_Rotate_Clockwise(bpy.types.Operator):
    bl_idname = "wm.rotate_clockwise"
    bl_label = "Rotate Clockwise"
    bl_description = "Rotate Camera Clockwise"
    bl_options = {"REGISTER"}

    def execute(self, context):
        bpy.context.scene.sna_rotation_slider = float(bpy.context.scene.sna_rotation_slider - bpy.context.scene.sna_rotation_steps)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Rotate_Counter_Clockwise_Acaed(bpy.types.Operator):
    bl_idname = "wm.rotate_counter_clockwise_acaed"
    bl_label = "Rotate Counter Clockwise"
    bl_description = "Rotate Camera Counter Clockwise"
    bl_options = {"REGISTER"}

    def execute(self, context):
        bpy.context.scene.sna_rotation_slider = float(bpy.context.scene.sna_rotation_slider + bpy.context.scene.sna_rotation_steps)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)

#Overscan
def string_to_icon(value):
    if value in bpy.types.UILayout.bl_rna.functions["prop"].parameters["icon"].enum_items.keys():
        return bpy.types.UILayout.bl_rna.functions["prop"].parameters["icon"].enum_items[value].value
    return string_to_int(value)

class RENDER_OT_co_duplicate_camera(Operator):
    bl_idname = "scene.co_duplicate_camera"
    bl_label = "Bake to New Camera"
    bl_description = ("Make a new overscan camera with all the settings builtin\n"
                      "Needs an active Camera type in the Scene")
     
    
    @classmethod
    def poll(cls, context):
        active_cam = getattr(context.scene, "camera", None)
        return active_cam is not None

    def execute(self, context):
        active_cam = getattr(context.scene, "camera", None)
        try:
            if active_cam and active_cam.type == 'CAMERA':
                cam_obj = active_cam.copy()
                cam_obj.data = active_cam.data.copy()
                cam_obj.name = "Camera_Overscan"
                context.collection.objects.link(cam_obj)
        except:
            self.report({'WARNING'}, "Setting up a new Overscan Camera has failed")
            return {'CANCELLED'}

        return {'FINISHED'}
        
class SNA_OT_Import_Template(bpy.types.Operator):
    bl_idname = "wm.import_template"
    bl_label = "Import Template"
    bl_description = "Import Animation Template as Mesh Plane, Overscan's Width & Height value will be updated to the Image resolution"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        
        overscan = context.scene.camera_overscan
        overscan.activate = True
        # Load the image directly to get its size
        try:
            img = bpy.data.images.load(self.filepath)
        except RuntimeError:
            self.report({'ERROR'}, f"Could not load image: {self.filepath}")
            return {'CANCELLED'}

        # Update overscan sizes to image size
        overscan.custom_res_x = img.size[0]
        overscan.custom_res_y = img.size[1]

        # Delete any active plane (optional cleanup)
#        if context.active_object and context.active_object.type == 'MESH':
#            bpy.data.objects.remove(context.active_object, do_unlink=True)

        # import the image plane so it fits the camera
        bpy.ops.image.import_as_mesh_planes(
            files=[{"name": os.path.basename(self.filepath)}],
            directory=os.path.dirname(self.filepath),
            size_mode='CAMERA',
            fill_mode='FIT',
            shader='SHADELESS'
        )
        plane = context.active_object
        action_name = context.scene.sna_camera_action_2_name

        # --- Action handling ---
        action_name = context.scene.sna_camera_action_2_name
        if action_name in bpy.data.actions:
            action = bpy.data.actions[action_name]
        else:
            action = bpy.data.actions.new(name=action_name)
            action.use_fake_user = True

        # Assign action to the Camera
        cam = context.scene.camera
        if cam:
            if not cam.animation_data:
                cam.animation_data_create()
            cam.animation_data.action = action

            # Insert a starting keyframe at frame 1
            cam.keyframe_insert(data_path="location", frame=1)
        
        bpy.ops.screen.frame_jump(end=False)
        bpy.ops.wm.select_active_camera()
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

            
# Foldable panel
class RenderOutputButtonsPanel:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "SakugaGP"

# UI panel
class Camera_popover(bpy.types.Panel):
    bl_label = ""
    bl_idname = "wm.camera_popover"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    
    def draw(self, context):
        scene = context.scene
        overscan = scene.camera_overscan
        layout = self.layout
        layout.use_property_split = False
        layout.use_property_decorate = False  # No animation
        
        
        active_cam = getattr(scene, "camera", None)
        
        colA = layout.column()
        colA.operator("wm.import_template", text="Import Template", icon='IMAGE_DATA')
        colA.operator('wm.camera_action_switch', text='Switch Camera/Overscan', icon_value=string_to_icon('OBJECT_HIDDEN'), emboss=True, depress=False)
        colA.separator()
        box = colA.box()
        colB = box.column(align=True)
        row = colB.row()
        row.label(text="Camera Actions :", icon_value=string_to_icon('ACTION'))
        row.prop(bpy.context.scene, 'sna_toggle_overscan_as_well', text='', icon_value=string_to_icon('CON_OBJECTSOLVER'))
        colB.prop(bpy.context.scene, 'sna_camera_action_1_name', text='', icon_value=string_to_icon('EVENT_NDOF_BUTTON_1'))
        colB.prop(bpy.context.scene, 'sna_camera_action_2_name', text='', icon_value=string_to_icon('EVENT_NDOF_BUTTON_2'))
        
        
        box = layout.box()
        
        row = box.row()
        
        row.label(text="Overscan :",  icon_value=string_to_icon('CON_OBJECTSOLVER'))
        row.prop(overscan, "activate", text="")
        
        if active_cam and active_cam.type == 'CAMERA':
           
            col = box.row(align=True)
            col.label(icon_value=string_to_icon("CAMERA_DATA"))
            col.prop(overscan, 'original_res_x', text="X")
            col.prop(overscan, 'original_res_y', text="Y")
            col.enabled = False

            col = box.column(align=True)
            col.prop(overscan, 'custom_res_x', text="Width")
            col.prop(overscan, 'custom_res_y', text="Height")
            col.prop(overscan, 'custom_res_scale', text="Scale")
            col.enabled = overscan.activate

            
            col = box.column(align=True)
            row2 = col.row(align=True)
            col2 = row2.column(align=True)
            col2.prop(overscan, 'custom_res_offset_x', text="Offset Width")
            col2.prop(overscan, 'custom_res_offset_y', text="Offset Height")
            
            row2.prop(overscan, 'custom_res_retain_aspect_ratio', text="", icon_value=string_to_icon('LINKED'))
            row2.enabled = overscan.activate

            col = box.column()
            col.separator()
            col.operator("scene.co_duplicate_camera", icon="RENDER_STILL")
        else:
            layout.label(text="No active camera in the scene", icon='INFO')


def update(self, context):
    scene = context.scene
    overscan = scene.camera_overscan
    render_settings = scene.render
    active_camera = getattr(scene, "camera", None)
    active_cam = getattr(active_camera, "data", None)

    if not active_cam or active_camera.type not in {'CAMERA'}:
        return None

    if overscan.activate:
        if overscan.original_sensor_size == -1:
            # Save property values
            overscan.original_res_x = render_settings.resolution_x
            overscan.original_res_y = render_settings.resolution_y
            overscan.original_sensor_size = active_cam.sensor_width
            overscan.original_sensor_fit = active_cam.sensor_fit

        if overscan.custom_res_x == 0 or overscan.custom_res_y == 0:
            # Avoid infinite recursion on props update
            if overscan.custom_res_x != render_settings.resolution_x:
                overscan.custom_res_x = render_settings.resolution_x
            if overscan.custom_res_y != render_settings.resolution_y:
                overscan.custom_res_y = render_settings.resolution_y

        # Reset property values
        active_cam.sensor_width = scene.camera_overscan.original_sensor_size

        # Calc sensor size
        active_cam.sensor_fit = 'HORIZONTAL'
        dx = overscan.custom_res_offset_x
        dy = overscan.custom_res_offset_y
        scale = overscan.custom_res_scale * 0.01
        x = int(overscan.custom_res_x * scale + dx)
        y = int(overscan.custom_res_y * scale + dy)
        sensor_size_factor = float(x / overscan.original_res_x)

        # Set new property values
        active_cam.sensor_width = active_cam.sensor_width * sensor_size_factor
        render_settings.resolution_x = x
        render_settings.resolution_y = y

    else:
        if overscan.original_sensor_size != -1:
            # Restore property values
            render_settings.resolution_x = int(overscan.original_res_x)
            render_settings.resolution_y = int(overscan.original_res_y)
            active_cam.sensor_width = overscan.original_sensor_size
            active_cam.sensor_fit = overscan.original_sensor_fit
            overscan.original_sensor_size = -1


def get_overscan_object(context):
    scene = context.scene
    overscan = scene.camera_overscan
    active_camera = getattr(scene, "camera", None)
    active_cam = getattr(active_camera, "data", None)
    if not active_cam or active_camera.type not in {'CAMERA'} or not overscan.activate:
        return None
    return overscan


def update_x_offset(self, context):
    overscan = get_overscan_object(context)
    if overscan is None:
        return

    if overscan.custom_res_retain_aspect_ratio:
        overscan.activate = False  # Recursion guard
        overscan.custom_res_offset_y = int(overscan.custom_res_offset_x * overscan.original_res_y / overscan.original_res_x)

    overscan.activate = True
    update(self, context)


def update_y_offset(self, context):
    overscan = get_overscan_object(context)
    if overscan is None:
        return None

    if overscan.custom_res_retain_aspect_ratio:
        overscan.activate = False  # Recursion guard
        overscan.custom_res_offset_x = int(overscan.custom_res_offset_y * overscan.original_res_x / overscan.original_res_y)

    overscan.activate = True
    update(self, context)


class CameraOverscanProps(PropertyGroup):
    activate: BoolProperty(
        name="Enable Camera Overscan",
        description="Affects the active Scene Camera only\n"
        "(Objects as cameras are not supported)",
        default=False,
        update=update
    )
    custom_res_x: IntProperty(
        name="Target Resolution X",
        default=0,
        min=0,
        max=65536,
        update=update,
    )
    custom_res_y: IntProperty(
        name="Target Resolution Y",
        default=0,
        min=0,
        max=65536,
        update=update,
    )
    custom_res_scale: FloatProperty(
        name="Resolution Percentage",
        default=100,
        min=0,
        max=1000,
        step=100,
        update=update,
    )
    custom_res_offset_x: IntProperty(
        name="Resolution Offset X",
        default=0,
        min=-65536,
        max=65536,
        update=update_x_offset,
    )
    custom_res_offset_y: IntProperty(
        name="Resolution Offset Y",
        default=0,
        min=-65536,
        max=65536,
        update=update_y_offset,
    )
    custom_res_retain_aspect_ratio: BoolProperty(
        name="Retain Aspect Ratio",
        description="Keep the aspect ratio of the original resolution. Affects Offset Width, Offset Height",
        default=False,
    )

    original_res_x: IntProperty(name="Original Resolution X")
    original_res_y: IntProperty(name="Original Resolution Y")

    original_sensor_size: FloatProperty(
        default=-1,
        min=-1,
        max=65536
    )
    original_sensor_fit: StringProperty()

class SNA_OT_Camera_Action_Switch(bpy.types.Operator):
    bl_idname = "wm.camera_action_switch"
    bl_label = "Camera Action Switch"
    bl_description = "Switch to Original Camera/Overscan Size while also switching between the Actions"
    bl_options = {"REGISTER"}

    def execute(self, context):
        scene, cam = context.scene, context.scene.camera
        if not cam or not cam.animation_data:
            return {"CANCELLED"}

        a1 = bpy.data.actions.get(scene.sna_camera_action_1_name)
        a2 = bpy.data.actions.get(scene.sna_camera_action_2_name)
        if not a1 or not a2:
            return {"CANCELLED"}

        if scene.sna_toggle_overscan_as_well:
            scene.camera_overscan.activate = not scene.camera_overscan.activate
            cam.animation_data.action = a2 if scene.camera_overscan.activate else a1
        else:
            cam.animation_data.action = a2 if cam.animation_data.action == a1 else a1

        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)

classes = [
    SNA_OT_Select_Active_Camera,
    SNA_OT_Mirror_Camera_Horizontally,
    SNA_OT_Mirror_Camera_Vertically,
    SNA_OT_Reset_Camera_Rotation,
    sna_add_to_view3d_pt_tools_active,
    SNA_OT_Rotate_Clockwise,
    SNA_OT_Rotate_Counter_Clockwise_Acaed,
    RENDER_OT_co_duplicate_camera,
    CameraOverscanProps,
    SNA_OT_Camera_Action_Switch,
    SNA_OT_Import_Template,
    Camera_popover
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
    bpy.types.Scene.sna_rotation_slider = bpy.props.FloatProperty(
        name='Rotation Slider', default=0.0, step=3, precision=3,
        update=sna_update_sna_rotation_slider_BF78B
    )
    bpy.types.Scene.sna_rotation_steps = bpy.props.FloatProperty(
        name='Rotation Steps', default=math.radians(45), min=0.0, step=5, precision=2
    )
    bpy.types.Scene.camera_overscan = PointerProperty(type=CameraOverscanProps)
    bpy.types.Scene.sna_camera_action_switch = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.sna_camera_action_1_name = bpy.props.StringProperty(default='CameraAction')
    bpy.types.Scene.sna_camera_action_2_name = bpy.props.StringProperty(default='CameraOverscan')
    bpy.types.Scene.sna_toggle_overscan_as_well = bpy.props.BoolProperty(default=True)

    bpy.app.handlers.depsgraph_update_pre.append(depsgraph_update_pre_handler_172E3)

def unregister():
    del bpy.types.Scene.sna_rotation_slider
    del bpy.types.Scene.sna_rotation_steps
    del bpy.types.Scene.camera_overscan
    del bpy.types.Scene.sna_camera_action_switch
    del bpy.types.Scene.sna_camera_action_1_name
    del bpy.types.Scene.sna_camera_action_2_name
    del bpy.types.Scene.sna_toggle_overscan_as_well

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    bpy.app.handlers.depsgraph_update_pre.remove(depsgraph_update_pre_handler_172E3)

if __name__ == "__main__":
    register()

