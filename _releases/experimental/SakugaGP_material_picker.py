bl_info = {
    "name": "SakugaGP - Material Picker (Experimental)",
    "author": "Sadewoo (Spikysaurus)",
    "version": (0, 0, 1),
    "blender": (5, 0, 0),
    "location": "View3D",
    "description": "Adds Grease Pencil Material picker to the Viewport",
    "category": "Grease Pencil",
}

import bpy
from bpy.types import GizmoGroup, Operator
from mathutils import Matrix

BUTTON_OFFSET = [100, 100]   # offset from chosen corner
ANCHOR_CORNER = "BL"         # BL, BR, TL, TR
BUTTON_SPACING_X, BUTTON_SPACING_Y = 30, 40
SMALL_BUTTON_OFFSET_X, SMALL_BUTTON_OFFSET_Y = 8, -18
BUTTONS_PER_LINE = 8

def get_anchor_pos(region):
    if ANCHOR_CORNER == "BL": return (BUTTON_OFFSET[0], BUTTON_OFFSET[1])
    if ANCHOR_CORNER == "BR": return (region.width - BUTTON_OFFSET[0], BUTTON_OFFSET[1])
    if ANCHOR_CORNER == "TL": return (BUTTON_OFFSET[0], region.height - BUTTON_OFFSET[1])
    if ANCHOR_CORNER == "TR": return (region.width - BUTTON_OFFSET[0], region.height - BUTTON_OFFSET[1])

# --- Operators ---
class VIEW3D_OT_set_gp_material(Operator):
    bl_idname, bl_label = "view3d.set_gp_material", "Set Grease Pencil Material"
    bl_options = {'REGISTER','UNDO'}
    material_index: bpy.props.IntProperty()
    material_name: bpy.props.StringProperty()
    def execute(self, context):
        obj = context.active_object
        if obj and obj.type == 'GREASEPENCIL':
            obj.active_material_index = self.material_index
        return {'FINISHED'}
    @classmethod
    def description(cls, context, props): return f"{props.material_name}"

class VIEW3D_OT_add_gp_material(Operator):
    bl_idname, bl_label = "view3d.add_gp_material", "Add Grease Pencil Material"
    bl_options = {'REGISTER','UNDO'}
    def execute(self, context):
        obj = context.active_object
        if obj and obj.type == 'GREASEPENCIL':
            mat = bpy.data.materials.new(name="New Material")
            bpy.data.materials.create_gpencil_data(mat)
            obj.data.materials.append(mat)
            mat.grease_pencil.show_stroke, mat.grease_pencil.show_fill = True, True
            bpy.utils.unregister_class(VIEW3D_GZ_gp_material_buttons)
            bpy.utils.register_class(VIEW3D_GZ_gp_material_buttons)
        return {'FINISHED'}
    @classmethod
    def description(cls, context, props): return "Add new Grease Pencil material"

class VIEW3D_OT_delete_gp_material(Operator):
    bl_idname, bl_label = "view3d.delete_gp_material", "Delete Active Grease Pencil Material"
    bl_options = {"REGISTER","UNDO"}
    def execute(self, context):
        obj = context.active_object
        if obj and obj.type == 'GREASEPENCIL' and obj.active_material:
            bpy.data.materials.remove(obj.active_material)
            bpy.ops.object.material_slot_remove()
            bpy.utils.unregister_class(VIEW3D_GZ_gp_material_buttons)
            bpy.utils.register_class(VIEW3D_GZ_gp_material_buttons)
        return {"FINISHED"}
    @classmethod
    def description(cls, context, props): return "Delete currently active Grease Pencil material"

class VIEW3D_OT_drag_gizmo(Operator):
    bl_idname = "view3d.drag_gizmo"
    bl_label = "Drag Gizmo Overlay"
    bl_options = {'BLOCKING'}
    start_mouse_x: bpy.props.IntProperty()
    start_mouse_y: bpy.props.IntProperty()
    start_button_x: bpy.props.IntProperty()
    start_button_y: bpy.props.IntProperty()

    def modal(self, context, event):
        global BUTTON_OFFSET, ANCHOR_CORNER
        context.area.tag_redraw()
        region = context.region
        if event.type == 'MOUSEMOVE':
            dx = event.mouse_region_x - self.start_mouse_x
            dy = event.mouse_region_y - self.start_mouse_y
            abs_x = self.start_button_x + dx
            abs_y = self.start_button_y + dy
            corners = {
                "BL": (abs_x, abs_y),
                "BR": (region.width - abs_x, abs_y),
                "TL": (abs_x, region.height - abs_y),
                "TR": (region.width - abs_x, region.height - abs_y),
            }
            ANCHOR_CORNER, _ = min(corners.items(), key=lambda kv: kv[1][0]**2+kv[1][1]**2)
            if ANCHOR_CORNER == "BL": BUTTON_OFFSET = [abs_x, abs_y]
            elif ANCHOR_CORNER == "BR": BUTTON_OFFSET = [region.width - abs_x, abs_y]
            elif ANCHOR_CORNER == "TL": BUTTON_OFFSET = [abs_x, region.height - abs_y]
            elif ANCHOR_CORNER == "TR": BUTTON_OFFSET = [region.width - abs_x, region.height - abs_y]
            return {'RUNNING_MODAL'}
        elif event.type in {'LEFTMOUSE','RIGHTMOUSE','ESC'}:
            return {'FINISHED'}
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        global BUTTON_OFFSET, ANCHOR_CORNER
        region = context.region
        base_x, base_y = get_anchor_pos(region)
        self.start_mouse_x, self.start_mouse_y = event.mouse_region_x, event.mouse_region_y
        self.start_button_x, self.start_button_y = base_x, base_y
        context.window.cursor_set("HAND")
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}
    @classmethod
    def description(cls, context, props): return "Drag handle"

# --- Gizmo Group ---
class VIEW3D_GZ_gp_material_buttons(GizmoGroup):
    bl_idname, bl_label = "VIEW3D_GZ_gp_material_buttons", "Grease Pencil Material Overlay Buttons"
    bl_space_type, bl_region_type, bl_options = 'VIEW_3D','WINDOW',{'PERSISTENT','SCALE'}
    def setup(self, context):
        obj = context.active_object; self.buttons, self.small_buttons = [], []
        # Drag button
        drag_btn = self.gizmos.new("GIZMO_GT_button_2d")
        drag_btn.target_set_operator("view3d.drag_gizmo")
        drag_btn.icon, drag_btn.scale_basis = 'HAND', 14.0
        drag_btn.draw_options, drag_btn.color, drag_btn.alpha = {'BACKDROP'}, (0.8,0.8,0.2), 1.0
        drag_btn.use_draw_modal = True; self.drag_button = drag_btn
        # Add button
        plus_btn = self.gizmos.new("GIZMO_GT_button_2d")
        plus_btn.target_set_operator("view3d.add_gp_material")
        plus_btn.icon, plus_btn.scale_basis = 'PLUS', 14.0
        plus_btn.draw_options, plus_btn.color, plus_btn.alpha = {'BACKDROP'}, (0.2,0.8,0.2), 1.0
        plus_btn.use_draw_modal = True; self.plus_button = plus_btn
        # Delete button
        del_btn = self.gizmos.new("GIZMO_GT_button_2d")
        del_btn.target_set_operator("view3d.delete_gp_material")
        del_btn.icon, del_btn.scale_basis = 'X', 14.0
        del_btn.draw_options, del_btn.color, del_btn.alpha = {'BACKDROP'}, (0.8,0.2,0.2), 1.0
        del_btn.use_draw_modal = True; self.delete_button = del_btn
        # Material buttons
        if obj and obj.type == 'GREASEPENCIL':
            for i, slot in enumerate(obj.material_slots):
                mat = slot.material
                if mat and mat.grease_pencil:
                    gp = mat.grease_pencil
                    btn = self.gizmos.new("GIZMO_GT_button_2d")
                    op = btn.target_set_operator("view3d.set_gp_material")
                    op.material_index, op.material_name = i, mat.name
                    btn.icon, btn.scale_basis = 'NONE', 12.0
                    btn.draw_options, btn.color, btn.alpha = {'BACKDROP'}, tuple(gp.fill_color[:3]), gp.fill_color[3]
                    btn.use_draw_modal = True; self.buttons.append(btn)
                    small_btn = self.gizmos.new("GIZMO_GT_button_2d")
                    op_s = small_btn.target_set_operator("view3d.set_gp_material")
                    op_s.material_index, op_s.material_name = i, mat.name
                    small_btn.icon, small_btn.scale_basis = 'STROKE', 10.0
                    small_btn.draw_options, small_btn.color, small_btn.alpha = {'BACKDROP'}, tuple(gp.color[:3]), gp.color[3]
                    small_btn.use_draw_modal = True; self.small_buttons.append(small_btn)
    def draw_prepare(self, context):
        global BUTTON_OFFSET, BUTTON_SPACING_X, BUTTON_SPACING_Y, BUTTONS_PER_LINE, ANCHOR_CORNER
        region = context.region
        base_x, base_y = get_anchor_pos(region)
        mat_drag = Matrix.Identity(4); mat_drag[0][3], mat_drag[1][3] = base_x-BUTTON_SPACING_X, base_y
        self.drag_button.matrix_basis = mat_drag
        mat_plus = Matrix.Identity(4); mat_plus[0][3], mat_plus[1][3] = base_x-BUTTON_SPACING_X, base_y-BUTTON_SPACING_Y
        self.plus_button.matrix_basis = mat_plus
        mat_del = Matrix.Identity(4); mat_del[0][3], mat_del[1][3] = base_x-BUTTON_SPACING_X, base_y-2*BUTTON_SPACING_Y
        self.delete_button.matrix_basis = mat_del
        for i,(btn,small_btn) in enumerate(zip(self.buttons,self.small_buttons)):
            line, col = i//BUTTONS_PER_LINE, i%BUTTONS_PER_LINE
            x, y = base_x+col*BUTTON_SPACING_X, base_y-line*BUTTON_SPACING_Y
            mat_main = Matrix.Identity(4); mat_main[0][3], mat_main[1][3] = x, y; btn.matrix_basis = mat_main
            mat_small = Matrix.Identity(4); mat_small[0][3], mat_small[1][3] = x+SMALL_BUTTON_OFFSET_X, y+SMALL_BUTTON_OFFSET_Y
            small_btn.matrix_basis = mat_small

# --- Register ---
classes = (VIEW3D_OT_set_gp_material, VIEW3D_OT_add_gp_material, VIEW3D_OT_delete_gp_material, VIEW3D_OT_drag_gizmo, VIEW3D_GZ_gp_material_buttons)
def register(): [bpy.utils.register_class(c) for c in classes]
def unregister(): [bpy.utils.unregister_class(c) for c in reversed(classes)]
if __name__ == "__main__": register()
