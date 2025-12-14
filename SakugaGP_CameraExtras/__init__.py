bl_info = {
    "name" : "SakugaGP - Camera Extras",
    "author" : "Sadewoo (Spikysaurus)", 
    "description" : "Extra Camera Stuff",
    "blender" : (5, 0, 0),
    "version" : (0, 0, 0),
    "location" : "",
    "warning" : "",
    "doc_url": "https://spikysaurus.github.io/", 
    "tracker_url": "", 
    "category" : "Animation" 
}

import bpy
from bpy.app.handlers import persistent

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
addon_keymaps = {}    
def sna_update_sna_rotation_slider_BF78B(self, context):
    sna_updated_prop = self.sna_rotation_slider
    bpy.data.objects[str(bpy.context.scene.camera.name)].rotation_euler.y = bpy.context.scene.sna_rotation_slider

#https://projects.blender.org/blender/blender/issues/146576
#class Mute_Camera(bpy.types.Operator):
#    scene = bpy.context.scene
#    camera = scene.camera

#    if camera and camera.animation_data and camera.animation_data.action:
#        action = camera.animation_data.action
#        for fcurve in action.fcurves_all:
#            # Only affect transform channels
#            if fcurve.data_path in {"location", "rotation_euler", "scale"}:
#                fcurve.mute = False

#        # Force refresh so changes are visible immediately
#        scene.frame_set(scene.frame_current)
#        
class sna_add_to_view3d_pt_tools_active_63904(bpy.types.Panel):
    bl_label = 'Camera Extras'
    bl_idname = 'camera_extras'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = 'SakugaGP'
    bl_order = 0
    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        if True:
#            box_FF417 = layout.box()
            box_FF417 = layout.column(heading='', align=True)
            box_FF417.alert = False
            box_FF417.enabled = True
            box_FF417.active = True
            box_FF417.use_property_split = False
            box_FF417.use_property_decorate = False
            box_FF417.alignment = 'Expand'.upper()
            box_FF417.scale_x = 1.0
            box_FF417.scale_y = 1.0
            if not True: box_FF417.operator_context = "EXEC_DEFAULT"
            op = box_FF417.operator('wm.select_active_camera_81ec7', text='Select Camera', icon_value=string_to_icon('RESTRICT_SELECT_OFF'), emboss=True, depress=False)
            col_95FB8 = box_FF417.column(heading='', align=True)
            col_95FB8.alert = False
            col_95FB8.enabled = True
            col_95FB8.active = True
            col_95FB8.use_property_split = False
            col_95FB8.use_property_decorate = False
            col_95FB8.scale_x = 1.0
            col_95FB8.scale_y = 1.0
            col_95FB8.alignment = 'Expand'.upper()
            col_95FB8.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_380B8 = col_95FB8.row(heading='', align=True)
            row_380B8.alert = False
            row_380B8.enabled = True
            row_380B8.active = True
            row_380B8.use_property_split = False
            row_380B8.use_property_decorate = False
            row_380B8.scale_x = 1.0
            row_380B8.scale_y = 1.0
            row_380B8.alignment = 'Expand'.upper()
            row_380B8.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_380B8.prop(bpy.context.scene.camera.data, 'show_passepartout', text='', icon_value=string_to_icon('OUTLINER_OB_CAMERA'), emboss=True)
            row_380B8.prop(bpy.context.scene.camera.data, 'passepartout_alpha', text='', icon_value=0, emboss=True)
            row_BFED7 = col_95FB8.row(heading='', align=True)
            row_BFED7.alert = False
            row_BFED7.enabled = True
            row_BFED7.active = True
            row_BFED7.use_property_split = False
            row_BFED7.use_property_decorate = False
            row_BFED7.scale_x = 1.0
            row_BFED7.scale_y = 1.0
            row_BFED7.alignment = 'Expand'.upper()
            row_BFED7.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            op = row_BFED7.operator('wm.reset_camera_rotation_02dbe', text='', icon_value=string_to_icon('LOOP_BACK'), emboss=True, depress=False)
            row_BFED7.prop(bpy.context.scene, 'sna_rotation_slider', text='', icon_value=0, emboss=True)
            grid_BA00D = col_95FB8.grid_flow(columns=2, row_major=False, even_columns=False, even_rows=False, align=True)
            grid_BA00D.enabled = True
            grid_BA00D.active = True
            grid_BA00D.use_property_split = False
            grid_BA00D.use_property_decorate = False
            grid_BA00D.alignment = 'Expand'.upper()
            grid_BA00D.scale_x = 1.0
            grid_BA00D.scale_y = 1.0
            if not True: grid_BA00D.operator_context = "EXEC_DEFAULT"
            
            grid_BA00D.operator('wm.mirror_camera_horizontally_861b9', text='X', icon_value=0, emboss=True, depress=False)
    #        grid_BA00D.prop('wm_mute_camera_action', text='', icon_value=string_to_icon('DECORATE_LOCKED'), emboss=True)
            grid_BA00D.operator('wm.mirror_camera_vertically_1fff5', text='Y', icon_value=0, emboss=True, depress=False)
            box_FF417.prop(bpy.context.scene, 'sna_rotation_shortcut', text='Rotation Shortcuts', icon_value=0, emboss=True)
class SNA_OT_Select_Active_Camera_81Ec7(bpy.types.Operator):
    bl_idname = "wm.select_active_camera_81ec7"
    bl_label = "Select Active Camera"
    bl_description = "Select the Active Camera for current scene (Scene Properties > Camera)"
    bl_options = {"REGISTER","UNDO", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.context.view_layer.objects.active = bpy.context.scene.camera
        bpy.ops.object.mode_set(mode='OBJECT')
        for i in bpy.data.objects:
            i.select_set(False)
        bpy.context.scene.camera.select_set(True)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
    

class SNA_OT_Mirror_Camera_Horizontally_861B9(bpy.types.Operator):
    bl_idname = "wm.mirror_camera_horizontally_861b9"
    bl_label = "Mirror Camera Horizontally"
    bl_description = "Invert X Scale"
    bl_options = {"REGISTER","UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

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


class SNA_OT_Mirror_Camera_Vertically_1Fff5(bpy.types.Operator):
    bl_idname = "wm.mirror_camera_vertically_1fff5"
    bl_label = "Mirror Camera Vertically"
    bl_description = "Invert Y Scale"
    bl_options = {"REGISTER","UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        cam = bpy.context.scene.camera
        if cam.scale.y == 1.0:
            cam.scale.y = -1.0
        else :
            cam.scale.y = 1.0
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Reset_Camera_Rotation_02Dbe(bpy.types.Operator):
    bl_idname = "wm.reset_camera_rotation_02dbe"
    bl_label = "Reset Camera Rotation"
    bl_description = "Reset Camera Rotation to 0"
    bl_options = {"REGISTER","UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.context.scene.sna_rotation_slider = 0.0
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)

class SNA_OT_Rotate_Clockwise_B155B(bpy.types.Operator):
    bl_idname = "wm.rotate_clockwise_b155b"
    bl_label = "Rotate Clockwise"
    bl_description = ""
    bl_options = {"REGISTER","UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        if bpy.context.scene.sna_rotation_shortcut:
            bpy.context.scene.sna_rotation_slider = float(bpy.context.scene.sna_rotation_slider - bpy.context.scene.sna_rotation_steps)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Rotate_Counter_Clockwise_Acaed(bpy.types.Operator):
    bl_idname = "wm.rotate_counter_clockwise_acaed"
    bl_label = "Rotate Counter Clockwise"
    bl_description = ""
    bl_options = {"REGISTER","UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        if bpy.context.scene.sna_rotation_shortcut:
            bpy.context.scene.sna_rotation_slider = float(bpy.context.scene.sna_rotation_slider + bpy.context.scene.sna_rotation_steps)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
    
def register():
#    bpy.utils.register_class(Mute_camera)
    bpy.types.Scene.sna_rotation_slider = bpy.props.FloatProperty(name='Rotation Slider', description='', default=0.0, subtype='NONE', unit='NONE', step=3, precision=3, update=sna_update_sna_rotation_slider_BF78B)
    bpy.types.Scene.sna_rotation_steps = bpy.props.FloatProperty(name='Rotation Steps', description='', default=0.05, subtype='NONE', unit='NONE', min=0.0, step=5, precision=2)
    bpy.utils.register_class(SNA_OT_Select_Active_Camera_81Ec7)
    bpy.utils.register_class(SNA_OT_Mirror_Camera_Horizontally_861B9)
    bpy.utils.register_class(SNA_OT_Mirror_Camera_Vertically_1Fff5)
    bpy.utils.register_class(SNA_OT_Reset_Camera_Rotation_02Dbe)
    bpy.utils.register_class(sna_add_to_view3d_pt_tools_active_63904)
#    bpy.types.VIEW3D_PT_tools_active.prepend(sna_add_to_view3d_pt_tools_active_63904)
    bpy.app.handlers.depsgraph_update_pre.append(depsgraph_update_pre_handler_172E3)
    bpy.utils.register_class(SNA_OT_Rotate_Clockwise_B155B)
    bpy.utils.register_class(SNA_OT_Rotate_Counter_Clockwise_Acaed)
    bpy.types.Scene.sna_rotation_shortcut = bpy.props.BoolProperty(name='Rotation Shortcut', description='', default=True)
    
    kc = bpy.context.window_manager.keyconfigs.addon
    km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
    kmi = km.keymap_items.new('wm.rotate_clockwise_b155b', 'PERIOD', 'PRESS',
        ctrl=False, alt=True, shift=False, repeat=True)
    addon_keymaps['E126D'] = (km, kmi)
    kc = bpy.context.window_manager.keyconfigs.addon
    km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
    kmi = km.keymap_items.new('wm.rotate_counter_clockwise_acaed', 'COMMA', 'PRESS',
        ctrl=False, alt=True, shift=False, repeat=True)
    addon_keymaps['F095F'] = (km, kmi)
    
def unregister():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    for km, kmi in addon_keymaps.values():
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
#    bpy.utils.unregister_class(Mute_camera)
    del bpy.types.Scene.sna_rotation_slider
    del bpy.types.Scene.sna_rotation_shortcut
    del bpy.types.Scene.sna_rotation_steps
    bpy.utils.unregister_class(SNA_OT_Select_Active_Camera_81Ec7)
    bpy.utils.unregister_class(SNA_OT_Mirror_Camera_Horizontally_861B9)
    bpy.utils.unregister_class(SNA_OT_Mirror_Camera_Vertically_1Fff5)
    bpy.utils.unregister_class(SNA_OT_Reset_Camera_Rotation_02Dbe)
    bpy.utils.unregister_class(sna_add_to_view3d_pt_tools_active_63904)
    bpy.types.VIEW3D_PT_tools_active.remove(sna_add_to_view3d_pt_tools_active_63904)
    bpy.app.handlers.depsgraph_update_pre.remove(depsgraph_update_pre_handler_172E3)

if __name__ == "__main__":
    register()
