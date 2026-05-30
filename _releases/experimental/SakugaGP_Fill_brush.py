bl_info = {
    "name": "Sakuga - Fill Brush (Experimental)",
    "author": "Sadewoo",
    "version": (0, 0, 1),
    "blender": (5, 0, 0),
    "location": "View3D > Sidebar > SakugaGP > Fill Brush",
    "description": "Converts Strokes to Fills with Boolean operations using pyclipper",
    "category": "Grease Pencil",
}

import bpy, pyclipper
import math
from mathutils import Vector

def scale_to_clipper(val, scale=100000): return int(round(val * scale))
def scale_from_clipper(val, scale=100000): return float(val) / scale

def execute_pyclipper_boolean_operation(context, op_type="UNION"):
    obj = context.active_object
    if not obj or obj.type != 'GREASEPENCIL': return {"CANCELLED"}
    idx = obj.active_material_index
    if not obj.material_slots or idx < 0: return {"CANCELLED"}
    mat = obj.material_slots[idx].material
    if not mat: return {"CANCELLED"}
    if hasattr(mat, "grease_pencil") and mat.grease_pencil:
        mat.grease_pencil.show_stroke, mat.grease_pencil.show_fill = False, True

    layer = obj.data.layers.active
    if not layer or not layer.frames: return {"CANCELLED"}
    frame = next((f for f in layer.frames if f.frame_number == context.scene.frame_current), None)
    if not frame or not frame.drawing: return {"CANCELLED"}
    drawing, old_count = frame.drawing, len(frame.drawing.strokes)

    # Detect Active Brush Cap Settings
    caps_type = 'ROUND'
    try:
        brush = context.tool_settings.gpencil_paint.brush
        if brush and hasattr(brush, "gpencil_settings"):
            caps_type = brush.gpencil_settings.caps_type
    except AttributeError:
        pass

    existing_shapes, new_hulls = [], []
    # TRACK PRECISELY WHICH STROKE INDICES TO REMOVE AT THE END
    stroke_indices_to_remove = []

    for s_idx, stroke in enumerate(drawing.strokes):
        if len(stroke.points) < 2: continue
        
        # Only process strokes that match the ACTIVE material index
        if stroke.material_index != idx: 
            continue

        stroke_indices_to_remove.append(s_idx)
        is_cyclic = getattr(stroke, "cyclic", False)

        if is_cyclic and len(stroke.points) >= 3:
            path = [(scale_to_clipper(p.position.x), scale_to_clipper(p.position.z)) for p in stroke.points]
            existing_shapes.append(path)
        else:
            # Extract pen pressure thickness attributes
            pressures = None
            if "pressure" in drawing.attributes:
                pr_attr = drawing.attributes["pressure"].data
                pr_slice = pr_attr[stroke.points_range.start:stroke.points_range.stop]
                pressures = [d.value for d in pr_slice]

            pts = [Vector((p.position.x, 0.0, p.position.z)) for p in stroke.points]
            radii = [max(p.radius * (pressures[i] if pressures else 1.0), 0.0001) for i, p in enumerate(stroke.points)]
            pts_count = len(pts)

            # Generate forward segment direction vectors
            seg_dirs = []
            for i in range(pts_count - 1):
                d = pts[i+1] - pts[i]
                if d.length == 0:
                    d = Vector((1.0, 0.0, 0.0))
                seg_dirs.append(d.normalized())

            outer_track, inner_track = [], []
            
            # 1. Starting vertex track offsets
            d_start = seg_dirs[0]
            n_start = Vector((-d_start.z, 0.0, d_start.x))
            outer_track.append(pts[0] + n_start * radii[0])
            inner_track.append(pts[0] - n_start * radii[0])

            # 2. Intermediate mitered joints offsets
            for i in range(1, pts_count - 1):
                d1 = seg_dirs[i-1]
                d2 = seg_dirs[i]
                n1 = Vector((-d1.z, 0.0, d1.x))
                n2 = Vector((-d2.z, 0.0, d2.x))
                
                bisector = (n1 + n2)
                if bisector.length == 0:
                    bisector = n1
                else:
                    bisector.normalize()
                
                cos_half_angle = bisector.dot(n1)
                if cos_half_angle > 0.1:
                    miter_scale = 1.0 / cos_half_angle
                    if miter_scale > 3.0: 
                        miter_out, miter_in = n1, -n1
                    else:
                        miter_out, miter_in = bisector * miter_scale, -bisector * miter_scale
                else:
                    miter_out, miter_in = n1, -n1

                outer_track.append(pts[i] + miter_out * radii[i])
                inner_track.append(pts[i] + miter_in * radii[i])

            # 3. Ending vertex track offsets
            d_end = seg_dirs[-1]
            n_end = Vector((-d_end.z, 0.0, d_end.x))
            outer_track.append(pts[-1] + n_end * radii[-1])
            inner_track.append(pts[-1] - n_end * radii[-1])

            # --- SEAMLESS SINGLE CONTOUR LOOP ASSEMBLY ---
            silhouette = []

            # Start Cap Construction
            if caps_type == 'ROUND':
                cap_steps = 12
                start_pos = pts[0]
                for step in range(cap_steps + 1):
                    angle = math.pi * (step / cap_steps)
                    offset_vec = (-n_start * math.cos(angle)) - (d_start * math.sin(angle))
                    pt_loc = start_pos + offset_vec * radii[0]
                    silhouette.append((scale_to_clipper(pt_loc.x), scale_to_clipper(pt_loc.z)))
            else:  # 'FLAT'
                silhouette.append((scale_to_clipper(inner_track[0].x), scale_to_clipper(inner_track[0].z)))
                silhouette.append((scale_to_clipper(outer_track[0].x), scale_to_clipper(outer_track[0].z)))

            # Outer Track Points
            for i in range(1, pts_count):
                pt_loc = outer_track[i]
                silhouette.append((scale_to_clipper(pt_loc.x), scale_to_clipper(pt_loc.z)))

            # End Cap Construction
            if caps_type == 'ROUND':
                cap_steps = 12
                end_pos = pts[-1]
                for step in range(cap_steps + 1):
                    angle = math.pi * (step / cap_steps)
                    offset_vec = (n_end * math.cos(angle)) + (d_end * math.sin(angle))
                    pt_loc = end_pos + offset_vec * radii[-1]
                    silhouette.append((scale_to_clipper(pt_loc.x), scale_to_clipper(pt_loc.z)))
            else:  # 'FLAT'
                silhouette.append((scale_to_clipper(outer_track[-1].x), scale_to_clipper(outer_track[-1].z)))
                silhouette.append((scale_to_clipper(inner_track[-1].x), scale_to_clipper(inner_track[-1].z)))

            # Inner Track Points (Processed in reverse sequence)
            for i in range(pts_count - 2, -1, -1):
                pt_loc = inner_track[i]
                silhouette.append((scale_to_clipper(pt_loc.x), scale_to_clipper(pt_loc.z)))

            if len(silhouette) >= 3:
                new_hulls.append(silhouette)

    # --- CLIPPER ENGINE LOGIC ---
    pc, result = pyclipper.Pyclipper(), []
    
    if op_type == "UNION":
        if not existing_shapes and not new_hulls: return {"CANCELLED"}
        if existing_shapes: pc.AddPaths(existing_shapes, pyclipper.PT_SUBJECT, True)
        if new_hulls: pc.AddPaths(new_hulls, pyclipper.PT_CLIP, True)
        result = pc.Execute(pyclipper.CT_UNION, pyclipper.PFT_NONZERO, pyclipper.PFT_NONZERO)
    elif op_type == "SUBTRACT":
        if not existing_shapes or not new_hulls: return {"CANCELLED"}
        pc.AddPaths(existing_shapes, pyclipper.PT_SUBJECT, True)
        pc.AddPaths(new_hulls, pyclipper.PT_CLIP, True)
        result = pc.Execute(pyclipper.CT_DIFFERENCE, pyclipper.PFT_NONZERO, pyclipper.PFT_NONZERO)

    # SAFE DELETION: If no boolean results generated, only wipe processed indices
    if not result:
        drawing.remove_strokes(indices=stroke_indices_to_remove)
        context.view_layer.update(); return {"FINISHED"}

    drawing.add_strokes([len(p) for p in result])
    for i, path in enumerate(result):
        s = drawing.strokes[old_count + i]; s.material_index, s.cyclic = idx, True
        s.hide_stroke, s.fill_id = True, 1
        for j, pt in enumerate(path):
            p = s.points[j]
            rx, rz = scale_from_clipper(pt[0]), scale_from_clipper(pt[1])
            p.position = (rx, 0.0, rz)
            p.opacity = 1.0
            p.radius = 0.01

    # FIXED: Only delete old strokes that match the processed material index
    drawing.remove_strokes(indices=stroke_indices_to_remove)
    context.view_layer.update(); return {"FINISHED"}

class GP_OT_PyclipperUnion(bpy.types.Operator):
    bl_idname, bl_label, bl_description, bl_options = "wm.pyclipper_union", "Union Silhouette", "Welds new brush traces", {'REGISTER','UNDO'}
    def execute(self, ctx): return execute_pyclipper_boolean_operation(ctx, "UNION")

class GP_OT_PyclipperSubtract(bpy.types.Operator):
    bl_idname, bl_label, bl_description, bl_options = "wm.pyclipper_subtract", "Subtract Silhouette", "Cuts holes with brush traces", {'REGISTER','UNDO'}
    def execute(self, ctx): return execute_pyclipper_boolean_operation(ctx, "SUBTRACT")

class GP_PT_PyclipperPanel(bpy.types.Panel):
    bl_label, bl_idname, bl_space_type, bl_region_type, bl_category = "Fill Brush", "GP_PT_fill_brush_panel", 'VIEW_3D', 'UI', "SakugaGP"
    def draw(self, ctx):
        layout, obj = self.layout, ctx.active_object
        if not obj or obj.type != 'GREASEPENCIL': layout.label(text="Select a Grease Pencil object", icon='ERROR'); return
        col = layout.column(align=True); col.scale_y = 1.3
        col.operator("wm.pyclipper_union", text="Union", icon='ADD'); col.separator()
        col.operator("wm.pyclipper_subtract", text="Subtract", icon='REMOVE')

classes = (GP_OT_PyclipperUnion, GP_OT_PyclipperSubtract, GP_PT_PyclipperPanel)
def register(): [bpy.utils.register_class(c) for c in classes]
def unregister(): [bpy.utils.unregister_class(c) for c in reversed(classes)]
if __name__ == "__main__": register()
