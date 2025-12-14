bl_info = {
    "name" : "SakugaGP - Grease Pencil Extras",
    "author" : "Sadewoo (Spikysaurus)", 
    "description" : "Some extra buttons",
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
    
class SNA_PT_GREASE_PENCIL_888D9(bpy.types.Panel):
    bl_label = 'Grease Pencil Extras'
    bl_idname = 'SNA_PT_GREASE_PENCIL_888D9'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = 'SakugaGP'
    bl_order = 1
    bl_ui_units_x=0

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        
class SNA_OT_Add_Material_Stroke_And_Fill_B_B_For_Both_581B7(bpy.types.Operator):
    bl_idname = "wm.add_material_stroke_and_fill_b_b_for_both_581b7"
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

class SNA_OT_Add_Material_Fill_Only_F_B7E95(bpy.types.Operator):
    bl_idname = "wm.add_material_fill_only_f_b7e95"
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
        
        

class SNA_OT_Add_Material_Stroke_Only_S_F198A(bpy.types.Operator):
    bl_idname = "wm.add_material_stroke_only_s_f198a"
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

class SNA_OT_Add_Empty_Without_Materials_7097F(bpy.types.Operator):
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

class SNA_OT_Add_Empty_With_All_Materials_Abd31(bpy.types.Operator):
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
                    
                    
class SNA_OT_Delete_Material_238Fa(bpy.types.Operator):
    bl_idname = "wm.delete_material_238fa"
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
    
class SNA_OT_Unlink_All_Materials_7Fc01(bpy.types.Operator):
    bl_idname = "wm.unlink_all_materials_7fc01"
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

class SNA_OT_Link_All_Materials_A41Fe(bpy.types.Operator):
    bl_idname = "wm.link_all_materials_a41fe"
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
    

class SNA_PT_OBJECT_4C8BE(bpy.types.Panel):
    bl_label = 'Object'
    bl_idname = 'SNA_PT_OBJECT_4C8BE'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_order = 0
    bl_parent_id = 'SNA_PT_GREASE_PENCIL_888D9'
    bl_ui_units_x=0


    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        col_B4840 = layout.column(heading='', align=True)
        col_B4840.alert = False
        col_B4840.enabled = True
        col_B4840.active = True
        col_B4840.use_property_split = False
        col_B4840.use_property_decorate = False
        col_B4840.scale_x = 1.0
        col_B4840.scale_y = 1.0
        col_B4840.alignment = 'Expand'.upper()
        col_B4840.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        op = col_B4840.operator('wm.add_empty_with_all_materials_abd31', text='Grease Pencil + Materials', icon_value=string_to_icon('OUTLINER_OB_GREASEPENCIL'), emboss=True, depress=False)
        op = col_B4840.operator('wm.add_empty_without_materials_7097f', text='Empty Grease Pencil', icon_value=string_to_icon('OUTLINER_OB_GREASEPENCIL'), emboss=True, depress=False)


class SNA_PT_MATERIAL_A3AB5(bpy.types.Panel):
    bl_label = 'Material'
    bl_idname = 'SNA_PT_MATERIAL_A3AB5'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_order = 1
    bl_parent_id = 'SNA_PT_GREASE_PENCIL_888D9'
    bl_ui_units_x=0
    
    
    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        obj = bpy.context.active_object
        if obj and obj.type == 'GREASEPENCIL':
            layout = self.layout
            col_6E257 = layout.column(heading='', align=True)
            col_6E257.alert = False
            col_6E257.enabled = True
            col_6E257.active = True
            col_6E257.use_property_split = False
            col_6E257.use_property_decorate = False
            col_6E257.scale_x = 1.0
            col_6E257.scale_y = 1.0
            col_6E257.alignment = 'Expand'.upper()
            col_6E257.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            op = col_6E257.operator('wm.add_material_stroke_only_s_f198a', text='Add Stroke Only', icon_value=string_to_icon('PLUS'), emboss=True, depress=False)
            op = col_6E257.operator('wm.add_material_fill_only_f_b7e95', text='Add Fill Only', icon_value=string_to_icon('PLUS'), emboss=True, depress=False)
            op = col_6E257.operator('wm.add_material_stroke_and_fill_b_b_for_both_581b7', text='Add Stroke + Fill', icon_value=string_to_icon('PLUS'), emboss=True, depress=False)
            col_E1F06 = layout.column(heading='', align=True)
            col_E1F06.alert = False
            col_E1F06.enabled = True
            col_E1F06.active = True
            col_E1F06.use_property_split = False
            col_E1F06.use_property_decorate = False
            col_E1F06.scale_x = 1.0
            col_E1F06.scale_y = 1.0
            col_E1F06.alignment = 'Expand'.upper()
            col_E1F06.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            op = col_E1F06.operator('wm.link_all_materials_a41fe', text='Link All Material', icon_value=string_to_icon('LINKED'), emboss=True, depress=False)
            op = col_E1F06.operator('wm.unlink_all_materials_7fc01', text='Unlink All Material', icon_value=string_to_icon('UNLINKED'), emboss=True, depress=False)
            col_C4F2E = layout.column(heading='', align=False)
            col_C4F2E.alert = False
            col_C4F2E.enabled = True
            col_C4F2E.active = True
            col_C4F2E.use_property_split = False
            col_C4F2E.use_property_decorate = False
            col_C4F2E.scale_x = 1.0
            col_C4F2E.scale_y = 1.0
            col_C4F2E.alignment = 'Expand'.upper()
            col_C4F2E.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            op = col_C4F2E.operator('wm.delete_material_238fa', text='Delete Active Material', icon_value=string_to_icon('TRASH'), emboss=True, depress=False)
        else:
            layout = self.layout
            layout.label(text="Select a Grease Pencil Object!")
def register():
    global _icons
    _icons = bpy.utils.previews.new()
    
    bpy.utils.register_class(SNA_OT_Add_Empty_Without_Materials_7097F)
    bpy.utils.register_class(SNA_OT_Add_Empty_With_All_Materials_Abd31)
    bpy.utils.register_class(SNA_PT_GREASE_PENCIL_888D9)
    bpy.utils.register_class(SNA_OT_Link_All_Materials_A41Fe)
    bpy.utils.register_class(SNA_OT_Unlink_All_Materials_7Fc01)
    bpy.utils.register_class(SNA_OT_Delete_Material_238Fa)
    bpy.utils.register_class(SNA_OT_Add_Material_Stroke_Only_S_F198A)
    bpy.utils.register_class(SNA_OT_Add_Material_Fill_Only_F_B7E95)
    bpy.utils.register_class(SNA_OT_Add_Material_Stroke_And_Fill_B_B_For_Both_581B7)
    bpy.utils.register_class(SNA_PT_OBJECT_4C8BE)
    bpy.utils.register_class(SNA_PT_MATERIAL_A3AB5)
    
def unregister():
    global _icons
    bpy.utils.previews.remove(_icons)
    bpy.utils.unregister_class(SNA_OT_Add_Empty_Without_Materials_7097F)
    bpy.utils.unregister_class(SNA_OT_Add_Empty_With_All_Materials_Abd31)
    bpy.utils.unregister_class(SNA_PT_GREASE_PENCIL_888D9)
    bpy.utils.unregister_class(SNA_OT_Link_All_Materials_A41Fe)
    bpy.utils.unregister_class(SNA_OT_Unlink_All_Materials_7Fc01)
    bpy.utils.unregister_class(SNA_OT_Delete_Material_238Fa)
    bpy.utils.unregister_class(SNA_OT_Add_Material_Stroke_Only_S_F198A)
    bpy.utils.unregister_class(SNA_OT_Add_Material_Fill_Only_F_B7E95)
    bpy.utils.unregister_class(SNA_OT_Add_Material_Stroke_And_Fill_B_B_For_Both_581B7)
    bpy.utils.unregister_class(SNA_PT_OBJECT_4C8BE)
    bpy.utils.unregister_class(SNA_PT_MATERIAL_A3AB5)
    
if __name__ == "__main__":
    register()