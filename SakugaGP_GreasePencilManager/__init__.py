bl_info = {
    "name" : "SakugaGP - Grease Pencil Manager",
    "author" : "Sadewoo (Spikysaurus)", 
    "description" : "Grease Pencil Manager, Change Orders, Quick Opacity, Freeze Frames",
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
import bpy.utils.previews


def string_to_icon(value):
    if value in bpy.types.UILayout.bl_rna.functions["prop"].parameters["icon"].enum_items.keys():
        return bpy.types.UILayout.bl_rna.functions["prop"].parameters["icon"].enum_items[value].value
    return string_to_int(value)
    
selector = {'sna_default_opacity': 0.30000001192092896, 'sna_opacity_mesh_check': False, 'sna_opacity_gp_check': False, 'sna_opacity_ref_check': False, }


def sna_update_sna_brush_size_E295A(self, context):
    sna_updated_prop = self.sna_brush_size
    val = sna_updated_prop
    calc = val/400
    bpy.context.tool_settings.gpencil_paint.brush.unprojected_radius = calc


def sna_update_sna_rotation_slider_BF78B(self, context):
    sna_updated_prop = self.sna_rotation_slider
    bpy.data.objects[str(bpy.context.scene.camera.name)].rotation_euler.y = bpy.context.scene.sna_rotation_slider


def sna_update_sna_mute_camera_action_27A28(self, context):
    sna_updated_prop = self.sna_mute_camera_action
    bool = sna_updated_prop
    active = bpy.context.scene.camera
    action = active.animation_data.action
    for i in action.fcurves:
        i.mute = bool
        bpy.context.scene.render.fps


def sna_update_sna_object_list_EDFF0(self, context):
    sna_updated_prop = self.sna_object_list
    bpy.context.view_layer.objects.active = bpy.data.objects[sna_updated_prop]
    bpy.ops.object.mode_set('INVOKE_DEFAULT', mode='OBJECT')
    prev_context = bpy.context.area.type
    bpy.context.area.type = 'OUTLINER'
    bpy.ops.object.select_all('INVOKE_DEFAULT', action='DESELECT')
    bpy.context.area.type = prev_context
    bpy.data.objects[sna_updated_prop].select_set(state=True, )


def sna_update_sna_opacity_ref_6D10B(self, context):
    sna_updated_prop = self.sna_opacity_ref
    bpy.context.view_layer.objects.active.color[3] = sna_updated_prop


def sna_update_sna_opacity_mesh_E925E(self, context):
    sna_updated_prop = self.sna_opacity_mesh
    bpy.context.view_layer.objects.active.active_material.node_tree.nodes['sakugagp_opacity'].inputs[1].default_value = sna_updated_prop


def display_collection_id(uid, vars):
    id = f"coll_{uid}"
    for var in vars.keys():
        if var.startswith("i_"):
            id += f"_{var}_{vars[var]}"
    return id


class SNA_UL_display_collection_list_FECBF(bpy.types.UIList):

    def draw_item(self, context, layout, data, item_FECBF, icon, active_data, active_propname, index_FECBF):
        row = layout
        row_186E9 = layout.row(heading='', align=False)
        row_186E9.alert = False
        row_186E9.enabled = True
        row_186E9.active = True
        row_186E9.use_property_split = False
        row_186E9.use_property_decorate = False
        row_186E9.scale_x = 1.0
        row_186E9.scale_y = 1.0
        row_186E9.alignment = 'Expand'.upper()
        row_186E9.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        if item_FECBF.type == 'MESH':
            row_186E9.label(text='', icon_value=string_to_icon('OUTLINER_OB_MESH'))
        else:
            row_186E9.label(text='', icon_value=string_to_icon('OUTLINER_OB_GREASEPENCIL'))
        row_186E9.prop(item_FECBF, 'name', text='', icon_value=0, emboss=False)
        row_7915F = layout.row(heading='', align=True)
        row_7915F.alert = False
        row_7915F.enabled = True
        row_7915F.active = True
        row_7915F.use_property_split = False
        row_7915F.use_property_decorate = False
        row_7915F.scale_x = 1.0
        row_7915F.scale_y = 1.0
        row_7915F.alignment = 'Left'.upper()
        row_7915F.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_7915F.label(text=str(int(bpy.data.objects[str(item_FECBF.name)].location.y * 1000.0)), icon_value=0)

    def filter_items(self, context, data, propname):
        flt_flags = []
        for item in getattr(data, propname):
            if not self.filter_name or self.filter_name.lower() in item.name.lower():
                if sna_filter_gp_2AA1B(item):
                    flt_flags.append(self.bitflag_filter_item)
                else:
                    flt_flags.append(0)
            else:
                flt_flags.append(0)
        return flt_flags, []

def sna_filter_gp_2AA1B(Input):
    Input = Input
    Mesh = bpy.context.scene.sna_include_mesh_objects
    Output = None
    if Input == None: pass
    else:
        string = str(Input.name)  
        index = string.find('#')  
        if index != -1: pass
        else :
            if Mesh == True :
                if Input.type == 'GREASEPENCIL' or Input.type == 'MESH' :
                    Output = True
                else:
                    Output = False
            else :
                if Input.type == 'GREASEPENCIL':
                    Output = True
                else:
                    Output = False
    return Output


class SNA_OT_Enable_Grease_Pencil_Opacity_D52Eb(bpy.types.Operator):
    bl_idname = "wm.enable_grease_pencil_opacity_d52eb"
    bl_label = "Enable Grease Pencil Opacity"
    bl_description = "Add Opacity Modifier to Active Grease Pencil Object"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):

        default_opacity = bpy.context.scene.sna_opacity_default
        obj = bpy.context.active_object
        # Explicitly check if the modifier 'sakugagp_opacity' exists in the active object's modifiers
        modifier_exists = "sakugagp_opacity" in [mod.name for mod in obj.modifiers]
        if not modifier_exists:
        #    # Only create a new modifier if it does not exist
            if obj and obj.type =='GREASEPENCIL':
                op=obj.modifiers.new(name='sakugagp_opacity',type='GREASE_PENCIL_OPACITY')
                op.color_factor = default_opacity
        else : pass
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


@persistent
def depsgraph_update_pre_handler_02B43(dummy):
    node_found = None
    if bpy.context.active_object == None : pass
    else:
        if bpy.context.active_object.type == 'MESH':
            if bpy.context.active_object.active_material == None:
                pass
            else:
                mat_name = bpy.context.active_object.active_material.name
                mat = bpy.data.materials[mat_name]
                if mat.use_nodes:
                    ntree = mat.node_tree
                    node = ntree.nodes.get("sakugagp_opacity", None)
                    if node is not None:
                        node_found = True
                    else:
                        node_found = False
                else: pass
        else: pass
    #print(bpy.data.objects['Plane'].active_material.name)
    selector['sna_opacity_mesh_check'] = node_found


class SNA_OT_Enable_Image_Mesh_Plane_Opacity_De052(bpy.types.Operator):
    bl_idname = "wm.enable_image_mesh_plane_opacity_de052"
    bl_label = "Enable Image Mesh Plane Opacity"
    bl_description = "Add alpha slider to Image Mesh Plane Object"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        obj_name = bpy.context.object.name
        mat_name = bpy.context.active_object.active_material.name
        mat = (bpy.data.materials.get(mat_name))
        if mat.use_nodes:
            if obj_name == mat_name :
                mat.blend_method = "BLEND"
                nodes = mat.node_tree.nodes
                links = mat.node_tree.links
                image_texture_node = nodes.get("Image Texture")
                math_node = mat.node_tree.nodes.new('ShaderNodeMath')
                math_node.operation = 'MULTIPLY'
                math_node.name = "sakugagp_opacity"
                math_node.label = "sakugagp_opacity"
                ntree = mat.node_tree
                node_bsdf = ntree.nodes.get("Principled BSDF", None)
                node_mix = ntree.nodes.get("Mix Shader", None)
                if node_bsdf is not None:
                    bsdf_shader_node = nodes.get("Principled BSDF")
                    links.new(image_texture_node.outputs['Alpha'], math_node.inputs[0])
                    links.new(math_node.outputs[0], bsdf_shader_node.inputs['Alpha'])
                elif node_mix is not None:
                    mix_shader_node = nodes.get("Mix Shader")
                    links.new(image_texture_node.outputs['Alpha'], math_node.inputs[0])
                    links.new(math_node.outputs[0], mix_shader_node.inputs['Fac'])
        else: pass
        bpy.context.scene.sna_opacity_mesh = bpy.context.scene.sna_opacity_default
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Disable_Image_Mesh_Plane_Opacity_E26A2(bpy.types.Operator):
    bl_idname = "wm.disable_image_mesh_plane_opacity_e26a2"
    bl_label = "Disable Image Mesh Plane Opacity"
    bl_description = "Remove alpha slider from Image Mesh Plane Object"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        node_found = False
        obj_name = bpy.context.object.name
        mat_name = bpy.context.active_object.active_material.name
        mat = bpy.data.materials[mat_name]
        if mat.use_nodes:
            if obj_name == mat_name :
                ntree = mat.node_tree
                node = ntree.nodes.get("sakugagp_opacity", None)
                if node is not None:
                    node_found = True
                    mat.node_tree.nodes.remove(node)
                    nodes = mat.node_tree.nodes
                    links = mat.node_tree.links
                    image_texture_node = nodes.get("Image Texture")
                    if mat.use_nodes:
                        ntree = mat.node_tree
                        node_bsdf = ntree.nodes.get("Principled BSDF", None)
                        node_mix = ntree.nodes.get("Mix Shader", None)
                        if node_bsdf is not None:
                            for link in node_bsdf.inputs[4].links:
                                mat.node_tree.links.remove(link)
        #                    bsdf_shader_node = nodes.get("Principled BSDF")
        #                    links.new(image_texture_node.outputs['Alpha'], bsdf_shader_node.inputs['Alpha'])
                        elif node_mix is not None:
                            node_mix.inputs[0].default_value = 1
                            for link in node_mix.inputs[0].links:
                                mat.node_tree.links.remove(link)
        #                    mix_shader_node = nodes.get("Mix Shader")
        #                    links.new(image_texture_node.outputs['Alpha'], mix_shader_node.inputs['Fac']) 
                else:
                    pass
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


@persistent
def depsgraph_update_pre_handler_697C5(dummy):
    modifier_found = None
    if bpy.context.active_object == None : pass
    else:
        if bpy.context.active_object.type == 'GREASEPENCIL':
            active_obj = bpy.context.active_object
            # Explicitly check if the modifier 'sakugagp_opacity' exists in the active object's modifiers
            modifier_exists = "sakugagp_opacity" in [mod.name for mod in active_obj.modifiers]
            if not modifier_exists:
                modifier_found = False
            else : 
                modifier_found = True
        else: pass
    selector['sna_opacity_gp_check'] = modifier_found


class SNA_OT_Disable_Gp_Opacity_7E22B(bpy.types.Operator):
    bl_idname = "wm.disable_gp_opacity_7e22b"
    bl_label = "Disable GP Opacity"
    bl_description = "Remove Opacity Modifier from Active Grease Pencil Object"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):

        default_opacity = None
        active_obj = bpy.context.active_object
        # Explicitly check if the modifier 'sakugagp_opacity' exists in the active object's modifiers
        modifier_exists = "sakugagp_opacity" in [mod.name for mod in active_obj.modifiers]
        if not modifier_exists:
            # Only create a new modifier if it does not exist
            pass
        else : 
            active_obj.modifiers.remove(active_obj.modifiers['sakugagp_opacity'])
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Bring_Object_Forward_E16E7(bpy.types.Operator):
    bl_idname = "wm.bring_object_forward_e16e7"
    bl_label = "Bring Object Forward"
    bl_description = "Y - 0.002"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        if bpy.context.active_object is None :
            self.report({'ERROR'}, "Select a object! if object is hidden, unhide it")
        else :
            bpy.context.active_object.location.y -= 0.002
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Bring_Object_Backward_Aad11(bpy.types.Operator):
    bl_idname = "wm.bring_object_backward_aad11"
    bl_label = "Bring Object Backward"
    bl_description = "Y + 0.002"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        if bpy.context.active_object is None :
            self.report({'ERROR'}, "Select a object! if object is hidden, unhide it")
        else :
            bpy.context.active_object.location.y += 0.002
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Hide_From_List_05F1A(bpy.types.Operator):
    bl_idname = "wm.hide_from_list_05f1a"
    bl_label = "Hide from list"
    bl_description = "Hide selected object from list by inserting ' # ' to its name. Remove the ' # '  by renaming it from outliner to bring it back to the list"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        Input = None
        Input = bpy.context.active_object
        Input.name = "#" + str(Input.name)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_PT_SELECTOR_MENU_0FA79(bpy.types.Panel):
    bl_label = 'Selector Menu'
    bl_idname = 'SNA_PT_SELECTOR_MENU_0FA79'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_context = ''
    bl_order = 0
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        box_BBFDA = layout.box()
        box_BBFDA.alert = False
        box_BBFDA.enabled = True
        box_BBFDA.active = True
        box_BBFDA.use_property_split = False
        box_BBFDA.use_property_decorate = False
        box_BBFDA.alignment = 'Expand'.upper()
        box_BBFDA.scale_x = 1.0
        box_BBFDA.scale_y = 1.0
        if not True: box_BBFDA.operator_context = "EXEC_DEFAULT"
        col_FFE24 = box_BBFDA.column(heading='', align=True)
        col_FFE24.alert = False
        col_FFE24.enabled = True
        col_FFE24.active = True
        col_FFE24.use_property_split = False
        col_FFE24.use_property_decorate = False
        col_FFE24.scale_x = 1.0
        col_FFE24.scale_y = 1.0
        col_FFE24.alignment = 'Expand'.upper()
        col_FFE24.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_FFE24.label(text='Filter :', icon_value=0)
        col_FFE24.prop(bpy.context.scene, 'sna_include_mesh_objects', text='Include Mesh Objects', icon_value=string_to_icon('OUTLINER_OB_MESH'), emboss=True)
        op = col_FFE24.operator('wm.hide_from_list_05f1a', text='Exclude Object from the list', icon_value=string_to_icon('GRID'), emboss=True, depress=False)


@persistent
def depsgraph_update_pre_handler_D3288(dummy):
    Variable = None
    has_image = None
    obj = bpy.context.active_object
    if obj.type == "EMPTY":
        if obj.empty_display_type == "IMAGE":
            has_image = True
        else:
            has_image = False
    else: pass
    selector['sna_opacity_ref_check'] = has_image


class SNA_OT_Enable_Ref_Opacity_5375E(bpy.types.Operator):
    bl_idname = "wm.enable_ref_opacity_5375e"
    bl_label = "Enable Ref Opacity"
    bl_description = "Enable opacity to Image Reference"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        obj = bpy.context.active_object
        obj.use_empty_image_alpha = True
        bpy.context.scene.sna_opacity_ref = bpy.context.scene.sna_opacity_default
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Disable_Ref_Opacity_Ddd03(bpy.types.Operator):
    bl_idname = "wm.disable_ref_opacity_ddd03"
    bl_label = "Disable Ref Opacity"
    bl_description = "Disable opacity to Image Reference"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):

        default_opacity = None
        obj = bpy.context.object
        obj.use_empty_image_alpha = False
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_PT_SELECTOR_C3563(bpy.types.Panel):
    bl_label = 'Grease Pencil Manager'
    bl_idname = 'SNA_PT_SELECTOR_C3563'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = 'SakugaGP'
    bl_order = 0
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        col_E5D76 = layout.column(heading='', align=False)
        col_E5D76.alert = False
        col_E5D76.enabled = True
        col_E5D76.active = True
        col_E5D76.use_property_split = False
        col_E5D76.use_property_decorate = False
        col_E5D76.scale_x = 1.0
        col_E5D76.scale_y = 1.0
        col_E5D76.alignment = 'Expand'.upper()
        col_E5D76.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        if (selector['sna_opacity_ref_check'] and bpy.context.view_layer.objects.active.use_empty_image_alpha):
            col_22F40 = col_E5D76.column(heading='', align=False)
            col_22F40.alert = False
            col_22F40.enabled = True
            col_22F40.active = True
            col_22F40.use_property_split = False
            col_22F40.use_property_decorate = False
            col_22F40.scale_x = 1.0
            col_22F40.scale_y = 1.0
            col_22F40.alignment = 'Expand'.upper()
            col_22F40.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            col_22F40.prop(bpy.context.scene, 'sna_opacity_ref', text='Opacity', icon_value=0, emboss=True)
            col_22F40.prop(bpy.context.view_layer.objects.active, 'color', text='', icon_value=0, emboss=True)
        else:
            if selector['sna_opacity_gp_check']:
                col_E5D76.prop(bpy.context.view_layer.objects.active.modifiers['sakugagp_opacity'], 'color_factor', text='Opacity', icon_value=0, emboss=True)
            else:
                if selector['sna_opacity_mesh_check']:
                    col_E5D76.prop(bpy.context.scene, 'sna_opacity_mesh', text='Opacity', icon_value=0, emboss=True)
        row_D48B0 = col_E5D76.row(heading='', align=True)
        row_D48B0.alert = False
        row_D48B0.enabled = True
        row_D48B0.active = True
        row_D48B0.use_property_split = False
        row_D48B0.use_property_decorate = False
        row_D48B0.scale_x = 1.0
        row_D48B0.scale_y = 1.0
        row_D48B0.alignment = 'Expand'.upper()
        row_D48B0.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        coll_id = display_collection_id('FECBF', locals())
        row_D48B0.template_list('SNA_UL_display_collection_list_FECBF', coll_id, bpy.data, 'objects', bpy.context.scene, 'sna_object_list', rows=0)
        col_B97BA = row_D48B0.column(heading='', align=False)
        col_B97BA.alert = False
        col_B97BA.enabled = True
        col_B97BA.active = True
        col_B97BA.use_property_split = False
        col_B97BA.use_property_decorate = False
        col_B97BA.scale_x = 1.0
        col_B97BA.scale_y = 1.0
        col_B97BA.alignment = 'Expand'.upper()
        col_B97BA.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_B97BA.popover('SNA_PT_SELECTOR_MENU_0FA79', text='', icon_value=string_to_icon('COLLAPSEMENU'))
        if (bpy.context.view_layer.objects.active == None):
            pass
        else:
            col_B2F92 = col_B97BA.column(heading='', align=False)
            col_B2F92.alert = False
            col_B2F92.enabled = True
            col_B2F92.active = True
            col_B2F92.use_property_split = False
            col_B2F92.use_property_decorate = False
            col_B2F92.scale_x = 1.0
            col_B2F92.scale_y = 1.0
            col_B2F92.alignment = 'Expand'.upper()
            col_B2F92.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            col_46D9A = col_B2F92.column(heading='', align=True)
            col_46D9A.alert = False
            col_46D9A.enabled = True
            col_46D9A.active = True
            col_46D9A.use_property_split = False
            col_46D9A.use_property_decorate = False
            col_46D9A.scale_x = 1.0
            col_46D9A.scale_y = 1.0
            col_46D9A.alignment = 'Expand'.upper()
            col_46D9A.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            op = col_46D9A.operator('wm.bring_object_forward_e16e7', text='', icon_value=string_to_icon('TRIA_UP'), emboss=True, depress=False)
            op = col_46D9A.operator('wm.bring_object_backward_aad11', text='', icon_value=string_to_icon('TRIA_DOWN'), emboss=True, depress=False)
            if (bpy.context.view_layer.objects.active == None):
                pass
            else:
                if bpy.context.view_layer.objects.active.type == 'CAMERA':
                    pass
                else:
                    if selector['sna_opacity_ref_check']:
                        if bpy.context.view_layer.objects.active.use_empty_image_alpha:
                            op = col_B2F92.operator('wm.disable_ref_opacity_ddd03', text='', icon_value=string_to_icon('MOD_OPACITY'), emboss=True, depress=True)
                        else:
                            op = col_B2F92.operator('wm.enable_ref_opacity_5375e', text='', icon_value=string_to_icon('MOD_OPACITY'), emboss=True, depress=False)
                    else:
                        if bpy.context.view_layer.objects.active.type == 'MESH':
                            if selector['sna_opacity_mesh_check']:
                                op = col_B2F92.operator('wm.disable_image_mesh_plane_opacity_e26a2', text='', icon_value=string_to_icon('MOD_OPACITY'), emboss=True, depress=True)
                            else:
                                op = col_B2F92.operator('wm.enable_image_mesh_plane_opacity_de052', text='', icon_value=string_to_icon('MOD_OPACITY'), emboss=True, depress=False)
                        else:
                            if selector['sna_opacity_gp_check']:
                                op = col_B2F92.operator('wm.disable_gp_opacity_7e22b', text='', icon_value=string_to_icon('MOD_OPACITY'), emboss=True, depress=True)
                            else:
                                op = col_B2F92.operator('wm.enable_grease_pencil_opacity_d52eb', text='', icon_value=string_to_icon('MOD_OPACITY'), emboss=True, depress=False)
        if (bpy.context.view_layer.objects.active == None):
            pass
        else:
            row_0E0EF = col_E5D76.row(heading='', align=True)
            row_0E0EF.alert = False
            row_0E0EF.enabled = True
            row_0E0EF.active = True
            row_0E0EF.use_property_split = False
            row_0E0EF.use_property_decorate = False
            row_0E0EF.scale_x = 1.0
            row_0E0EF.scale_y = 1.0
            row_0E0EF.alignment = 'Expand'.upper()
            row_0E0EF.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_0E0EF.label(text='Freeze Frame :', icon_value=0)
            op = row_0E0EF.operator('wm.freeze_red_ccc81', text='', icon_value=string_to_icon('STRIP_COLOR_01'), emboss=True, depress=False)
            op = row_0E0EF.operator('wm.freeze_green_7f385', text='', icon_value=string_to_icon('STRIP_COLOR_03'), emboss=True, depress=False)
            op = row_0E0EF.operator('wm.freeze_blue_49961', text='', icon_value=string_to_icon('STRIP_COLOR_06'), emboss=True, depress=False)


class SNA_OT_Freeze_Red_Ccc81(bpy.types.Operator):
    bl_idname = "wm.freeze_red_ccc81"
    bl_label = "Freeze Red"
    bl_description = "Duplicate and Freeze Current Object's Frame"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        x = False
        if bpy.context.active_object:
            bpy.ops.object.mode_set(mode='OBJECT')
            if bpy.context.active_object.type == "GREASEPENCIL":
                bpy.ops.object.duplicate_move_linked(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_elements":{'INCREMENT'}, "use_snap_project":False, "snap_target":'CLOSEST', "use_snap_self":True, "use_snap_edit":True, "use_snap_nonedit":True, "use_snap_selectable":False, "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "use_duplicated_keyframes":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False, "translate_origin":False})
                x = True
            else:
                pass
            if x == True:
                obj = bpy.context.active_object
                sc = bpy.context.scene
                op=obj.modifiers.new(name='sakugagp_time_offset_freeze',type='GREASE_PENCIL_TIME')
                op.mode = "FIX"
                op.offset = sc.frame_current
                opB=obj.modifiers.new(name='sakugagp_tint_freeze',type='GREASE_PENCIL_TINT')
                opB.factor = 1.0
                opB.color = (1,0,0)
        else:
           pass

        default_opacity = bpy.context.scene.sna_opacity_default
        obj = bpy.context.active_object
        # Explicitly check if the modifier 'sakugagp_opacity' exists in the active object's modifiers
        modifier_exists = "sakugagp_opacity" in [mod.name for mod in obj.modifiers]
        if not modifier_exists:
        #    # Only create a new modifier if it does not exist
            if obj and obj.type =='GREASEPENCIL':
                op=obj.modifiers.new(name='sakugagp_opacity',type='GREASE_PENCIL_OPACITY')
                op.color_factor = default_opacity
        else : pass
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Freeze_Green_7F385(bpy.types.Operator):
    bl_idname = "wm.freeze_green_7f385"
    bl_label = "Freeze Green"
    bl_description = "Duplicate and Freeze Current Object's Frame"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        x = False
        if bpy.context.active_object:
            bpy.ops.object.mode_set(mode='OBJECT')
            if bpy.context.active_object.type == "GREASEPENCIL":
                bpy.ops.object.duplicate_move_linked(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_elements":{'INCREMENT'}, "use_snap_project":False, "snap_target":'CLOSEST', "use_snap_self":True, "use_snap_edit":True, "use_snap_nonedit":True, "use_snap_selectable":False, "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "use_duplicated_keyframes":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False, "translate_origin":False})
                x = True
            else:
                pass
            if x == True:
                obj = bpy.context.active_object
                sc = bpy.context.scene
                op=obj.modifiers.new(name='sakugagp_time_offset_freeze',type='GREASE_PENCIL_TIME')
                op.mode = "FIX"
                op.offset = sc.frame_current
                opB=obj.modifiers.new(name='sakugagp_tint_freeze',type='GREASE_PENCIL_TINT')
                opB.factor = 1.0
                opB.color = (0,1,0)
        else:
           pass

        default_opacity = bpy.context.scene.sna_opacity_default
        obj = bpy.context.active_object
        # Explicitly check if the modifier 'sakugagp_opacity' exists in the active object's modifiers
        modifier_exists = "sakugagp_opacity" in [mod.name for mod in obj.modifiers]
        if not modifier_exists:
        #    # Only create a new modifier if it does not exist
            if obj and obj.type =='GREASEPENCIL':
                op=obj.modifiers.new(name='sakugagp_opacity',type='GREASE_PENCIL_OPACITY')
                op.color_factor = default_opacity
        else : pass
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Freeze_Blue_49961(bpy.types.Operator):
    bl_idname = "wm.freeze_blue_49961"
    bl_label = "Freeze Blue"
    bl_description = "Duplicate and Freeze Current Object's Frame"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        x = False
        if bpy.context.active_object:
            bpy.ops.object.mode_set(mode='OBJECT')
            if bpy.context.active_object.type == "GREASEPENCIL":
                bpy.ops.object.duplicate_move_linked(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_elements":{'INCREMENT'}, "use_snap_project":False, "snap_target":'CLOSEST', "use_snap_self":True, "use_snap_edit":True, "use_snap_nonedit":True, "use_snap_selectable":False, "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "use_duplicated_keyframes":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False, "translate_origin":False})
                x = True
            else:
                pass
            if x == True:
                obj = bpy.context.active_object
                sc = bpy.context.scene
                op=obj.modifiers.new(name='sakugagp_time_offset_freeze',type='GREASE_PENCIL_TIME')
                op.mode = "FIX"
                op.offset = sc.frame_current
                opB=obj.modifiers.new(name='sakugagp_tint_freeze',type='GREASE_PENCIL_TINT')
                opB.factor = 1.0
                opB.color = (0,0,1)
        else:
           pass

        default_opacity = bpy.context.scene.sna_opacity_default
        obj = bpy.context.active_object
        # Explicitly check if the modifier 'sakugagp_opacity' exists in the active object's modifiers
        modifier_exists = "sakugagp_opacity" in [mod.name for mod in obj.modifiers]
        if not modifier_exists:
        #    # Only create a new modifier if it does not exist
            if obj and obj.type =='GREASEPENCIL':
                op=obj.modifiers.new(name='sakugagp_opacity',type='GREASE_PENCIL_OPACITY')
                op.color_factor = default_opacity
        else : pass
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
    
def register():
    bpy.types.Scene.sna_object_list = bpy.props.IntProperty(name='Object List', description='', default=0, subtype='NONE', update=sna_update_sna_object_list_EDFF0)
    bpy.types.Scene.sna_include_mesh_objects = bpy.props.BoolProperty(name='Include Mesh Objects', description='', default=False)
    bpy.types.Scene.sna_opacity_ref = bpy.props.FloatProperty(name='opacity_ref', description='', default=0.0, subtype='NONE', unit='NONE', min=0.0, max=1.0, step=3, precision=2, update=sna_update_sna_opacity_ref_6D10B)
    bpy.types.Scene.sna_opacity_mesh = bpy.props.FloatProperty(name='opacity_mesh', description='', default=0.0, subtype='NONE', unit='NONE', min=0.0, max=1.0, step=3, precision=2, update=sna_update_sna_opacity_mesh_E925E)
    bpy.types.Scene.sna_opacity_default = bpy.props.FloatProperty(name='opacity_default', description='', default=0.30000001192092896, subtype='NONE', unit='NONE', min=0.0, max=1.0, step=5, precision=2)
    bpy.utils.register_class(SNA_OT_Enable_Grease_Pencil_Opacity_D52Eb)
    bpy.app.handlers.depsgraph_update_pre.append(depsgraph_update_pre_handler_02B43)
    bpy.utils.register_class(SNA_OT_Enable_Image_Mesh_Plane_Opacity_De052)
    bpy.utils.register_class(SNA_OT_Disable_Image_Mesh_Plane_Opacity_E26A2)
    bpy.app.handlers.depsgraph_update_pre.append(depsgraph_update_pre_handler_697C5)
    bpy.utils.register_class(SNA_OT_Disable_Gp_Opacity_7E22B)
    bpy.utils.register_class(SNA_OT_Bring_Object_Forward_E16E7)
    bpy.utils.register_class(SNA_OT_Bring_Object_Backward_Aad11)
    bpy.utils.register_class(SNA_OT_Hide_From_List_05F1A)
    bpy.utils.register_class(SNA_PT_SELECTOR_MENU_0FA79)
    bpy.app.handlers.depsgraph_update_pre.append(depsgraph_update_pre_handler_D3288)
    bpy.utils.register_class(SNA_OT_Enable_Ref_Opacity_5375E)
    bpy.utils.register_class(SNA_OT_Disable_Ref_Opacity_Ddd03)
    bpy.utils.register_class(SNA_PT_SELECTOR_C3563)
    bpy.utils.register_class(SNA_UL_display_collection_list_FECBF)
    bpy.utils.register_class(SNA_OT_Freeze_Red_Ccc81)
    bpy.utils.register_class(SNA_OT_Freeze_Green_7F385)
    bpy.utils.register_class(SNA_OT_Freeze_Blue_49961)
def unregister():
    del bpy.types.Scene.sna_opacity_default
    del bpy.types.Scene.sna_opacity_mesh
    del bpy.types.Scene.sna_opacity_ref
    del bpy.types.Scene.sna_include_mesh_objects
    del bpy.types.Scene.sna_object_list
    bpy.utils.unregister_class(SNA_OT_Enable_Grease_Pencil_Opacity_D52Eb)
    bpy.app.handlers.depsgraph_update_pre.remove(depsgraph_update_pre_handler_02B43)
    bpy.utils.unregister_class(SNA_OT_Enable_Image_Mesh_Plane_Opacity_De052)
    bpy.utils.unregister_class(SNA_OT_Disable_Image_Mesh_Plane_Opacity_E26A2)
    bpy.app.handlers.depsgraph_update_pre.remove(depsgraph_update_pre_handler_697C5)
    bpy.utils.unregister_class(SNA_OT_Disable_Gp_Opacity_7E22B)
    bpy.utils.unregister_class(SNA_OT_Bring_Object_Forward_E16E7)
    bpy.utils.unregister_class(SNA_OT_Bring_Object_Backward_Aad11)
    bpy.utils.unregister_class(SNA_OT_Hide_From_List_05F1A)
    bpy.utils.unregister_class(SNA_PT_SELECTOR_MENU_0FA79)
    bpy.app.handlers.depsgraph_update_pre.remove(depsgraph_update_pre_handler_D3288)
    bpy.utils.unregister_class(SNA_OT_Enable_Ref_Opacity_5375E)
    bpy.utils.unregister_class(SNA_OT_Disable_Ref_Opacity_Ddd03)
    bpy.utils.unregister_class(SNA_PT_SELECTOR_C3563)
    bpy.utils.unregister_class(SNA_UL_display_collection_list_FECBF)
    bpy.utils.unregister_class(SNA_OT_Freeze_Red_Ccc81)
    bpy.utils.unregister_class(SNA_OT_Freeze_Green_7F385)
    bpy.utils.unregister_class(SNA_OT_Freeze_Blue_49961)
if __name__ == "__main__":
    register()