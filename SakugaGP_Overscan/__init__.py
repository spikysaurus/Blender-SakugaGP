bl_info = {
    "name" : "SakugaGP - Overscan",
    "author" : "Sadewoo (Spikysaurus)", 
    "description" : "Camera Overscan and Switch between two Camera Actions",
    "blender" : (5, 0, 0),
    "version" : (0, 0, 0),
    "location" : "",
    "warning" : "",
    "doc_url": "https://spikysaurus.github.io/", 
    "tracker_url": "", 
    "category" : "Animation" 
}

import bpy
from bpy.types import (
    Panel,
    Operator,
    PropertyGroup,
)
from bpy.props import (
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


# Foldable panel
class RenderOutputButtonsPanel:
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "output"

# UI panel
class RENDER_PT_overscan(RenderOutputButtonsPanel, Panel):
    bl_label = "Overscan"
    bl_parent_id = "RENDER_PT_format"
    bl_options = {'DEFAULT_CLOSED'}
    

    def draw_header(self, context):
        overscan = context.scene.camera_overscan
        self.layout.prop(overscan, "activate", text="")

    def draw(self, context):
        scene = context.scene
        overscan = scene.camera_overscan
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation

        active_cam = getattr(scene, "camera", None)
        
        colA = layout.column(align=True)  
        colA.prop(bpy.context.scene, 'sna_camera_action_1_name', text='', icon_value=string_to_icon('EVENT_NDOF_BUTTON_1'), emboss=True)
        colA.prop(bpy.context.scene, 'sna_camera_action_2_name', text='', icon_value=string_to_icon('EVENT_NDOF_BUTTON_2'), emboss=True)
        colA.operator('wm.camera_action_switch_950fd', text='Switch Camera Action ', icon_value=string_to_icon('OBJECT_HIDDEN'), emboss=True, depress=False)
        colA.prop(bpy.context.scene, 'sna_toggle_overscan_as_well', text='Toggle Overscan', icon_value=0, emboss=True)
        
        if active_cam and active_cam.type == 'CAMERA':
           
            col = layout.column(align=True)
            col.prop(overscan, 'original_res_x', text="Original X")
            col.prop(overscan, 'original_res_y', text="Y")
            col.enabled = False

            col = layout.column(align=True)
            col.prop(overscan, 'custom_res_x', text="New X")
            col.prop(overscan, 'custom_res_y', text="Y")
            col.prop(overscan, 'custom_res_scale', text="%")
            col.enabled = overscan.activate

            col = layout.column(align=True)
            col.prop(overscan, 'custom_res_offset_x', text="dX")
            col.prop(overscan, 'custom_res_offset_y', text="dY")
            col.prop(overscan, 'custom_res_retain_aspect_ratio', text="Retain Aspect Ratio")
            col.enabled = overscan.activate

            col = layout.column()
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

    # Check if there is a camera type in the scene (Object as camera doesn't work)
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
        description="Keep the aspect ratio of the original resolution. Affects dX, dY",
        default=False,
    )

    original_res_x: IntProperty(name="Original Resolution X")
    original_res_y: IntProperty(name="Original Resolution Y")

    # The hard limit is sys.max which is too much, used 65536 instead
    original_sensor_size: FloatProperty(
        default=-1,
        min=-1,
        max=65536
    )
    original_sensor_fit: StringProperty()

class SNA_OT_Camera_Action_Switch_950Fd(bpy.types.Operator):
    bl_idname = "wm.camera_action_switch_950fd"
    bl_label = "Camera Action Switch"
    bl_description = "Switch between Camera's Actions you set in the setting"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        CO = bpy.context.scene.sna_camera_action_2_name
        CA = bpy.context.scene.sna_camera_action_1_name
        OV = bpy.context.scene.sna_toggle_overscan_as_well
        object = bpy.context.scene.camera
        action = object.animation_data.action
        CameraOverscan = CO
        CameraAction = CA
        if OV == True:
            if bpy.context.scene.camera_overscan.activate == False:
                bpy.context.scene.camera_overscan.activate = True
                bpy.context.scene.camera.animation_data.action = bpy.data.actions.get(str(CameraOverscan))
            else:
                bpy.context.scene.camera_overscan.activate = False
                bpy.context.scene.camera.animation_data.action = bpy.data.actions.get(str(CameraAction))
        else:
            if bpy.context.scene.camera.animation_data.action == bpy.data.actions.get(str(CameraOverscan)):
                bpy.context.scene.camera.animation_data.action = bpy.data.actions.get(str(CameraAction))
            elif bpy.context.scene.camera.animation_data.action == bpy.data.actions.get(str(CameraAction)):
                bpy.context.scene.camera.animation_data.action = bpy.data.actions.get(str(CameraOverscan))
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
    
def register():
    bpy.utils.register_class(RENDER_OT_co_duplicate_camera)
    bpy.utils.register_class(CameraOverscanProps)
    bpy.utils.register_class(RENDER_PT_overscan)
    bpy.types.Scene.camera_overscan = PointerProperty(
        type=CameraOverscanProps
    )
    bpy.utils.register_class(SNA_OT_Camera_Action_Switch_950Fd)
    bpy.types.Scene.sna_camera_action_switch = bpy.props.BoolProperty(name='Camera Action Switch', description='', default=False)
    bpy.types.Scene.sna_camera_action_1_name = bpy.props.StringProperty(name='Camera Action 1 Name', description='', default='CameraAction', subtype='NONE', maxlen=0)
    bpy.types.Scene.sna_camera_action_2_name = bpy.props.StringProperty(name='Camera Action 2 Name', description='', default='CameraOverscan', subtype='NONE', maxlen=0)
    bpy.types.Scene.sna_toggle_overscan_as_well = bpy.props.BoolProperty(name='Toggle Overscan as well', description='', default=True)


def unregister():
    bpy.utils.unregister_class(RENDER_PT_overscan)
    bpy.utils.unregister_class(RENDER_OT_co_duplicate_camera)
    bpy.utils.unregister_class(CameraOverscanProps)
    del bpy.types.Scene.camera_overscan
    
    del bpy.types.Scene.sna_toggle_overscan_as_well
    del bpy.types.Scene.sna_camera_action_2_name
    del bpy.types.Scene.sna_camera_action_1_name
    del bpy.types.Scene.sna_camera_action_switch
    bpy.utils.unregister_class(SNA_OT_Camera_Action_Switch_950Fd)


if __name__ == "__main__":
    register()