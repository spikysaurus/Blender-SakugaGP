bl_info = {
    "name" : "SakugaGP - Manager",
    "author" : "Sadewoo (Spikysaurus)", 
    "description" : "Object Manager, Change Orders, Quick Opacity, Freeze Frames",
    "blender" : (5, 0, 0),
    "version" : (0, 1, 1),
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
    
selector = {'sna_default_opacity': 0.3, 'sna_opacity_mesh_check': False, 'sna_opacity_gp_check': False }


def sna_update_sna_opacity_ref(self, context):
    sna_updated_prop = self.sna_opacity_ref
    bpy.context.view_layer.objects.active.color[3] = sna_updated_prop


def sna_update_sna_opacity_mesh(self, context):
    sna_updated_prop = self.sna_opacity_mesh
    bpy.context.view_layer.objects.active.active_material.node_tree.nodes['sakugagp_opacity'].inputs[1].default_value = sna_updated_prop


def display_collection_id(uid, vars):
    id = f"coll_{uid}"
    for var in vars.keys():
        if var.startswith("i_"):
            id += f"_{var}_{vars[var]}"
    return id

def sna_update_sna_object_list_EDFF0(self, context):
    sna_updated_prop = self.sna_object_list
    bpy.context.view_layer.objects.active = bpy.data.objects[sna_updated_prop]
    bpy.ops.object.mode_set('INVOKE_DEFAULT', mode='OBJECT')
    prev_context = bpy.context.area.type
    bpy.context.area.type = 'OUTLINER'
    bpy.ops.object.select_all('INVOKE_DEFAULT', action='DESELECT')
    bpy.context.area.type = prev_context
    bpy.data.objects[sna_updated_prop].select_set(state=True, )


class SNA_UL_display_collection_list(bpy.types.UIList):
    sort_by_y: bpy.props.BoolProperty(
        name="Sort by Y",
        description="Enable sorting by Y location value",
        default=False
    )

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # Calculate Y location value
        y_val = int(bpy.data.objects[item.name].location.y * 1000.0)

        # Format as 3 digits with leading zeros
        y_str = str(y_val).zfill(4)[-4:]
#        y_str = str(y_val)

        # Split row into two parts (Y value and Name)
        split = layout.split(factor=0.6, align=True)

        if self.sort_by_y:
            # Show Y value first, then name
            split.label(text=y_str)
            col = split.column(align=True)
            col.alignment = 'LEFT'
            col.prop(item, 'name', text='', emboss=False)
        else:
            # Default: name first, then Y value
            col = split.column(align=True)
            col.alignment = 'LEFT'
            col.prop(item, 'name', text='', emboss=False)
            split.label(text=y_str)



    def filter_items(self, context, data, propname):
        items = getattr(data, propname)

        # Filtering
        flt_flags = [
            (self.bitflag_filter_item if (not self.filter_name or self.filter_name.lower() in item.name.lower()) and sna_filter_gp(item) else 0)
            for item in items
        ]

        # Sorting
        flt_neworder = []
        if self.sort_by_y:
            flt_neworder = sorted(
                range(len(items)),
                key=lambda i: bpy.data.objects[items[i].name].location.y
            )

        return flt_flags, flt_neworder

def sna_filter_gp(Input):
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

@persistent
def depsgraph_update_pre_handler(dummy):
    obj = bpy.context.active_object

    if obj is None:
        return

    # --- Mesh check ---
    if obj.type == 'MESH' and obj.active_material:
        mat = obj.active_material
        engine = bpy.context.scene.render.engine
        if engine == 'BLENDER_EEVEE' or engine == 'CYCLES':
            if mat.use_nodes:
                node = mat.node_tree.nodes.get("sakugagp_opacity")
                selector['sna_opacity_mesh_check'] = node is not None
                
        if engine == 'BLENDER_WORKBENCH':
            # True if alpha channel is less than 1.0
            selector['sna_opacity_mesh_check'] = (mat.diffuse_color[3] < 1.0)

                
    # --- Grease Pencil check ---
    elif obj.type == 'GREASEPENCIL':
        selector['sna_opacity_gp_check'] = "sakugagp_opacity" in [mod.name for mod in obj.modifiers]
    
class SNA_OT_Enable_Ref_Opacity(bpy.types.Operator):
    bl_idname = "wm.enable_ref_opacity"
    bl_label = "Enable Ref Opacity"
    bl_description = "Enable opacity to Image Reference"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = bpy.context.active_object
        obj.use_empty_image_alpha = True
        bpy.context.scene.sna_opacity_ref = bpy.context.scene.sna_opacity_default
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)

class SNA_OT_Disable_Ref_Opacity(bpy.types.Operator):
    bl_idname = "wm.disable_ref_opacity"
    bl_label = "Disable Ref Opacity"
    bl_description = "Disable opacity to Image Reference"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        default_opacity = None
        obj = bpy.context.object
        obj.use_empty_image_alpha = False
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)    
class SNA_OT_Enable_Grease_Pencil_Opacity(bpy.types.Operator):
    bl_idname = "wm.enable_grease_pencil_opacity"
    bl_label = "Enable Grease Pencil Opacity"
    bl_description = "Add Opacity Modifier to Active Grease Pencil Object"
    bl_options = {"REGISTER", "UNDO"}

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

class SNA_OT_Disable_Gp_Opacity(bpy.types.Operator):
    bl_idname = "wm.disable_gp_opacity"
    bl_label = "Disable GP Opacity"
    bl_description = "Remove Opacity Modifier from Active Grease Pencil Object"
    bl_options = {"REGISTER", "UNDO"}

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

class SNA_OT_Enable_Image_Mesh_Plane_Opacity(bpy.types.Operator):
    bl_idname = "wm.enable_image_mesh_plane_opacity"
    bl_label = "Enable Image Mesh Plane Opacity"
    bl_description = "Add alpha slider to Image Mesh Plane Object"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = context.object
        mat = obj.active_material
        if mat and mat.use_nodes and obj.name == mat.name:
            mat.blend_method = "BLEND"
            nodes, links = mat.node_tree.nodes, mat.node_tree.links
            tex_node = nodes.get("Image Texture")
            math_node = nodes.new('ShaderNodeMath')
            math_node.operation = 'MULTIPLY'
            math_node.name = math_node.label = "sakugagp_opacity"

            bsdf = nodes.get("Principled BSDF")
            mix = nodes.get("Mix Shader")
            if tex_node:
                if bsdf:
                    links.new(tex_node.outputs['Alpha'], math_node.inputs[0])
                    links.new(math_node.outputs[0], bsdf.inputs['Alpha'])
                elif mix:
                    links.new(tex_node.outputs['Alpha'], math_node.inputs[0])
                    links.new(math_node.outputs[0], mix.inputs['Fac'])

        context.scene.sna_opacity_mesh = context.scene.sna_opacity_default
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)

class SNA_OT_Disable_Image_Mesh_Plane_Opacity(bpy.types.Operator):
    bl_idname = "wm.disable_image_mesh_plane_opacity"
    bl_label = "Disable Image Mesh Plane Opacity"
    bl_description = "Remove alpha slider from Image Mesh Plane Object"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = context.object
        mat = obj.active_material
        if mat and mat.use_nodes and obj.name == mat.name:
            ntree = mat.node_tree
            node = ntree.nodes.get("sakugagp_opacity")
            if node:
                ntree.nodes.remove(node)
                bsdf, mix = ntree.nodes.get("Principled BSDF"), ntree.nodes.get("Mix Shader")
                if bsdf:
                    for link in bsdf.inputs['Alpha'].links:
                        ntree.links.remove(link)
                elif mix:
                    mix.inputs[0].default_value = 1
                    for link in mix.inputs[0].links:
                        ntree.links.remove(link)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)

class SNA_OT_Enable_Image_Mesh_Plane_Opacity_Workbench(bpy.types.Operator):
    bl_idname = "wm.enable_image_mesh_plane_opacity_workbench"
    bl_label = "Enable Image Mesh Plane Opacity (Workbench)"
    bl_description = "Add alpha slider to Image Mesh Plane Object"
    bl_options = {"REGISTER", "UNDO"}
    
    def execute(self, context):
        obj = context.object
        mat = obj.active_material
        mat.diffuse_color[3] = context.scene.sna_opacity_default
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
    
class SNA_OT_Disable_Image_Mesh_Plane_Opacity_Workbench(bpy.types.Operator):
    bl_idname = "wm.disable_image_mesh_plane_opacity_workbench"
    bl_label = "Disable Image Mesh Plane Opacity (Workbench)"
    bl_description = "Remove alpha slider from Image Mesh Plane Object"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = context.object
        mat = obj.active_material
        mat.diffuse_color[3] = 1.0
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
    
class SNA_OT_Bring_Object_Forward(bpy.types.Operator):
    bl_idname = "wm.bring_object_forward"
    bl_label = "Bring Object Forward"
    bl_description = "Y - 0.002"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        if bpy.context.active_object is None :
            self.report({'ERROR'}, "Select a object! if object is hidden, unhide it")
        else :
            bpy.context.active_object.location.y -= 0.002
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Bring_Object_Backward(bpy.types.Operator):
    bl_idname = "wm.bring_object_backward"
    bl_label = "Bring Object Backward"
    bl_description = "Y + 0.002"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        if bpy.context.active_object is None :
            self.report({'ERROR'}, "Select a object! if object is hidden, unhide it")
        else :
            bpy.context.active_object.location.y += 0.002
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Hide_From_List(bpy.types.Operator):
    bl_idname = "wm.hide_from_list_05f1a"
    bl_label = "Hide from list"
    bl_description = "Hide selected object from list by inserting ' # ' to its name. Remove the ' # '  by renaming it from outliner to bring it back to the list"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        Input = None
        Input = bpy.context.active_object
        Input.name = "#" + str(Input.name)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)

class MATERIAL_MENU(bpy.types.Panel):
    bl_label = "Material Menu"
    bl_idname = "MATERIAL_MENU"
    bl_space_type = "VIEW_3D"
    bl_region_type = "WINDOW"

    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == "GREASEPENCIL"

    def draw(self, context):
        layout = self.layout
        obj = context.active_object

        if obj:
            col = layout.column(align=True)
            col.operator("wm.add_material_stroke_only", text="Add Stroke Only", icon_value=string_to_icon("MATERIAL"))
            col.operator("wm.add_material_fill_only", text="Add Fill Only", icon_value=string_to_icon("MATERIAL"))
            col.operator("wm.add_material_stroke_and_fill", text="Add Stroke + Fill", icon_value=string_to_icon("MATERIAL"))

            col = layout.column(align=True)
            col.operator("wm.link_all_materials", text="Link All Material", icon_value=string_to_icon("LINKED"))
            col.operator("wm.unlink_all_materials", text="Unlink All Material", icon_value=string_to_icon("UNLINKED"))

            col = layout.column(align=True)
            col.operator("wm.delete_material", text="Delete Active Material", icon_value=string_to_icon("TRASH"))
        else:
            layout.label(text="Select a Grease Pencil Object!")

class OBJECT_MENU(bpy.types.Panel):
    bl_label = "Object Menu"
    bl_idname = "OBJECT_MENU"
    bl_space_type = "VIEW_3D"
    bl_region_type = "WINDOW"

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout = self.layout

        # Filter box
        box = layout.box()
        col = box.column(align=True)
        col.label(text="Filter :", icon_value=0)
        col.prop(context.scene, "sna_include_mesh_objects", 
                 text="Include Mesh Objects", 
                 icon_value=string_to_icon("OUTLINER_OB_MESH"))
        col.operator("wm.hide_from_list_05f1a", 
                     text="Exclude Object from the list", 
                     icon_value=string_to_icon("GRID"))

        # GPencil options
        col = layout.column(align=True)
        col.operator("wm.add_empty_with_all_materials_abd31", 
                     text="Add GPencil + Materials", 
                     icon_value=string_to_icon("OUTLINER_OB_GREASEPENCIL"))
        col.operator("wm.add_empty_without_materials_7097f", 
                     text="Add Empty GPencil", 
                     icon_value=string_to_icon("OUTLINER_OB_GREASEPENCIL"))

class SNA_OT_Add_Empty_Without_Materials(bpy.types.Operator):
    bl_idname = "wm.add_empty_without_materials_7097f"
    bl_label = "Add Empty without Materials"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        if bpy.context.active_object is None :
            bpy.ops.object.grease_pencil_add(type='EMPTY',use_lights=False)
            bpy.data.grease_pencils[bpy.context.active_object.data.name].use_autolock_layers = True
        else:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.grease_pencil_add(type='EMPTY',use_lights=False)
            bpy.data.grease_pencils[bpy.context.active_object.data.name].use_autolock_layers = True
        obj = bpy.context.object
        if obj is not None:
            if obj.type == 'GREASEPENCIL':
                if obj.active_material is not None:
                    bpy.data.materials.remove(obj.active_material)
                    bpy.ops.object.material_slot_remove()
                else: pass
            else: pass
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)

class SNA_OT_Add_Empty_With_All_Materials(bpy.types.Operator):
    bl_idname = "wm.add_empty_with_all_materials_abd31"
    bl_label = "Add Empty with all Materials"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        if bpy.context.active_object is None :
            bpy.ops.object.grease_pencil_add(type='EMPTY',use_lights=False)
            bpy.data.grease_pencils[bpy.context.active_object.data.name].use_autolock_layers = True
        else:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.grease_pencil_add(type='EMPTY',use_lights=False)
            bpy.data.grease_pencils[bpy.context.active_object.data.name].use_autolock_layers = True
        obj = bpy.context.object
        if obj is not None:
            if obj.type == 'GREASEPENCIL':
                if obj.active_material is not None:
                    bpy.data.materials.remove(obj.active_material)
                    bpy.ops.object.material_slot_remove()
                else: pass
            else: pass
        obj = bpy.context.object
        arr_x = [x.name for x in obj.material_slots]
        res = [k for k in obj.material_slots]

        def app():
            for mat in bpy.data.materials:
                if mat.is_grease_pencil and mat.name not in arr_x:
                    obj.data.materials.append(mat)

        def rem():
            for slot in res:
                if slot.material is None:
                    # Set the active material slot to Empty
                    obj.active_material_index = slot.slot_index
                    # Remove the active material slot
                    bpy.ops.object.material_slot_remove()
                else: pass
        rem()
        app()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)

class SNA_OT_Delete_Material(bpy.types.Operator):
    bl_idname = "wm.delete_material"
    bl_label = "Delete Material"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = bpy.context.object
        if obj is not None:
            if obj.type == 'GREASEPENCIL':
                if obj.active_material is not None:
                    bpy.data.materials.remove(obj.active_material)
                    bpy.ops.object.material_slot_remove()
                else: pass
            else: pass
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
    
class SNA_OT_Unlink_All_Materials(bpy.types.Operator):
    bl_idname = "wm.unlink_all_materials"
    bl_label = "Unlink All Materials"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = bpy.context.active_object
        last = len(obj.material_slots)
        res = [k for k in obj.material_slots]

        def remove():
            obj.active_material_index = last
            bpy.ops.object.material_slot_remove()   
        for slot in res:
            remove()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)

class SNA_OT_Link_All_Materials(bpy.types.Operator):
    bl_idname = "wm.link_all_materials"
    bl_label = "Link All Materials"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = bpy.context.object
        arr_x = [x.name for x in obj.material_slots]
        res = [k for k in obj.material_slots]

        def app():
            for mat in bpy.data.materials:
                if mat.is_grease_pencil and mat.name not in arr_x:
                    obj.data.materials.append(mat)

        def rem():
            for slot in res:
                if slot.material is None:
                    # Set the active material slot to Empty
                    obj.active_material_index = slot.slot_index
                    # Remove the active material slot
                    bpy.ops.object.material_slot_remove()
                else: pass
        rem()
        app()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)

       
class SNA_OT_Add_Material_Stroke_And_Fill(bpy.types.Operator):
    bl_idname = "wm.add_material_stroke_and_fill"
    bl_label = "Add Material Stroke and Fill (B) B for Both"
    bl_description = "Add Material Stroke and Fill (B)(B for Both)"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        ob = bpy.context.active_object
        mat = bpy.data.materials.new(name="B-")
        bpy.data.materials.create_gpencil_data(mat)
        ob.data.materials.append(mat)
        mat.grease_pencil.show_stroke = True
        mat.grease_pencil.show_fill = True
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)

class SNA_OT_Add_Material_Fill_Only(bpy.types.Operator):
    bl_idname = "wm.add_material_fill_only"
    bl_label = "Add Material Fill Only (F)"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        ob = bpy.context.active_object
        mat = bpy.data.materials.new(name="F-")
        bpy.data.materials.create_gpencil_data(mat)
        ob.data.materials.append(mat)
        mat.grease_pencil.show_stroke = False
        mat.grease_pencil.show_fill = True
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
        
class SNA_OT_Add_Material_Stroke_Only(bpy.types.Operator):
    bl_idname = "wm.add_material_stroke_only"
    bl_label = "Add Material Stroke Only (S)"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        ob = bpy.context.active_object
        mat = bpy.data.materials.new(name="S-")
        bpy.data.materials.create_gpencil_data(mat)
        ob.data.materials.append(mat)
        mat.grease_pencil.show_stroke = True
        mat.grease_pencil.show_fill = False
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
        
class SNA_PT_SELECTOR(bpy.types.Panel):
    bl_label = 'Manager'
    bl_idname = 'SNA_PT_SELECTOR'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SakugaGP'

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout = self.layout
        col = layout.column()

        obj = context.view_layer.objects.active

        # Object list
        row = col.row(align=True)
        coll_id = display_collection_id('FECBF', locals())
        row.template_list('SNA_UL_display_collection_list', coll_id, bpy.data, 'objects',
                          context.scene, 'sna_object_list')
        col_ops = row.column(align=True)
        col_ops.popover('OBJECT_MENU', text='', icon_value=string_to_icon('OBJECT_DATA'))
        col_ops.popover('MATERIAL_MENU', text='', icon_value=string_to_icon('MATERIAL'))
        
        engine = bpy.context.scene.render.engine
        if obj:
            # Object order operators
            col_ops.operator('wm.bring_object_forward', text='', icon_value=string_to_icon('TRIA_UP'))
            col_ops.operator('wm.bring_object_backward', text='', icon_value=string_to_icon('TRIA_DOWN'))

            # Opacity toggle operators
            if obj.type != 'CAMERA':
                if obj.type == 'EMPTY':
                    if obj.use_empty_image_alpha == False:
                        col_ops.operator('wm.enable_ref_opacity', text='', icon_value=string_to_icon('MOD_OPACITY'))
                    else:  
                        col_ops.operator('wm.disable_ref_opacity', text='', icon_value=string_to_icon('MOD_PHYSICS'))

                elif obj.type == 'MESH':
                    if engine == 'BLENDER_EEVEE' or engine == 'CYCLES':
                        if selector['sna_opacity_mesh_check'] == False:
                            col_ops.operator('wm.enable_image_mesh_plane_opacity', text='', icon_value=string_to_icon('MOD_OPACITY'))
                        else:
                            col_ops.operator('wm.disable_image_mesh_plane_opacity', text='', icon_value=string_to_icon('MOD_PHYSICS'))
                    
                    elif engine == 'BLENDER_WORKBENCH':
                        if selector['sna_opacity_mesh_check'] == False:
                            col_ops.operator('wm.enable_image_mesh_plane_opacity_workbench', text='', icon_value=string_to_icon('MOD_OPACITY'))
                        else:
                            col_ops.operator('wm.disable_image_mesh_plane_opacity_workbench', text='', icon_value=string_to_icon('MOD_PHYSICS'))
                        
                        
                elif obj.type == 'GREASEPENCIL':
                    if selector['sna_opacity_gp_check'] == False:
                        col_ops.operator('wm.enable_grease_pencil_opacity', text='', icon_value=string_to_icon('MOD_OPACITY'))
                    else:
                        col_ops.operator('wm.disable_gp_opacity', text='', icon_value=string_to_icon('MOD_PHYSICS'))

            # Freeze frame operators
            if obj.type == 'GREASEPENCIL':
                freeze_row = col.row(align=True)
                freeze_row.label(icon_value=string_to_icon('FREEZE'), text='Freeze Frame:')
                freeze_row.operator('wm.freeze_red', text='', icon_value=string_to_icon('STRIP_COLOR_01'))
                freeze_row.operator('wm.freeze_green', text='', icon_value=string_to_icon('STRIP_COLOR_03'))
                freeze_row.operator('wm.freeze_blue', text='', icon_value=string_to_icon('STRIP_COLOR_06'))

            # Opacity slider controls
            if obj.type == 'EMPTY' and obj.use_empty_image_alpha:
                col.prop(context.scene, 'sna_opacity_ref', text='Opacity')
                col.prop(obj, 'color', text='')

            elif obj.type == 'GREASEPENCIL':
                if selector['sna_opacity_gp_check'] == True:
                    col.prop(obj.modifiers['sakugagp_opacity'], 'color_factor', text='Opacity')

            elif obj.type == 'MESH':
                if engine == 'BLENDER_EEVEE' or engine == 'CYCLES':
                    col.prop(context.scene, 'sna_opacity_mesh', text='Opacity')
                elif engine == 'BLENDER_WORKBENCH':
                    if selector['sna_opacity_mesh_check'] == True:
                        mat = obj.active_material
                        col.prop(mat, "diffuse_color",index=3, text="Opacity")
                        col.prop(mat, "diffuse_color",text="")

class SNA_OT_Freeze_Color(bpy.types.Operator):
    bl_idname = "wm.freeze_color"
    bl_label = "Freeze Color"
    bl_description = "Duplicate and Freeze Current Object's Frame with Tint"
    bl_options = {"REGISTER", "UNDO"}

    # default tint color, subclasses override this
    tint_color = (1.0, 0.0, 0.0)

    def execute(self, context):
        obj = bpy.context.active_object
        sc = bpy.context.scene

        if obj and obj.type == "GREASEPENCIL":
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.duplicate(linked=True)

            # Rename duplicated object
            dup_obj = bpy.context.active_object
            dup_obj.name = f"frozen_{obj.name}_{sc.frame_current}"

            # Add time offset modifier
            time_mod = dup_obj.modifiers.new(
                name='sakugagp_time_offset_freeze',
                type='GREASE_PENCIL_TIME'
            )
            time_mod.mode = "FIX"
            time_mod.offset = sc.frame_current

            # Add tint modifier
            tint_mod = dup_obj.modifiers.new(
                name='sakugagp_tint_freeze',
                type='GREASE_PENCIL_TINT'
            )
            tint_mod.factor = 1.0
            tint_mod.color = self.tint_color   # ✅ use subclass color

            # Ensure opacity modifier exists
            default_opacity = sc.sna_opacity_default
            if "sakugagp_opacity" not in [mod.name for mod in dup_obj.modifiers]:
                op_mod = dup_obj.modifiers.new(
                    name='sakugagp_opacity',
                    type='GREASE_PENCIL_OPACITY'
                )
                op_mod.color_factor = default_opacity

        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


# Register operators for Red, Green, Blue
class SNA_OT_Freeze_Red(SNA_OT_Freeze_Color):
    bl_idname = "wm.freeze_red"
    bl_label = "Freeze Red"
    tint_color = (1.0, 0.0, 0.0)


class SNA_OT_Freeze_Green(SNA_OT_Freeze_Color):
    bl_idname = "wm.freeze_green"
    bl_label = "Freeze Green"
    tint_color = (0.0, 1.0, 0.0)


class SNA_OT_Freeze_Blue(SNA_OT_Freeze_Color):
    bl_idname = "wm.freeze_blue"
    bl_label = "Freeze Blue"
    tint_color = (0.0, 0.0, 1.0)


# Scene properties
scene_props = [
    ("sna_object_list", bpy.props.IntProperty(
        name='Object List', default=0,
        update=sna_update_sna_object_list_EDFF0)),
    ("sna_include_mesh_objects", bpy.props.BoolProperty(
        name='Include Mesh Objects', default=False)),
    ("sna_opacity_ref", bpy.props.FloatProperty(
        name='opacity_ref', default=0.0, min=0.0, max=1.0,
        step=3, precision=2, update=sna_update_sna_opacity_ref)),
    ("sna_opacity_mesh", bpy.props.FloatProperty(
        name='opacity_mesh', default=0.0, min=0.0, max=1.0,
        step=3, precision=2, update=sna_update_sna_opacity_mesh)),
    ("sna_opacity_default", bpy.props.FloatProperty(
        name='opacity_default', default=0.3, min=0.0, max=1.0,
        step=5, precision=2))
]

# Classes to register/unregister
classes = [
    SNA_OT_Enable_Image_Mesh_Plane_Opacity,
    SNA_OT_Disable_Image_Mesh_Plane_Opacity,
    SNA_OT_Enable_Image_Mesh_Plane_Opacity_Workbench,
    SNA_OT_Disable_Image_Mesh_Plane_Opacity_Workbench,
    SNA_OT_Disable_Gp_Opacity,
    SNA_OT_Bring_Object_Forward,
    SNA_OT_Bring_Object_Backward,
    SNA_OT_Hide_From_List,
    OBJECT_MENU,
    MATERIAL_MENU,
    SNA_OT_Enable_Grease_Pencil_Opacity,
    SNA_OT_Enable_Ref_Opacity,
    SNA_OT_Disable_Ref_Opacity,
    SNA_PT_SELECTOR,
    SNA_UL_display_collection_list,
    SNA_OT_Freeze_Color,
    SNA_OT_Freeze_Red,
    SNA_OT_Freeze_Green,
    SNA_OT_Freeze_Blue,
    SNA_OT_Add_Empty_Without_Materials,
    SNA_OT_Add_Empty_With_All_Materials,
    SNA_OT_Link_All_Materials,
    SNA_OT_Unlink_All_Materials,
    SNA_OT_Delete_Material,
    SNA_OT_Add_Material_Stroke_Only,
    SNA_OT_Add_Material_Fill_Only,
    SNA_OT_Add_Material_Stroke_And_Fill,
]

def register():
    # Register properties
    for prop_name, prop_def in scene_props:
        setattr(bpy.types.Scene, prop_name, prop_def)

    # Register classes
    for cls in classes:
        bpy.utils.register_class(cls)

    # Register handler once
    if depsgraph_update_pre_handler not in bpy.app.handlers.depsgraph_update_pre:
        bpy.app.handlers.depsgraph_update_pre.append(depsgraph_update_pre_handler)

def unregister():
    # Remove properties
    for prop_name, _ in scene_props:
        delattr(bpy.types.Scene, prop_name)

    # Unregister classes
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    # Remove handler safely
    if depsgraph_update_pre_handler in bpy.app.handlers.depsgraph_update_pre:
        bpy.app.handlers.depsgraph_update_pre.remove(depsgraph_update_pre_handler)

if __name__ == "__main__":
    register()

