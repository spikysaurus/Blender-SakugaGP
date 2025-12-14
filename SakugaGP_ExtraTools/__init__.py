bl_info = {
    "name" : "SakugaGP - Extra Tools",
    "author" : "Sadewoo (Spikysaurus)", 
    "description" : "Extra Tools",
    "blender" : (5, 0, 0),
    "version" : (0, 0, 0),
    "location" : "",
    "warning" : "",
    "doc_url": "https://spikysaurus.github.io/", 
    "tracker_url": "", 
    "category" : "Animation" 
}

import bpy,json,os,sys,subprocess


def string_to_icon(value):
    if value in bpy.types.UILayout.bl_rna.functions["prop"].parameters["icon"].enum_items.keys():
        return bpy.types.UILayout.bl_rna.functions["prop"].parameters["icon"].enum_items[value].value
    return string_to_int(value)
    
# --- Helpers ---
def get_user_library_path():
    prefs = bpy.context.preferences.filepaths
    for lib in prefs.asset_libraries:
        if lib.name == "User Library":
            return lib.path
    return None

def get_toolbar_folder():
    lib_path = get_user_library_path()
    if lib_path:
        parent = os.path.dirname(lib_path)  # go one level up
        folder = os.path.join(parent, "ExtraTools")
        os.makedirs(folder, exist_ok=True)
        return folder
    return None

def get_json_path():
    lib_path = get_user_library_path()
    if lib_path:
        parent = os.path.dirname(lib_path)  # go one level up
        return os.path.join(parent, "ExtraTools.json")
    return None

button_defs = []

# --- Operators ---
class add_button(bpy.types.Operator):
    bl_idname = "wm.add_button"
    bl_label = "Add Custom Button"

    label: bpy.props.StringProperty(name="Button Label", default="NewButton")
    script: bpy.props.StringProperty(name="Python Script", default="print('Hello World!')")

    def invoke(self, context, event):
        # Show a popup dialog with text inputs
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        global button_defs
        folder = get_toolbar_folder()
        if not folder:
            self.report({'ERROR'}, "User Library not found")
            return {'CANCELLED'}

        # Save script to file
        script_filename = f"{self.label.replace(' ', '_')}.py"
        script_path = os.path.join(folder, script_filename)
        try:
            with open(script_path, "w") as f:
                f.write(self.script)
        except Exception as e:
            self.report({'ERROR'}, f"Failed to save script: {e}")
            return {'CANCELLED'}

        # Store button definition
        button_defs.append({"label": self.label, "script_path": script_path})
        self.report({'INFO'}, f"Added button: {self.label}, script saved to {script_path}")
        return {'FINISHED'}

class save_buttons(bpy.types.Operator):
    bl_idname = "wm.save_buttons"
    bl_label = "Save Buttons"

    def execute(self, context):
        path = get_json_path()
        if not path:
            self.report({'ERROR'}, "User Library not found")
            return {'CANCELLED'}
        with open(path, "w") as f:
            json.dump(button_defs, f, indent=4)
        self.report({'INFO'}, f"Saved button definitions to {path}")
        return {'FINISHED'}

class load_buttons(bpy.types.Operator):
    bl_idname = "wm.load_buttons"
    bl_label = "Load Buttons"

    def execute(self, context):
        global button_defs
        path = get_json_path()
        if not path or not os.path.exists(path):
            self.report({'ERROR'}, "JSON file not found in User Library")
            return {'CANCELLED'}
        with open(path, "r") as f:
            button_defs = json.load(f)
        self.report({'INFO'}, f"Loaded {len(button_defs)} buttons")
        return {'FINISHED'}

class exec_button(bpy.types.Operator):
    bl_idname = "wm.exec_button"
    bl_label = "Execute Custom Button"

    script_path: bpy.props.StringProperty()

    def execute(self, context):
        if not os.path.exists(self.script_path):
            self.report({'ERROR'}, f"Script not found: {self.script_path}")
            return {'CANCELLED'}
        try:
            with open(self.script_path, "r") as f:
                code = f.read()
            exec(code, {"bpy": bpy})
            self.report({'INFO'}, f"Executed script: {self.script_path}")
        except Exception as e:
            self.report({'ERROR'}, f"Execution failed: {e}")
            return {'CANCELLED'}
        return {'FINISHED'}
    
presets = {
            "Cut":"import bpy\nbpy.ops.grease_pencil.copy()\nbpy.ops.grease_pencil.delete()",
            "Copy":"import bpy\nbpy.ops.grease_pencil.copy()",
            "Paste":"import bpy\nbpy.ops.grease_pencil.paste()",
            "Delete":"import bpy\nbpy.ops.grease_pencil.delete()",
            "👆": "import bpy\nbpy.ops.object.mode_set(mode='EDIT')\nbpy.ops.wm.tool_set_by_id(name='builtin.select_lasso')",
            "🖍": "import bpy\nbpy.ops.object.mode_set(mode='PAINT_GREASE_PENCIL')\nbpy.ops.wm.tool_set_by_id(name='builtin.brush')",
            "💊": "import bpy\nbpy.ops.object.mode_set(mode='PAINT_GREASE_PENCIL')\nbpy.ops.wm.tool_set_by_id(name='builtin_brush.Erase')",
            "🪣": "import bpy\nbpy.ops.object.mode_set(mode='PAINT_GREASE_PENCIL')\nbpy.ops.wm.tool_set_by_id(name='builtin_brush.Fill')",
            "メ":"import bpy\nbpy.ops.object.mode_set(mode='PAINT_GREASE_PENCIL')\nbpy.ops.wm.tool_set_by_id(name='builtin.trim')",
            "꠹":"import bpy\nbpy.ops.object.mode_set(mode='SCULPT_GREASE_PENCIL')",
            "╱":"import bpy\nbpy.ops.object.mode_set(mode='PAINT_GREASE_PENCIL')\nbpy.ops.wm.tool_set_by_id(name='builtin.line')",
            "🐵":"import bpy\nbpy.ops.object.mode_set(mode='OBJECT')\nbpy.ops.wm.tool_set_by_id(name='builtin.transform')",
            "▲":"import bpy\nbpy.ops.grease_pencil.reorder(direction='TOP')",
            "▼":"import bpy\nbpy.ops.grease_pencil.reorder(direction='BOTTOM')",
            "X":"import bpy\nbpy.ops.transform.mirror(orient_type='GLOBAL', constraint_axis=(True, False, False))",
            "Y":"import bpy\nbpy.ops.transform.mirror(orient_type='GLOBAL', constraint_axis=(False, False, True))",
            "💠":"import bpy\nbpy.ops.object.mode_set(mode='EDIT')\nbpy.ops.wm.tool_set_by_id(name='builtin.move')"
            
        }
        
class load_preset(bpy.types.Operator):
    """Load a predefined preset as a button"""
    bl_idname = "wm.load_preset"
    bl_label = "Load Preset"

    preset: bpy.props.EnumProperty(
        name="Preset",
        items=[
            ("Cut","Cut",""),
            ("Copy","Copy",""),
            ("Paste","Paste",""),
            ("Delete","Delete",""),
            ("👆", "Lasso", "Select with lasso"),
            ("🖍", "Brush", "Grease Pencil brush"),
            ("💊", "Eraser", "Grease Pencil eraser"),
            ("🪣", "Fill", ""),
            ("メ", "Trim", ""),
            ("꠹", "Sculpt", ""),
            ("╱", "Line", ""),
            ("🐵", "Transform Object", ""),
            ("▲", "Reorder Stroke to Top", ""),
            ("▼", "Reorder Stroke to Bottom", ""),
            ("X", "Mirror Stroke Horizontally", ""),
            ("Y", "Mirror Stroke Vertically", ""),
            ("💠", "Transform Stroke", "")
            
        ]
    )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        global button_defs
        folder = get_toolbar_folder()
        if not folder:
            self.report({'ERROR'}, "User Library not found")
            return {'CANCELLED'}

        label = self.preset.capitalize()
        script_filename = f"{label}.py"
        script_path = os.path.join(folder, script_filename)

        try:
            with open(script_path, "w") as f:
                f.write(presets[self.preset])
        except Exception as e:
            self.report({'ERROR'}, f"Failed to save preset script: {e}")
            return {'CANCELLED'}

        button_defs.append({"label": label, "script_path": script_path})
        self.report({'INFO'}, f"Preset '{label}' added, script saved to {script_path}")
        return {'FINISHED'}
class load_all_presets(bpy.types.Operator):
    """Load all predefined presets as buttons"""
    bl_idname = "wm.load_all_presets"
    bl_label = "Load All Presets"

    def execute(self, context):
        global button_defs
        folder = get_toolbar_folder()
        if not folder:
            self.report({'ERROR'}, "User Library not found")
            return {'CANCELLED'}

        

        for label, code in presets.items():
            script_filename = f"{label}.py"
            script_path = os.path.join(folder, script_filename)

            try:
                with open(script_path, "w") as f:
                    f.write(code)
            except Exception as e:
                self.report({'ERROR'}, f"Failed to save preset {label}: {e}")
                continue

            # Avoid duplicates
            if not any(b["label"] == label for b in button_defs):
                button_defs.append({"label": label, "script_path": script_path})

        self.report({'INFO'}, "All presets loaded into toolbar")
        return {'FINISHED'}
    
class Open_Asset_Library_Folder(bpy.types.Operator):
    bl_idname = "wm.open_asset_library_folder"
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
    
# Popover panel (must be standalone, not child)
class Tools_Popover(bpy.types.Panel):
    bl_label = "popover"
    bl_idname = "wm.popover"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
#    bl_category = "SakugaGP"


    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.operator("wm.add_button", text="Add New Button", icon_value=string_to_icon('PLUS'))
        col.operator("wm.load_preset", text="Add Preset Button",icon_value=string_to_icon('PLUS'))
        col.operator("wm.load_all_presets", text="Default Buttons Set",icon_value=string_to_icon('PLUS'))
        col.operator("wm.save_buttons", text="Save JSON", icon_value=string_to_icon('FILE_TICK'))
        col.operator("wm.load_buttons", text="Load JSON", icon_value=string_to_icon('FILE_REFRESH'))
        col.operator('wm.open_asset_library_folder', text='Open JSON Path', icon_value=string_to_icon('FILE_FOLDER'), emboss=True, depress=False)
        
        
        
# Main toolbar panel
class toolbar(bpy.types.Panel):
    bl_label = "ExtraTools"
    bl_idname = "toolbar"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout

        # Popover button (this is what shows up in your toolbar)
        layout.popover('wm.popover', text='Tools', icon_value=string_to_icon('TOOL_SETTINGS'))
        # Grid of dynamic buttons
        grid = layout.grid_flow(columns=2, align=True, row_major=True)
        grid.scale_x = 1.20
        grid.scale_y = 1.20
        for btn in button_defs:
            op = grid.operator("wm.exec_button", text=btn["label"])
            op.script_path = btn["script_path"]


def register():
    bpy.utils.register_class(Open_Asset_Library_Folder)
    bpy.utils.register_class(add_button)
    bpy.utils.register_class(save_buttons)
    bpy.utils.register_class(load_buttons)
    bpy.utils.register_class(load_preset)
    bpy.utils.register_class(load_all_presets)
    bpy.utils.register_class(exec_button)
    bpy.types.VIEW3D_PT_tools_active.prepend(toolbar.draw)
    bpy.utils.register_class(Tools_Popover)
    
    global button_defs
    path = get_json_path()
    if not path or not os.path.exists(path):
        return {'CANCELLED'}
    with open(path, "r") as f:
        button_defs = json.load(f)
    return {'FINISHED'}
   

def unregister():
    bpy.utils.unregister_class(Open_Asset_Library_Folder)
    bpy.utils.unregister_class(add_button)
    bpy.utils.unregister_class(save_buttons)
    bpy.utils.unregister_class(load_buttons)
    bpy.utils.unregister_class(load_preset)
    bpy.utils.unregister_class(load_all_presets)
    bpy.utils.unregister_class(exec_button)
    bpy.types.VIEW3D_PT_tools_active.remove(toolbar.draw)
    bpy.utils.unregister_class(Tools_Popover)
    

if __name__ == "__main__":
    register()
