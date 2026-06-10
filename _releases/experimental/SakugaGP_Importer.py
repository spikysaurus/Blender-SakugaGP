bl_info = {
    "name": "SakugaGP - Importer  (Experimental)",
    "author": "Sadewoo (Spikysaurus)",
    "version": (0, 0, 1),
    "blender": (5, 0, 0),
    "location": "View3D > Sidebar > SakugaGP > Importer",
    "description": "Import Image as Mesh Plane/Reference by Drag & Drop it from File Explorer",
    "category": "Import-Export",
}

import bpy
import os
from bpy.props import EnumProperty, StringProperty, CollectionProperty
from bpy.types import Operator, FileHandler, OperatorFileListElement, Menu, Panel


class VIEW3D_OT_intercept_image_drop(Operator):
    bl_idname = "view3d.intercept_image_drop"
    bl_label = "Import Image Options Selector"
    bl_options = {'UNDO'}

    filepath: StringProperty(subtype='FILE_PATH')
    directory: StringProperty(subtype='DIR_PATH', options={'SKIP_SAVE', 'HIDDEN'})
    files: CollectionProperty(type=OperatorFileListElement, options={'SKIP_SAVE', 'HIDDEN'})

    def invoke(self, context, event):
        if not self.filepath or not os.path.exists(self.filepath):
            return {'CANCELLED'}
        
        self.directory = os.path.dirname(self.filepath)
        base_name = os.path.basename(self.filepath)
        self.files.clear()
        item = self.files.add()
        item.name = base_name
        return self.execute(context)

    def execute(self, context):
        if not self.directory:
            self.directory = os.path.dirname(self.filepath)

        file_list = [{"name": f.name} for f in self.files]
        if not file_list and self.filepath:
            file_list = [{"name": os.path.basename(self.filepath)}]
        props = context.scene.image_drop_settings

        bpy.ops.image.import_as_mesh_planes(
            files=file_list,
            directory=self.directory,
            size_mode=props.size_mode,
            shader=props.shader,
            fill_mode=props.fill_mode
        )
        return {'FINISHED'}

class VIEW3D_OT_import_reference_image(Operator):
    bl_idname = "view3d.import_reference_image"
    bl_label = "Import Image as Reference"
    bl_options = {'UNDO'}

    filepath: StringProperty(subtype='FILE_PATH')

    def execute(self, context):
        if not self.filepath or not os.path.exists(self.filepath):
            return {'CANCELLED'}
        
        bpy.ops.object.empty_image_add(
            filepath=self.filepath,
            background=False,
            align='VIEW'
        )
        return {'FINISHED'}

class VIEW3D_MT_image_drop_menu(Menu):
    bl_label = "Import Image as..."
    bl_idname = "VIEW3D_MT_image_drop_menu"

    def draw(self, context):
        layout = self.layout
        filepath = context.window_manager.get("drop_filepath", "")
        
        op_mesh = layout.operator(VIEW3D_OT_intercept_image_drop.bl_idname, text="Mesh Plane", icon='MESH_PLANE')
        op_mesh.filepath = filepath
        
        op_ref = layout.operator(VIEW3D_OT_import_reference_image.bl_idname, text="Reference", icon='FILE_IMAGE')
        op_ref.filepath = filepath


class VIEW3D_OT_image_drop_router(Operator):
    bl_idname = "view3d.image_drop_router"
    bl_label = "Import Image as..."
    
    filepath: StringProperty(subtype='FILE_PATH')

    def execute(self, context):
        context.window_manager["drop_filepath"] = self.filepath
        bpy.ops.wm.call_menu(name=VIEW3D_MT_image_drop_menu.__name__)
        return {'FINISHED'}

class ImageDropSettings(bpy.types.PropertyGroup):
    size_mode: EnumProperty(
        name="Size Mode", 
        items=[('CAMERA', "Camera", ""), ('ABSOLUTE', "Absolute", ""), ('DPI', "DPI", "")], 
        default='CAMERA'
    )
    shader: EnumProperty(
        name="Shader", 
        items=[('SHADELESS', "Shadeless", ""), ('PRINCIPLED', "Principled", ""), ('EMISSION', "Emission", "")], 
        default='SHADELESS'
    )
    fill_mode: EnumProperty(
        name="Fill Mode",
        items=[('FIT', "Fit", ""), ('FILL', "Fill", "")],
        default='FIT'
    )


class VIEW3D_PT_image_drop_panel(Panel):
    bl_label = "Importer"
    bl_idname = "VIEW3D_PT_image_drop_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SakugaGP'

    def draw(self, context):
        layout = self.layout
        props = context.scene.image_drop_settings
        
        box = layout.box()
        box.label(text="Mesh Plane Import Setting", icon='IMAGE_DATA')
        box.prop(props, "size_mode")
        box.prop(props, "shader")
        box.prop(props, "fill_mode")


class VIEW3D_FH_image_dialog_router(FileHandler):
    bl_idname = "VIEW3D_FH_image_dialog_router"
    bl_label = "Image Drop Dialog Router Handler"
    bl_import_operator = "view3d.image_drop_router"
    bl_file_extensions = ".png;.jpg;.jpeg;.exr;.hdr;.tga;.tiff;.tif;.bmp;.webp"
    
    @classmethod
    def poll_drop(cls, context): 
        return context.area and context.area.type == 'VIEW_3D'


classes = (
    ImageDropSettings,
    VIEW3D_OT_intercept_image_drop,
    VIEW3D_OT_import_reference_image,
    VIEW3D_MT_image_drop_menu,
    VIEW3D_OT_image_drop_router,
    VIEW3D_PT_image_drop_panel,
    VIEW3D_FH_image_dialog_router
)

def register():
    for cls in classes: 
        bpy.utils.register_class(cls)
    bpy.types.Scene.image_drop_settings = bpy.props.PointerProperty(type=ImageDropSettings)

def unregister():
    for cls in reversed(classes): 
        bpy.utils.unregister_class(cls)
        
    if "drop_filepath" in bpy.types.WindowManager:
        del bpy.types.WindowManager["drop_filepath"]
        
    del bpy.types.Scene.image_drop_settings

if __name__ == "__main__": 
    register()
