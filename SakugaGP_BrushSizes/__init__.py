bl_info = {
    "name" : "SakugaGP - Brush Sizes",
    "author" : "Sadewoo (Spikysaurus)", 
    "description" : "Brush Sizes Palette for Grease Pencil",
    "blender" : (5, 0, 0),
    "version" : (0, 0, 0),
    "location" : "",
    "warning" : "",
    "doc_url": "https://spikysaurus.github.io/", 
    "tracker_url": "", 
    "category" : "Animation" 
}

import bpy,os,json,sys,subprocess

from bpy.app.handlers import persistent

brush_sizes = {'sna_brush_sizes_list': [], }

def string_to_icon(value):
    if value in bpy.types.UILayout.bl_rna.functions["prop"].parameters["icon"].enum_items.keys():
        return bpy.types.UILayout.bl_rna.functions["prop"].parameters["icon"].enum_items[value].value
    return string_to_int(value)
class SNA_PT_brush_sizes_AD1C2(bpy.types.Panel):
    bl_label = ''
    bl_idname = 'SNA_PT_brush_sizes_AD1C2'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = 'SakugaGP'
    bl_order = 0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout
        layout.popover('wm.brush_sizes_popover', text='Brush Sizes', icon_value=string_to_icon('TOOL_SETTINGS'))

    def draw(self, context):
        layout = self.layout
        col_D234F = layout.column(heading='', align=False)
        col_D234F.alert = False
        col_D234F.enabled = True
        col_D234F.active = True
        col_D234F.use_property_split = False
        col_D234F.use_property_decorate = False
        col_D234F.scale_x = 1.0
        col_D234F.scale_y = 1.0
        col_D234F.alignment = 'Expand'.upper()
        col_D234F.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        grid_560E5 = col_D234F.grid_flow(columns=6, row_major=True, even_columns=False, even_rows=False, align=True)
        grid_560E5.enabled = True
        grid_560E5.active = True
        grid_560E5.use_property_split = False
        grid_560E5.use_property_decorate = False
        grid_560E5.alignment = 'Expand'.upper()
        grid_560E5.scale_x = 1.0
        grid_560E5.scale_y = 1.0
        if not True: grid_560E5.operator_context = "EXEC_DEFAULT"
        for i_DA934 in range(len(brush_sizes['sna_brush_sizes_list'])):
            op = grid_560E5.operator('wm.brush_sizes_set_14c7c', text=str(int(brush_sizes['sna_brush_sizes_list'][i_DA934] * 400.0)), icon_value=0, emboss=True, depress=False)
            op.sna_size = str(brush_sizes['sna_brush_sizes_list'][i_DA934])
            
class BrushSizes_Popover(bpy.types.Panel):
    bl_label = "popover"
    bl_idname = "wm.brush_sizes_popover"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'

    def draw(self, context):
        layout = self.layout
        col = layout.column(heading='', align=True)
        col.operator('wm.create_brush_sizes_preset_ce1a5', text='New JSON', icon_value=string_to_icon('PLUS'), emboss=True, depress=False)
        col.operator('wm.refresh_5f018', text='Load JSON', icon_value=string_to_icon('FILE_REFRESH'), emboss=True, depress=False)
        col.operator('wm.open_asset_library_folder_d5c7d', text='Open JSON Path', icon_value=string_to_icon('FILE_FOLDER'), emboss=True, depress=False)

class SNA_OT_Refresh_5F018(bpy.types.Operator):
    bl_idname = "wm.refresh_5f018"
    bl_label = "Refresh"
    bl_description = "Load JSON"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        list = None
        #list = [0.0025,0.025,0.05]
        user_lib_index = bpy.context.preferences.filepaths.asset_libraries.find("User Library")
        user_asset_lib = bpy.context.preferences.filepaths.asset_libraries[user_lib_index]
        project_folder = os.path.dirname(user_asset_lib.path)
        output_path = os.path.join(project_folder,"BrushSizes.json")
        json_path = output_path
        json_filepath = json_path
        with open(json_filepath, 'r') as f:
            data = json.load(f)
        list = data['Size'] 
        brush_sizes['sna_brush_sizes_list'] = list
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
    
class SNA_OT_Create_Brush_Sizes_Preset_Ce1A5(bpy.types.Operator):
    bl_idname = "wm.create_brush_sizes_preset_ce1a5"
    bl_label = "Create Brush Sizes Preset"
    bl_description = "Create JSON File"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        import bpy
        # Define the data
        data = {
            "Size": [
                0.005,
                0.0075,
                0.0125,
                0.0175,
                0.025,
                0.0375,
                0.05,
                1,
                2,
                3,
                4,
                5
            ]
        }
        user_lib_index = bpy.context.preferences.filepaths.asset_libraries.find("User Library")
        user_asset_lib = bpy.context.preferences.filepaths.asset_libraries[user_lib_index]
        project_folder = os.path.dirname(user_asset_lib.path)
        # Set the output path (you can customize this)
        output_path = os.path.join(project_folder,"BrushSizes.json")
        # Write the JSON file
        with open(output_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        print(f"JSON file created at: {output_path}")
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
 
class SNA_OT_Brush_Sizes_Set_14C7C(bpy.types.Operator):
    bl_idname = "wm.brush_sizes_set_14c7c"
    bl_label = "Brush Sizes Set"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}
    sna_size: bpy.props.StringProperty(name='Size', description='', default='', subtype='NONE', maxlen=0)

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        Size = self.sna_size
        bpy.context.tool_settings.gpencil_paint.brush.unprojected_size = float(Size)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
    
class SNA_OT_Open_Asset_Library_Folder_D5C7D(bpy.types.Operator):
    bl_idname = "wm.open_asset_library_folder_d5c7d"
    bl_label = "Open Asset Library Folder"
    bl_description = "Open JSON file path"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        name = "User Library"
        prefs = bpy.context.preferences.filepaths
        lib = prefs.asset_libraries.get(name)

        if not lib:
            print(f"Asset library '{name}' not found in preferences.")
            return

        # Resolve to absolute path
        path = bpy.path.abspath(lib.path)

        # Step up one level (parent folder)
        parent_path = os.path.dirname(path)

        if not os.path.isdir(parent_path):
            print(f"Parent path does not exist: {parent_path}")
            return

        # Open folder depending on OS
        if sys.platform == "win32":
            os.startfile(parent_path)
        elif sys.platform == "darwin":  # macOS
            subprocess.Popen(["open", parent_path])
        else:  # Linux
            subprocess.Popen(["xdg-open", parent_path])

        print(f"Opened parent folder: {parent_path}")
        
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
           
@persistent
def load_post_handler_C09B8(dummy):
    exists = None
    # Define the path to the file you want to check
    user_lib_index = bpy.context.preferences.filepaths.asset_libraries.find("User Library")
    user_asset_lib = bpy.context.preferences.filepaths.asset_libraries[user_lib_index]
    project_folder = os.path.dirname(user_asset_lib.path)
    output_path = os.path.join(project_folder,"BrushSizes.json")
    json_path = Path(output_path)
    exists = False
    if json_path.exists():
        exists = True
    else:
        pass
    if exists:
        list = None
        #list = [0.0025,0.025,0.05]
        user_lib_index = bpy.context.preferences.filepaths.asset_libraries.find("User Library")
        user_asset_lib = bpy.context.preferences.filepaths.asset_libraries[user_lib_index]
        project_folder = os.path.dirname(user_asset_lib.path)
        output_path = os.path.join(project_folder,"BrushSizes.json")
        json_path = output_path
        json_filepath = json_path
        with open(json_filepath, 'r') as f:
            data = json.load(f)
        list = data['Size'] 
        brush_sizes['sna_brush_sizes_list'] = list
        
def register():
    bpy.utils.register_class(SNA_PT_brush_sizes_AD1C2)
    bpy.utils.register_class(SNA_OT_Refresh_5F018)
    bpy.utils.register_class(SNA_OT_Brush_Sizes_Set_14C7C)
    bpy.utils.register_class(SNA_OT_Open_Asset_Library_Folder_D5C7D)
    bpy.utils.register_class(SNA_OT_Create_Brush_Sizes_Preset_Ce1A5)
    bpy.utils.register_class(BrushSizes_Popover)
    
    #list = [0.0025,0.025,0.05]
    user_lib_index = bpy.context.preferences.filepaths.asset_libraries.find("User Library")
    user_asset_lib = bpy.context.preferences.filepaths.asset_libraries[user_lib_index]
    project_folder = os.path.dirname(user_asset_lib.path)
    output_path = os.path.join(project_folder,"BrushSizes.json")
    json_path = output_path
    json_filepath = json_path
    with open(json_filepath, 'r') as f:
        data = json.load(f)
    list = data['Size'] 
    brush_sizes['sna_brush_sizes_list'] = list
        
def unregister():
    bpy.utils.unregister_class(SNA_PT_brush_sizes_AD1C2)
    bpy.utils.unregister_class(SNA_OT_Refresh_5F018)
    bpy.utils.unregister_class(SNA_OT_Brush_Sizes_Set_14C7C)
    bpy.utils.unregister_class(SNA_OT_Open_Asset_Library_Folder_D5C7D)
    bpy.utils.unregister_class(SNA_OT_Create_Brush_Sizes_Preset_Ce1A5)
    bpy.utils.unregister_class(BrushSizes_Popover)

    
if __name__ == "__main__":
    register()