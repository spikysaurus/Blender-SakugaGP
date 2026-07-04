bl_info = {
    "name" : "SakugaGP - Exporter",
    "author" : "Sadewoo (Spikysaurus)", 
    "description" : "Exporter",
    "blender" : (5, 0, 0),
    "version" : (0, 2, 1),
    "location" : "",
    "warning" : "",
    "doc_url": "https://spikysaurus.github.io/", 
    "tracker_url": "", 
    "category" : "Animation" 
}

import bpy,os
from bpy.app.handlers import persistent
import bpy.utils.previews

menu = {'sna_check_rotate': False, }

def string_to_icon(value):
    if value in bpy.types.UILayout.bl_rna.functions["prop"].parameters["icon"].enum_items.keys():
        return bpy.types.UILayout.bl_rna.functions["prop"].parameters["icon"].enum_items[value].value
    return string_to_int(value)
    
class SNA_PT_menu_6D4CE(bpy.types.Panel):
    bl_label = 'Exporter'
    bl_idname = 'SNA_PT_menu_6D4CE'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = 'SakugaGP'
    bl_order = 0
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw(self, context):
        layout = self.layout
        col_F0D49 = layout.column(heading='', align=True)
        col_F0D49.alert = False
        col_F0D49.enabled = True
        col_F0D49.active = True
        col_F0D49.use_property_split = False
        col_F0D49.use_property_decorate = False
        col_F0D49.scale_x = 1.0
        col_F0D49.scale_y = 1.0
        col_F0D49.alignment = 'Expand'.upper()
        col_F0D49.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        box_71042 = col_F0D49.box()
        box_71042.alert = False
        box_71042.enabled = True
        box_71042.active = True
        box_71042.use_property_split = False
        box_71042.use_property_decorate = False
        box_71042.alignment = 'Expand'.upper()
        box_71042.scale_x = 1.0
        box_71042.scale_y = 1.0
        if not True: box_71042.operator_context = "EXEC_DEFAULT"
        col_774E9 = box_71042.column(heading='', align=True)
        col_774E9.alert = False
        col_774E9.enabled = True
        col_774E9.active = True
        col_774E9.use_property_split = False
        col_774E9.use_property_decorate = False
        col_774E9.scale_x = 1.0
        col_774E9.scale_y = 1.0
        col_774E9.alignment = 'Expand'.upper()
        col_774E9.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        box_A33AD = col_774E9.box()
        box_A33AD.alert = False
        box_A33AD.enabled = True
        box_A33AD.active = True
        box_A33AD.use_property_split = False
        box_A33AD.use_property_decorate = False
        box_A33AD.alignment = 'Expand'.upper()
        box_A33AD.scale_x = 1.0
        box_A33AD.scale_y = 1.0
        if not True: box_A33AD.operator_context = "EXEC_DEFAULT"
        row_F4F45 = box_A33AD.row(heading='', align=True)
        row_F4F45.alert = False
        row_F4F45.enabled = True
        row_F4F45.active = True
        row_F4F45.use_property_split = False
        row_F4F45.use_property_decorate = False
        row_F4F45.scale_x = 1.0
        row_F4F45.scale_y = 1.0
        row_F4F45.alignment = 'Expand'.upper()
        row_F4F45.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_F4F45.label(text='Antialiasing :', icon_value=0)
        row_83B8C = row_F4F45.row(heading='', align=True)
        row_83B8C.alert = False
        row_83B8C.enabled = True
        row_83B8C.active = True
        row_83B8C.use_property_split = False
        row_83B8C.use_property_decorate = False
        row_83B8C.scale_x = 0.699999988079071
        row_83B8C.scale_y = 1.0
        row_83B8C.alignment = 'Expand'.upper()
        row_83B8C.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        op = row_83B8C.operator('wm.add_antialiasing_b88d6', text='ON', icon_value=0, emboss=True, depress=False)
        op = row_83B8C.operator('wm.remove_antialiasing_bb2ae', text='OFF', icon_value=0, emboss=True, depress=False)
        box_056FA = col_774E9.box()
        box_056FA.alert = False
        box_056FA.enabled = True
        box_056FA.active = True
        box_056FA.use_property_split = False
        box_056FA.use_property_decorate = False
        box_056FA.alignment = 'Expand'.upper()
        box_056FA.scale_x = 1.0
        box_056FA.scale_y = 1.0
        if not True: box_056FA.operator_context = "EXEC_DEFAULT"
        col_26941 = box_056FA.column(heading='', align=True)
        col_26941.alert = False
        col_26941.enabled = True
        col_26941.active = True
        col_26941.use_property_split = False
        col_26941.use_property_decorate = False
        col_26941.scale_x = 1.0
        col_26941.scale_y = 1.0
        col_26941.alignment = 'Expand'.upper()
        col_26941.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_26941.label(text='Set render to :', icon_value=0)
        row_92215 = col_26941.row(heading='', align=True)
        row_92215.alert = False
        row_92215.enabled = True
        row_92215.active = True
        row_92215.use_property_split = False
        row_92215.use_property_decorate = False
        row_92215.scale_x = 1.0
        row_92215.scale_y = 1.0
        row_92215.alignment = 'Expand'.upper()
        row_92215.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        op = row_92215.operator('wm.set_to_mp4_4fc1e', text='MP4', icon_value=0, emboss=True, depress=False)
        op = row_92215.operator('wm.set_to_mov_4c792', text='MOV', icon_value=0, emboss=True, depress=False)
        op = row_92215.operator('wm.set_to_jpg_67847', text='JPG', icon_value=0, emboss=True, depress=False)
        op = row_92215.operator('wm.set_to_png_9c466', text='PNG', icon_value=0, emboss=True, depress=False)
        op = row_92215.operator('wm.set_to_tga_fd0a3', text='TGA', icon_value=0, emboss=True, depress=False)
        col_26941.prop(bpy.context.scene.render, 'film_transparent', text='Transparent', icon_value=string_to_icon('TEXTURE'), emboss=True, toggle=True)
        box_A9121 = col_F0D49.box()
        box_A9121.alert = False
        box_A9121.enabled = True
        box_A9121.active = True
        box_A9121.use_property_split = False
        box_A9121.use_property_decorate = False
        box_A9121.alignment = 'Expand'.upper()
        box_A9121.scale_x = 1.0
        box_A9121.scale_y = 1.0
        if not True: box_A9121.operator_context = "EXEC_DEFAULT"
        box_A9121.label(text='Render Keyframes :', icon_value=0)
        box_A9121.prop(bpy.context.scene, 'sna_frame_number_filenames', text='Name', icon_value=0, emboss=True)
        box_667C9 = box_A9121.box()
        box_667C9.alert = False
        box_667C9.enabled = True
        box_667C9.active = True
        box_667C9.use_property_split = False
        box_667C9.use_property_decorate = False
        box_667C9.alignment = 'Expand'.upper()
        box_667C9.scale_x = 1.0
        box_667C9.scale_y = 1.0
        if not True: box_667C9.operator_context = "EXEC_DEFAULT"
        col_8ED43 = box_667C9.column(heading='', align=True)
        col_8ED43.alert = False
        col_8ED43.enabled = True
        col_8ED43.active = True
        col_8ED43.use_property_split = False
        col_8ED43.use_property_decorate = False
        col_8ED43.scale_x = 1.0
        col_8ED43.scale_y = 1.0
        col_8ED43.alignment = 'Expand'.upper()
        col_8ED43.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        GPData = bpy.context.scene.sna_type_which_gp_to_renderexport
        col_8ED43.prop(bpy.context.scene, 'sna_type_target_layer_data', text='', icon_value=string_to_icon('OUTLINER_DATA_GP_LAYER'), emboss=True)
        col_8ED43.prop(bpy.context.scene, 'sna_type_which_gp_to_renderexport', text='', icon_value=string_to_icon('OUTLINER_DATA_GREASEPENCIL'), emboss=True)
        op = col_8ED43.operator('wm.render_all_keyframes__b07bc', text=str('Render '+'('+GPData+')'), icon_value=string_to_icon('RENDERLAYERS'), emboss=True, depress=False)
        op = col_8ED43.operator('wm.render_layer_keyframes_default_ec843', text='Render Current Layer', icon_value=string_to_icon('RENDERLAYERS'), emboss=True, depress=False)
        op = col_8ED43.operator('wm.export_xdts_457ec', text='Export XDTS', icon_value=string_to_icon('SPREADSHEET'), emboss=True, depress=False)
        op = col_8ED43.operator('wm.copy_text_commands', text='Copy Commands', icon_value=string_to_icon('DUPLICATE'), emboss=True, depress=False)
#        col_E0D27.prop(bpy.context.scene, 'sna_skip_extreme_type', text='Skip Extreme Keyframe', icon_value=0, emboss=True)

class SNA_Copy_Text_Commands(bpy.types.Operator):
    """Copy GP layer 'data' frames as text command, paste this command to auto-sheet : https://moaang.github.io/auto-sheet/"""
    bl_idname = "wm.copy_text_commands"
    bl_label = "Copy GP Layer Data"

    def execute(self, context):
        output_lines = []
        scene = context.scene
        
        GPData = bpy.context.scene.sna_type_which_gp_to_renderexport
        TargetLayerData = bpy.context.scene.sna_type_target_layer_data
        layers = []
        for obj_name in GPData.split(','):
            obj_name = obj_name.strip()  # remove whitespace
            if obj_name in bpy.data.objects:
                layers.append(bpy.data.objects[obj_name])
                
        for obj in layers:
            if TargetLayerData in obj.data.layers:
                layer = obj.data.layers[TargetLayerData]
                frames = layer.frames
                line = obj.name + ": "

                sorted_frames = sorted(frames, key=lambda f: f.frame_number)

                prev_frame = None
                count = 0
                for f in sorted_frames:
                    # Fill gaps with 'n'
                    if prev_frame is not None and f.frame_number > prev_frame + 1:
                        gap = f.frame_number - prev_frame - 1
                        line += " " + " ".join(["n"] * gap)

                    # Encode keyframe type
                    if f.keyframe_type == 'KEYFRAME':
                        count += 1
                        line += " " + str(count)
                    elif f.keyframe_type == 'BREAKDOWN':
                        line += " dot"
                    elif f.keyframe_type == 'EXTREME':
                        line += " x"
                    elif f.keyframe_type == 'MOVING_HOLD':
                        line += " _"
                    elif f.keyframe_type == 'GENERATED':
                        line += " rep"

                    prev_frame = f.frame_number

                output_lines.append(line.strip())

        # Write to Text datablock
        if "GP_Layer_Data" not in bpy.data.texts:
            textblock = bpy.data.texts.new("GP_Layer_Data")
        else:
            textblock = bpy.data.texts["GP_Layer_Data"]

        textblock.clear()
        for line in output_lines:
            textblock.write(line + "\n")

        # Copy to clipboard
        clipboard_text = "\n".join(output_lines)
        bpy.context.window_manager.clipboard = clipboard_text

        self.report({'INFO'}, "Frame data copied to Text Editor and clipboard")
        return {'FINISHED'}


class SNA_OT_Set_To_Mp4_4Fc1E(bpy.types.Operator):
    bl_idname = "wm.set_to_mp4_4fc1e"
    bl_label = "Set to MP4"
    bl_description = "Set output setting to MP4"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        sc = bpy.context.scene
        sc.render.image_settings.media_type = "VIDEO"
        sc.render.ffmpeg.format = "MPEG4"
        sc.render.ffmpeg.codec = "H264"
        sc.render.ffmpeg.audio_codec = "AAC"
        if sc.render.film_transparent == True:
            sc.render.film_transparent = False
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Set_To_Mov_4C792(bpy.types.Operator):
    bl_idname = "wm.set_to_mov_4c792"
    bl_label = "Set to MOV"
    bl_description = "Set output setting to MOV (RGBA)"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        sc = bpy.context.scene
        sc.render.image_settings.media_type = "VIDEO"
        sc.render.ffmpeg.format = "QUICKTIME"
        sc.render.ffmpeg.codec = "QTRLE"
        if sc.render.film_transparent == True:
            sc.render.image_settings.color_mode = "RGBA"
        else :
            sc.render.film_transparent = True
            sc.render.image_settings.color_mode = "RGBA"
        sc.render.ffmpeg.audio_codec = "AAC"
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Set_To_Png_9C466(bpy.types.Operator):
    bl_idname = "wm.set_to_png_9c466"
    bl_label = "Set to PNG"
    bl_description = "Set output setting to PNG"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        sc = bpy.context.scene
        sc.render.image_settings.media_type = "IMAGE"
        sc.render.image_settings.file_format = "PNG"
        if sc.render.film_transparent == True:
            sc.render.image_settings.color_mode = "RGBA"
        else :
            sc.render.image_settings.color_mode = "RGBA"
            sc.render.film_transparent = True
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Render_Layer_Keyframes_Default_Ec843(bpy.types.Operator):
    bl_idname = "wm.render_layer_keyframes_default_ec843"
    bl_label = "Render Layer Keyframes (Default)"
    bl_description = "Only render current layer's keyframes"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        str_filename = bpy.context.scene.sna_frame_number_filenames
        frames = []
        scene = bpy.context.scene
        scene.render.image_settings.media_type = "IMAGE"
        obj = bpy.context.object
        frmt = scene.render.image_settings.file_format
        fp = scene.render.filepath  # Get existing output path
        #scene.render.image_settings.file_format = 'PNG'  # Set output format to .png
        scene.render.image_settings.file_format = frmt
        if scene.render.film_transparent == True:
            scene.render.image_settings.color_mode = 'RGBA'
        else:
            scene.render.image_settings.color_mode = 'RGB'
        if obj.type == 'GREASEPENCIL':
        #    print(obj.data.layers.active)
            for i in obj.data.layers.active.frames:
                path = bpy.context.blend_data.filepath
                frames.append(int(i.frame_number))
            filename_number = 0
            for frame_nr in frames:
                scene.frame_set(frame_nr)  # Set current frame to the desired frame
                if str_filename == 'Counting Numbers':
                    filename_number += 1
                    scene.render.filepath = fp + str(filename_number)
                elif str_filename == 'GP name + Counting Numbers':
                    filename_number += 1
                    scene.render.filepath = fp + obj.name + "_" + str(filename_number).zfill(4)
                elif str_filename == 'Frame Numbers':
                    scene.render.filepath = fp + str(frame_nr)
                elif str_filename == 'GP name + Frame Numbers':
                    scene.render.filepath = fp + obj.name + "_" + str(frame_nr).zfill(4)
        #        scene.render.filepath = fp + "_" + str(frame_nr).zfill(4)  # Set output path to avoid overwriting
                bpy.ops.render.render(write_still=True)  # Render still image
            # Restore the original filepath
            scene.render.filepath = fp
        else:
            self.report({'ERROR'}, 'Select a Grease Pencil Layer !')
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)



class SNA_OT_Export_Xdts_457Ec(bpy.types.Operator):
    bl_idname = "wm.export_xdts_457ec"
    bl_label = "Export XDTS"
    bl_description = "Export Grease Pencils Data's first layer keyframes to XDTS"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        
        import json
        header = "" 
        GPData = bpy.context.scene.sna_type_which_gp_to_renderexport
        layers = GPData.split(',');
        layers_id = []
        dict = {}
        duration = bpy.context.scene.frame_end # total duration (frames)
        fieldIds = [0,3,5]
        _tracks = {}
        _trackNo = layers_id
        timetables_data = []
        
        #-------------------------
        #for x in bpy.data.objects:
        #    if x.type == "GREASEPENCIL":
        #        layers.append(x.name)
        for i in enumerate(layers):
            layers_id.append(i[0])
        #-------------------------
        dict["header"] = {"cut":0,"scene":0}
        dict["timeTables"] = []
        _df = {"duration":duration}
        dict["timeTables"].append(_df)
        _fields = []
        _df["fields"] = _fields
        _ft = {"fieldId":fieldIds[0]}
        _fields.append(_ft)
        _tracks = []
        _ft["tracks"]= _tracks
        _tf={}
        frames_list= []
        #bpy.data.grease_pencils_v3['GPencil.001'].layers['a'].frames
        gg = -1
        for l in layers:
            gg += 1
            for g in bpy.data.grease_pencils:
                if g.name == str(l):
                    _tf = {"trackNo":int(gg)}
                    _tf["frames"] = []
                    _tracks.append(_tf)
                    tt = 0
                    k = {str(g.name) : []}
                    frames_list.append(k)
                    TargetLayerData = bpy.context.scene.sna_type_target_layer_data
                    TLD = g.layers.get(TargetLayerData)
                    
                    for e in TLD.frames:
                        if e.keyframe_type == "KEYFRAME":
                            tt += 1
                            _frames = { "data": [{ "id": 0,"values": [str(tt)] }]}
                        elif e.keyframe_type == "BREAKDOWN":
                            _frames = { "data": [{ "id": 0,"values": ["SYMBOL_TICK_1"] }]}
                        elif e.keyframe_type == "JITTER":
                            _frames = { "data": [{ "id": 0,"values": ["SYMBOL_TICK_2"] }]}
                        elif e.keyframe_type == "MOVING_HOLD":
                            _frames = { "data": [{ "id": 0,"values": ["SYMBOL_HYPHEN"] }]}
                        elif e.keyframe_type == "EXTREME":
                            _frames = { "data": [{ "id": 0,"values": ["SYMBOL_NULL_CELL"] }]}
                        kk = e.frame_number
                        _frames["frame"] = int(kk) - 1
                        _tf["frames"].append(_frames)
                    _frames = { "data": [{ "id": 0,"values": ["SYMBOL_NULL_CELL"] }]}    
                    _frames["frame"] = bpy.context.scene.frame_end
                    _tf["frames"].append(_frames)
        _df["name"] = header
        _df["timeTableHeaders"] = []
        _fn = {"fieldId":0}
        _fn["names"] = layers
        _df["timeTableHeaders"].append(_fn)
        dict["version"] = 5
        js = json.dumps(dict)
        filename = "Timesheet"
        filepath = "//"
        abs_filepath = bpy.path.abspath(filepath) # returns the absolute path
        if not os.path.isdir(str(abs_filepath+"export")): # checks whether the directory exists
            os.mkdir(str(abs_filepath+"export")) # if it does not yet exist, makes it
        fp = open(bpy.path.abspath("//"+"export/"+str(filename)+".xdts"), 'w')
        fp.write("exchangeDigitalTimeSheet Save Data"+js)
        fp.close()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)

class SNA_OT_Set_To_Tga_Fd0A3(bpy.types.Operator):
    bl_idname = "wm.set_to_tga_fd0a3"
    bl_label = "Set to TGA"
    bl_description = "Set output setting to TGA"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        sc = bpy.context.scene
        sc.render.image_settings.media_type = "IMAGE"
        sc.render.image_settings.file_format = "TARGA"
        if sc.render.film_transparent == True:
            sc.render.image_settings.color_mode = "RGBA"
        else :
            sc.render.image_settings.color_mode = "RGBA"
            sc.render.film_transparent = True
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Render_All_Keyframes__B07Bc(bpy.types.Operator):
    bl_idname = "wm.render_all_keyframes__b07bc"
    bl_label = "Render All Keyframes "
    bl_description = "Render All Keyframes from all GPData you typed"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        
        str_filename = bpy.context.scene.sna_frame_number_filenames
        skip_extreme = bpy.context.scene.sna_skip_extreme_type
        filepath = "//"
        abs_filepath = bpy.path.abspath(filepath) # returns the absolute path
        if not os.path.isdir(str(abs_filepath+"export")): # checks whether the directory exists
            os.mkdir(str(abs_filepath+"export")) # if it does not yet exist, makes it
        GPData = bpy.context.scene.sna_type_which_gp_to_renderexport
        layers = GPData.split(',');
        for l in layers:
            for a in bpy.data.objects:
                for b in layers:
                    bpy.data.objects[str(b)].hide_render = True
                bpy.data.objects[str(l)].hide_render = False
        #        print(bpy.data.objects[str(a.name)].name,' = ',bpy.data.objects[str(a.name)].hide_render)
                scene = bpy.context.scene
                if str_filename == 'Counting Numbers' or str_filename == 'Frame Numbers' :
                    filename = ''
                elif str_filename == 'GP name + Counting Numbers' or str_filename == 'GP name + Frame Numbers' : 
                    filename = str(l)
                fp = abs_filepath+"export"+"/"+str(l)+"/"+filename  # Get existing output path
                frmt = scene.render.image_settings.file_format
                scene.render.image_settings.file_format = frmt #PNG
                if scene.render.film_transparent == True:
                    scene.render.image_settings.color_mode = 'RGBA'
                else:
                    scene.render.image_settings.color_mode = 'RGB'
            for b in bpy.data.objects:  
                frames = []
                
                obj = bpy.data.objects[str(b.name)]
                if obj.type == 'GREASEPENCIL':
                    # Get the target layer by name
                    TargetLayerData = bpy.context.scene.sna_type_target_layer_data
                    TLD = obj.data.layers.get(TargetLayerData)
                    if TLD:  # Ensure the layer exists
                        for frame in TLD.frames:
                            if skip_extreme and frame.keyframe_type == "EXTREME":
                                pass
                            else:
                                frames.append(frame.frame_number)

                    if obj.hide_render == False:
        #                print(frames)
                        filename_number = 0
                        for frame_nr in frames:
                            if not os.path.isdir(str(abs_filepath+"export"+"/"+str(l))): # checks whether the directory exists
                                os.mkdir(str(abs_filepath+"export"+"/"+str(l))) # if it does not yet exist, makes it
                            scene.frame_set(frame_nr)  # Set current frame to the desired frame
                            if str_filename == 'Counting Numbers':
                                filename_number += 1
                                scene.render.filepath = abs_filepath+"export"+"/"+str(l)+"/"+str(filename_number)
                            elif str_filename == 'GP name + Counting Numbers':
                                filename_number += 1
                                scene.render.filepath = fp +  "_" + str(filename_number).zfill(4)
                            elif str_filename == 'Frame Numbers':
                                scene.render.filepath = abs_filepath+"export"+"/"+str(l)+"/"+str(frame_nr)
                            elif str_filename == 'GP name + Frame Numbers':
                                scene.render.filepath = fp + "_" + str(frame_nr).zfill(4)
                            bpy.ops.render.render(write_still=True)  # Render still image
                        # Restore the original filepath
                        scene.render.filepath = fp
                    else:
                        pass
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Add_Antialiasing_B88D6(bpy.types.Operator):
    bl_idname = "wm.add_antialiasing_b88d6"
    bl_label = "Add Antialiasing"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        bpy.context.scene.grease_pencil_settings.antialias_threshold_render = 1.0
        bpy.context.scene.grease_pencil_settings.antialias_threshold = 1.0
        bpy.context.scene.render.dither_intensity = 1.0
        bpy.context.scene.grease_pencil_settings.aa_samples = 8
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Remove_Antialiasing_Bb2Ae(bpy.types.Operator):
    bl_idname = "wm.remove_antialiasing_bb2ae"
    bl_label = "Remove Antialiasing"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        bpy.context.scene.grease_pencil_settings.antialias_threshold_render = 0.0
        bpy.context.scene.grease_pencil_settings.antialias_threshold = 0.0
        bpy.context.scene.render.dither_intensity = 0.0
        bpy.context.scene.grease_pencil_settings.aa_samples = 1
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Set_To_Jpg_67847(bpy.types.Operator):
    bl_idname = "wm.set_to_jpg_67847"
    bl_label = "Set to JPG"
    bl_description = "Set output setting to JPG"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        sc = bpy.context.scene
        sc.render.image_settings.media_type = "IMAGE"
        sc.render.image_settings.file_format = "JPEG"
        if sc.render.film_transparent == True:
            sc.render.image_settings.color_mode = "RGB"
            sc.render.film_transparent = False
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)

def register():
    
    bpy.types.Scene.sna_camera_action_1_name = bpy.props.StringProperty(name='Camera Action 1 Name', description='', default='CameraAction', subtype='NONE', maxlen=0)
    bpy.types.Scene.sna_camera_action_2_name = bpy.props.StringProperty(name='Camera Action 2 Name', description='', default='CameraOverscan', subtype='NONE', maxlen=0)
    bpy.types.Scene.sna_toggle_overscan_as_well = bpy.props.BoolProperty(name='Toggle Overscan as well', description='', default=True)
    bpy.types.Scene.sna_type_target_layer_data = bpy.props.StringProperty(name='Target Layer Data', description='Type which layer name as target to export its keyframe data', default='data', subtype='NONE', maxlen=0)
    bpy.types.Scene.sna_type_which_gp_to_renderexport = bpy.props.StringProperty(name='Target Grease Pencils', description='Type which GP to render/export', default='A,B,C', subtype='NONE', maxlen=0)
    bpy.types.Scene.sna_frame_number_filenames = bpy.props.EnumProperty(name='Frame number filenames', description='', items=[('Counting Numbers', 'Counting Numbers', '', 0, 0), ('GP name + Counting Numbers', 'GP name + Counting Numbers', '', 0, 1), ('Frame Numbers', 'Frame Numbers', '', 0, 2), ('GP name + Frame Numbers', 'GP name + Frame Numbers', '', 0, 3)])
    bpy.types.Scene.sna_skip_extreme_type = bpy.props.BoolProperty(name='Skip Extreme Type', description='', default=False)
    bpy.utils.register_class(SNA_PT_menu_6D4CE)
    bpy.utils.register_class(SNA_OT_Set_To_Mp4_4Fc1E)
    bpy.utils.register_class(SNA_OT_Set_To_Mov_4C792)
    bpy.utils.register_class(SNA_OT_Set_To_Png_9C466)
    bpy.utils.register_class(SNA_OT_Render_Layer_Keyframes_Default_Ec843)
    bpy.utils.register_class(SNA_OT_Export_Xdts_457Ec)
    bpy.utils.register_class(SNA_OT_Set_To_Tga_Fd0A3)
    bpy.utils.register_class(SNA_OT_Render_All_Keyframes__B07Bc)
    bpy.utils.register_class(SNA_OT_Add_Antialiasing_B88D6)
    bpy.utils.register_class(SNA_OT_Remove_Antialiasing_Bb2Ae)
    bpy.utils.register_class(SNA_OT_Set_To_Jpg_67847)
    bpy.utils.register_class(SNA_Copy_Text_Commands)
def unregister():
    del bpy.types.Scene.sna_skip_extreme_type
    del bpy.types.Scene.sna_frame_number_filenames
    del bpy.types.Scene.sna_type_target_layer_data
    del bpy.types.Scene.sna_type_which_gp_to_renderexport
    del bpy.types.Scene.sna_show_brush_size_converter_pixel_to_meter
    del bpy.types.Scene.sna_brush_size
    del bpy.types.Scene.sna_toggle_overscan_as_well
    del bpy.types.Scene.sna_camera_action_2_name
    del bpy.types.Scene.sna_camera_action_1_name
    del bpy.types.Scene.sna_camera_action_switch
    bpy.utils.unregister_class(SNA_OT_Link_All_Materials_A41Fe)
    bpy.utils.unregister_class(SNA_OT_Unlink_All_Materials_7Fc01)
    bpy.utils.unregister_class(SNA_OT_Delete_Material_238Fa)
    bpy.utils.unregister_class(SNA_OT_Add_Material_Stroke_Only_S_F198A)
    bpy.utils.unregister_class(SNA_OT_Add_Material_Fill_Only_F_B7E95)
    bpy.utils.unregister_class(SNA_OT_Add_Material_Stroke_And_Fill_B_B_For_Both_581B7)
    bpy.utils.unregister_class(SNA_PT_menu_6D4CE)
    bpy.utils.unregister_class(SNA_OT_Set_To_Mp4_4Fc1E)
    bpy.utils.unregister_class(SNA_OT_Set_To_Mov_4C792)
    bpy.utils.unregister_class(SNA_OT_Set_To_Png_9C466)
    bpy.utils.unregister_class(SNA_OT_Render_Layer_Keyframes_Default_Ec843)
    bpy.utils.unregister_class(SNA_OT_Export_Xdts_457Ec)
    bpy.utils.unregister_class(SNA_OT_Set_To_Tga_Fd0A3)
    bpy.utils.unregister_class(SNA_OT_Render_All_Keyframes__B07Bc)
    bpy.utils.unregister_class(SNA_OT_Add_Antialiasing_B88D6)
    bpy.utils.unregister_class(SNA_OT_Remove_Antialiasing_Bb2Ae)
    bpy.utils.unregister_class(SNA_OT_Set_To_Jpg_67847)
    bpy.utils.unregister_class(SNA_Copy_Text_Commands)
if __name__ == "__main__":
    register()
