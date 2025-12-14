bl_info = {
    "name" : "SakugaGP - Grease Pencil Exporter",
    "author" : "Sadewoo (Spikysaurus)", 
    "description" : "Exporter",
    "blender" : (5, 0, 0),
    "version" : (0, 0, 0),
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
        op = col_8ED43.operator('wm.render_layer_keyframes_default_ec843', text='Render Current Layer', icon_value=string_to_icon('RENDERLAYERS'), emboss=True, depress=False)
        op = col_8ED43.operator('wm.render_layer_keyframes_svg_3543e', text='Render Current (SVG)', icon_value=string_to_icon('RENDERLAYERS'), emboss=True, depress=False)
        op = col_8ED43.operator('wm.open_output_folder_ac060', text='Open Output Folder', icon_value=string_to_icon('FILE_FOLDER'), emboss=True, depress=False)
        box_CFE72 = box_A9121.box()
        box_CFE72.alert = False
        box_CFE72.enabled = True
        box_CFE72.active = True
        box_CFE72.use_property_split = False
        box_CFE72.use_property_decorate = False
        box_CFE72.alignment = 'Expand'.upper()
        box_CFE72.scale_x = 1.0
        box_CFE72.scale_y = 1.0
        if not True: box_CFE72.operator_context = "EXEC_DEFAULT"
        col_E0D27 = box_CFE72.column(heading='', align=True)
        col_E0D27.alert = False
        col_E0D27.enabled = True
        col_E0D27.active = True
        col_E0D27.use_property_split = False
        col_E0D27.use_property_decorate = False
        col_E0D27.scale_x = 1.0
        col_E0D27.scale_y = 1.0
        col_E0D27.alignment = 'Expand'.upper()
        col_E0D27.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_FFDD1 = col_E0D27.column(heading='', align=True)
        col_FFDD1.alert = True
        col_FFDD1.enabled = True
        col_FFDD1.active = True
        col_FFDD1.use_property_split = False
        col_FFDD1.use_property_decorate = False
        col_FFDD1.scale_x = 1.0
        col_FFDD1.scale_y = 1.0
        col_FFDD1.alignment = 'Expand'.upper()
        col_FFDD1.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_FFDD1.prop(bpy.context.scene, 'sna_type_which_gp_to_renderexport', text='', icon_value=string_to_icon('OUTLINER_DATA_GREASEPENCIL'), emboss=True)
#        col_E0D27.prop(bpy.context.scene, 'sna_skip_extreme_type', text='Skip Extreme Keyframe', icon_value=0, emboss=True)
        GPData = bpy.context.scene.sna_type_which_gp_to_renderexport
        op = col_E0D27.operator('wm.render_all_keyframes__b07bc', text=str('Render '+'('+GPData+')'), icon_value=string_to_icon('RENDERLAYERS'), emboss=True, depress=False)
        op = col_E0D27.operator('wm.export_xdts_457ec', text='Export XDTS', icon_value=string_to_icon('SPREADSHEET'), emboss=True, depress=False)
#        op = col_E0D27.operator('wm.export_opentoonz_647d7', text='Export Opentoonz', icon_value=string_to_icon('BRUSHES_ALL'), emboss=True, depress=False)
#        op = col_E0D27.operator('wm.open_output_folder001_5d731', text='Open Output Folder', icon_value=string_to_icon('FILE_FOLDER'), emboss=True, depress=False)


class SNA_OT_Set_To_Mp4_4Fc1E(bpy.types.Operator):
    bl_idname = "wm.set_to_mp4_4fc1e"
    bl_label = "Set to MP4"
    bl_description = "Set output setting to MP4"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        sc = bpy.context.scene
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

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        sc = bpy.context.scene
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

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        sc = bpy.context.scene
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

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        str_filename = bpy.context.scene.sna_frame_number_filenames
        frames = []
        scene = bpy.context.scene
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
                elif str_filename == 'Layer name + Counting Numbers':
                    filename_number += 1
                    scene.render.filepath = fp + str(obj.data.name) + "_" + str(filename_number).zfill(4)
                elif str_filename == 'Frame Numbers':
                    scene.render.filepath = fp + str(frame_nr)
                elif str_filename == 'Layer name + Frame Numbers':
                    scene.render.filepath = fp + str(obj.data.name) + "_" + str(frame_nr).zfill(4)
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

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        GPData = bpy.context.scene.sna_type_which_gp_to_renderexport
        import json
        header = "" 
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
            for g in bpy.data.grease_pencils_v3:
                if g.name == str(l):
                    _tf = {"trackNo":int(gg)}
                    _tf["frames"] = []
                    _tracks.append(_tf)
                    tt = 0
                    k = {str(g.name) : []}
                    frames_list.append(k)
                    for e in g.layers[0].frames:
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


class SNA_OT_Render_Layer_Keyframes_Svg_3543E(bpy.types.Operator):
    bl_idname = "wm.render_layer_keyframes_svg_3543e"
    bl_label = "Render Layer Keyframes (SVG)"
    bl_description = "Only render current layer's keyframes in SVG format"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        str_filename = bpy.context.scene.sna_frame_number_filenames
        frames = []
        scene = bpy.context.scene
        obj = bpy.context.object
        fp = scene.render.filepath  # Get existing output path
        if obj.type == 'GREASEPENCIL':
        #    print(obj.data.layers.active)
            for i in obj.data.layers.active.frames:
                path = bpy.context.blend_data.filepath
                frames.append(int(i.frame_number))
            filename_number = 0
            for frame_nr in frames:
                scene.frame_set(frame_nr)  # Set current frame to the desired frame
                srf = ''
                if str_filename == 'Counting Numbers':
                    filename_number += 1
                    srf = fp + str(filename_number) + ".svg"
                elif str_filename == 'Layer name + Counting Numbers':
                    filename_number += 1
                    srf = fp + str(obj.data.name) + "_" + str(filename_number).zfill(4) + ".svg"
                elif str_filename == 'Frame Numbers':
                    srf = fp + str(frame_nr)
                elif str_filename == 'Layer name + Frame Numbers':
                    srf = fp + str(obj.data.name) + "_" + str(frame_nr).zfill(4) + ".svg"
                bpy.ops.wm.grease_pencil_export_svg(
                    filepath=srf, 
                    check_existing=True, 
                    filter_blender=False, 
                    filter_backup=False, 
                    filter_image=False, 
                    filter_movie=False, 
                    filter_python=False, 
                    filter_font=False, 
                    filter_sound=False, 
                    filter_text=False, 
                    filter_archive=False, 
                    filter_btx=False, 
                    filter_collada=False, 
                    filter_alembic=False, 
                    filter_usd=False, 
                    filter_obj=True, 
                    filter_volume=False, 
                    filter_folder=True, 
                    filter_blenlib=False, 
        #            filemode=8, 
                    display_type='DEFAULT', 
        #            sort_method='', 
                    use_fill=True, 
                    selected_object_type='VISIBLE', 
                    stroke_sample=0.0, 
                    use_uniform_width=False, 
                    use_clip_camera=False
                    )
            # Restore the original filepath
            scene.render.filepath = fp
        else:
            self.report({'ERROR'}, 'Select a Grease Pencil Layer !')
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Set_To_Tga_Fd0A3(bpy.types.Operator):
    bl_idname = "wm.set_to_tga_fd0a3"
    bl_label = "Set to TGA"
    bl_description = "Set output setting to TGA"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        sc = bpy.context.scene
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

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        GPData = bpy.context.scene.sna_type_which_gp_to_renderexport
        str_filename = bpy.context.scene.sna_frame_number_filenames
        skip_extreme = bpy.context.scene.sna_skip_extreme_type
        filepath = "//"
        abs_filepath = bpy.path.abspath(filepath) # returns the absolute path
        if not os.path.isdir(str(abs_filepath+"export")): # checks whether the directory exists
            os.mkdir(str(abs_filepath+"export")) # if it does not yet exist, makes it
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
                elif str_filename == 'Layer name + Counting Numbers' or str_filename == 'Layer name + Frame Numbers' : 
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
                #    print(obj.data.layers.active)
                    for i in obj.data.layers.active.frames:
                        if skip_extreme == True and i.keyframe_type == "EXTREME":
                            pass
                        else:
                            path = bpy.context.blend_data.filepath
                            frames.append(int(i.frame_number))
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
                            elif str_filename == 'Layer name + Counting Numbers':
                                filename_number += 1
                                scene.render.filepath = fp + "_" + str(filename_number).zfill(4)
                            elif str_filename == 'Frame Numbers':
                                scene.render.filepath = abs_filepath+"export"+"/"+str(l)+"/"+str(frame_nr)
                            elif str_filename == 'Layer name + Frame Numbers':
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

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.context.scene.grease_pencil_settings.antialias_threshold_render = 1.0
        bpy.context.scene.grease_pencil_settings.antialias_threshold = 1.0
        bpy.context.scene.render.dither_intensity = 1.0
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Remove_Antialiasing_Bb2Ae(bpy.types.Operator):
    bl_idname = "wm.remove_antialiasing_bb2ae"
    bl_label = "Remove Antialiasing"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        bpy.context.scene.grease_pencil_settings.antialias_threshold_render = 0.0
        bpy.context.scene.grease_pencil_settings.antialias_threshold = 0.0
        bpy.context.scene.render.dither_intensity = 0.0
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


#class SNA_OT_Open_Output_Folder001_5D731(bpy.types.Operator):
#    bl_idname = "wm.open_output_folder001_5d731"
#    bl_label = "Open Output Folder.001"
#    bl_description = ""
#    bl_options = {"REGISTER", "UNDO"}

#    @classmethod
#    def poll(cls, context):
#        if bpy.app.version >= (3, 0, 0) and True:
#            cls.poll_message_set('')
#        return not False

#    def execute(self, context):
#        import os
#        # Get the path of the currently open .blend file
#        current_blend_file = bpy.data.filepath
#        if current_blend_file:
#            # Get the directory of the .blend file
#            project_folder = os.path.dirname(current_blend_file)
#            # Open the folder using external_operation
#            bpy.ops.file.external_operation(filepath=project_folder, operation='FOLDER_OPEN')
#        else:
#            print("No .blend file is currently open.")
#        return {"FINISHED"}

#    def invoke(self, context, event):
#        return self.execute(context)


class SNA_OT_Set_To_Jpg_67847(bpy.types.Operator):
    bl_idname = "wm.set_to_jpg_67847"
    bl_label = "Set to JPG"
    bl_description = "Set output setting to JPG"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        sc = bpy.context.scene
        sc.render.image_settings.file_format = "JPEG"
        if sc.render.film_transparent == True:
            sc.render.image_settings.color_mode = "RGB"
            sc.render.film_transparent = False
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


#class SNA_OT_Open_Output_Folder_Ac060(bpy.types.Operator):
#    bl_idname = "wm.open_output_folder_ac060"
#    bl_label = "Open Output Folder"
#    bl_description = ""
#    bl_options = {"REGISTER", "UNDO"}

#    @classmethod
#    def poll(cls, context):
#        if bpy.app.version >= (3, 0, 0) and True:
#            cls.poll_message_set('')
#        return not False

#    def execute(self, context):
#        import os
#        # Get the path of the currently open .blend file
#        sc = bpy.context.scene
#        current_blend_file = bpy.data.filepath
#        if current_blend_file:
#            # Get the directory of the .blend file
#            project_folder = sc.render.filepath
#            # Open the folder using external_operation
#            bpy.ops.file.external_operation(filepath=project_folder, operation='FOLDER_OPEN')
#        else:
#            print("No .blend file is currently open.")
#        return {"FINISHED"}

#    def invoke(self, context, event):
#        return self.execute(context)


class SNA_OT_Export_Opentoonz_647D7(bpy.types.Operator):
    bl_idname = "wm.export_opentoonz_647d7"
    bl_label = "Export Opentoonz"
    bl_description = "Export Opentoonz Project File"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        GPData = bpy.context.scene.sna_type_which_gp_to_renderexport
        skip_extreme = bpy.context.scene.sna_skip_extreme_type
        import xml.etree.ElementTree as ET
        sc = bpy.context.scene
        sc.render.image_settings.file_format = "TIFF"
        if sc.render.film_transparent == True:
            sc.render.image_settings.color_mode = "RGBA"
        else :
            sc.render.image_settings.color_mode = "RGBA"
            sc.render.film_transparent = True
        filepath = "//"
        abs_filepath = bpy.path.abspath(filepath) # returns the absolute path
        f_opentoonz = str(abs_filepath+"opentoonz")
        f_drawings = str(abs_filepath+"opentoonz"+"/"+"drawings")
        f_extras = str(abs_filepath+"opentoonz"+"/"+"extras")
        f_inputs = str(abs_filepath+"opentoonz"+"/"+"inputs")
        f_outputs = str(abs_filepath+"opentoonz"+"/"+"outputs")
        f_palettes = str(abs_filepath+"opentoonz"+"/"+"palettes")
        f_scenes = str(abs_filepath+"opentoonz"+"/"+"scenes")
        f_scripts = str(abs_filepath+"opentoonz"+"/"+"scripts")
        file_paths = [f_drawings,f_extras,f_inputs,f_outputs,f_palettes,f_scenes,f_scripts]

        def xml_scenes():
            for i in file_paths:
                if not os.path.isdir(i): # checks whether the directory exists
                    os.mkdir(i) # if it does not yet exist, makes it
                    xml_content = """<parentProject type="projectFolder">".."</parentProject> """
                    file_name = "scenes.xml"
                    full_path = os.path.join(i, file_name)
                    with open(full_path, "w", encoding="utf-8") as file:
                        file.write(xml_content)

        def xml_otprj():
            xml_content = """<project>
          <version>
            70 1 
          </version>
          <folders>
            <folder name="inputs" path="inputs"/>
            <folder name="drawings" path="drawings"/>
            <folder name="scenes" path="scenes"/>
            <folder name="extras" path="extras"/>
            <folder name="outputs" path="outputs"/>
            <folder name="palettes" path="palettes"/>
            <folder name="scripts" path="scripts"/>
            </folders>
          <sceneProperties>
            <outputs>
              <output name="main">
                <range>
                  0 -1 
                </range>
                <step>
                  1 
                </step>
                <shrink>
                  1 
                </shrink>
                <applyShrinkToViewer>
                  0 
                </applyShrinkToViewer>
                <fps>
                  24 
                </fps>
                <path>
                  "+outputs/.tif"
                </path>
                <bpp>
                  32 
                </bpp>
                <multimedia>
                  0 
                </multimedia>
                <threadsIndex>
                  2 
                </threadsIndex>
                <maxTileSizeIndex>
                  0 
                </maxTileSizeIndex>
                <subcameraPrev>
                  0 
                </subcameraPrev>
                <stereoscopic>
                  0 0.05 
                </stereoscopic>
                <resquality>
                  0 
                </resquality>
                <fieldprevalence>
                  0 
                </fieldprevalence>
                <gamma>
                  1 
                </gamma>
                <timestretch>
                  25 25 
                </timestretch>
                <formatsProperties>
                  <formatProperties ext="tif">
                    <property name="Byte Ordering" type="enum" value="Mac">
                      <item value="IBM PC"/>
                      <item value="Mac"/>
                      </property>
                    <property name="Compression Type" type="enum" value="Lempel-Ziv and Welch encoding">
                      <item value="Lempel-Ziv and Welch encoding"/>
                      <item value="None"/>
                      <item value="Macintosh Run-length encoding"/>
                      <item value="ThunderScan Run-length encoding"/>
                      <item value="CCITT Group 3 fax encoding"/>
                      <item value="CCITT Group 4 fax encoding"/>
                      <item value="CCITT modified Huffman Run-length encoding"/>
                      <item value="JPEG compression"/>
                      <item value="JPEG compression 6.0"/>
                      <item value="SGILog"/>
                      <item value="SGILog24"/>
                      <item value="8"/>
                      <item value="zip"/>
                      <item value="Unknown"/>
                      </property>
                    <property name="Bits Per Pixel" type="enum" value="32(RGBM)">
                      <item value="24(RGB)"/>
                      <item value="48(RGB)"/>
                      <item value=" 1(BW)"/>
                      <item value=" 8(GREYTONES)"/>
                      <item value="32(RGBM)"/>
                      <item value="64(RGBM)"/>
                      </property>
                    <property name="Orientation" type="enum" value="Top Left">
                      <item value="Top Left"/>
                      <item value="Top Right"/>
                      <item value="Bottom Right"/>
                      <item value="Bottom Left"/>
                      <item value="Left Top"/>
                      <item value="Right Top"/>
                      <item value="Right Bottom"/>
                      <item value="Left Bottom"/>
                      </property>
                    </formatProperties>
                  </formatsProperties>
                </output>
              <output name="preview">
                <range>
                  0 -1 
                </range>
                <step>
                  1 
                </step>
                <shrink>
                  1 
                </shrink>
                <applyShrinkToViewer>
                  0 
                </applyShrinkToViewer>
                <fps>
                  24 
                </fps>
                <path>
                  "+outputs/.tif"
                </path>
                <bpp>
                  32 
                </bpp>
                <syncColorSettings>
                  1 
                </syncColorSettings>
                <multimedia>
                  0 
                </multimedia>
                <threadsIndex>
                  2 
                </threadsIndex>
                <maxTileSizeIndex>
                  0 
                </maxTileSizeIndex>
                <subcameraPrev>
                  0 
                </subcameraPrev>
                <stereoscopic>
                  0 0.05 
                </stereoscopic>
                <resquality>
                  0 
                </resquality>
                <fieldprevalence>
                  0 
                </fieldprevalence>
                <gamma>
                  1 
                </gamma>
                <timestretch>
                  25 25 
                </timestretch>
                <formatsProperties>
                  <formatProperties ext="tif">
                    <property name="Byte Ordering" type="enum" value="Mac">
                      <item value="IBM PC"/>
                      <item value="Mac"/>
                      </property>
                    <property name="Compression Type" type="enum" value="Lempel-Ziv and Welch encoding">
                      <item value="Lempel-Ziv and Welch encoding"/>
                      <item value="None"/>
                      <item value="Macintosh Run-length encoding"/>
                      <item value="ThunderScan Run-length encoding"/>
                      <item value="CCITT Group 3 fax encoding"/>
                      <item value="CCITT Group 4 fax encoding"/>
                      <item value="CCITT modified Huffman Run-length encoding"/>
                      <item value="JPEG compression"/>
                      <item value="JPEG compression 6.0"/>
                      <item value="SGILog"/>
                      <item value="SGILog24"/>
                      <item value="8"/>
                      <item value="zip"/>
                      <item value="Unknown"/>
                      </property>
                    <property name="Bits Per Pixel" type="enum" value="32(RGBM)">
                      <item value="24(RGB)"/>
                      <item value="48(RGB)"/>
                      <item value=" 1(BW)"/>
                      <item value=" 8(GREYTONES)"/>
                      <item value="32(RGBM)"/>
                      <item value="64(RGBM)"/>
                      </property>
                    <property name="Orientation" type="enum" value="Top Left">
                      <item value="Top Left"/>
                      <item value="Top Right"/>
                      <item value="Bottom Right"/>
                      <item value="Bottom Left"/>
                      <item value="Left Top"/>
                      <item value="Right Top"/>
                      <item value="Right Bottom"/>
                      <item value="Left Bottom"/>
                      </property>
                    </formatProperties>
                  </formatsProperties>
                </output>
              </outputs>
            <cleanupParameters>
              <cleanupCamera>
                <cameraSize>
                  16 9 
                </cameraSize>
                <cameraRes>
                  1920 1080 
                </cameraRes>
                <cameraXPrevalence>
                  1 
                </cameraXPrevalence>
                <interestRect>
                  0 0 -1 -1 
                </interestRect>
                </cleanupCamera>
              <cleanupPalette>
                <version>
                  71 0 
                </version>
                <styles>
                  <style>
                    color_0 3 255 255 255 0 
                  </style>
                  <style>
                    color_1 2002 0 0 0 255 0 0 0 255 0 50 70 10 
                  </style>
                  </styles>
                <stylepages>
                  <page>
                    <name>
                      colors 
                    </name>
                    <indices>
                      0 1 
                    </indices>
                    </page>
                  </stylepages>
                <shortcuts>
                  -1 0 1 -1 -1 -1 -1 -1 -1 -1 
                </shortcuts>
                </cleanupPalette>
              <lineProcessing autoAdjust="0" mode="grey" sharpness="90.000000"/>
              <despeckling value="2"/>
              <aaValue value="70"/>
              <closestField value="999.000000"/>
              <fdg name=""/>
              <altBrightnessContrast>
                0 50 
              </altBrightnessContrast>
              <lpNoneFormat>
                tif 
              </lpNoneFormat>
              </cleanupParameters>
            <scanParameters>
              <paper fmt=""/>
              </scanParameters>
            <vectorizerParameters>
              <version>
                71 0 
              </version>
              <outline>
                0 
              </outline>
              <visibilityBits>
                -1 
              </visibilityBits>
              <Centerline>
                <threshold>
                  8 
                </threshold>
                <accuracy>
                  9 
                </accuracy>
                <despeckling>
                  5 
                </despeckling>
                <maxThickness>
                  200 
                </maxThickness>
                <thicknessRatioFirst>
                  100 
                </thicknessRatioFirst>
                <thicknessRatioLast>
                  100 
                </thicknessRatioLast>
                <makeFrame>
                  0 
                </makeFrame>
                <paintFill>
                  0 
                </paintFill>
                <alignBoundaryStrokesDirection>
                  0 
                </alignBoundaryStrokesDirection>
                <naaSource>
                  0 
                </naaSource>
                </Centerline>
              <Outline>
                <despeckling>
                  4 
                </despeckling>
                <accuracy>
                  8 
                </accuracy>
                <adherence>
                  50 
                </adherence>
                <angle>
                  45 
                </angle>
                <relative>
                  25 
                </relative>
                <maxColors>
                  50 
                </maxColors>
                <toneThreshold>
                  128 
                </toneThreshold>
                <transparentColor>
                  255 255 255 255 
                </transparentColor>
                <paintFill>
                  0 
                </paintFill>
                <alignBoundaryStrokesDirection>
                  0 
                </alignBoundaryStrokesDirection>
                </Outline>
              </vectorizerParameters>
            <bgColor>
              255 255 255 0 
            </bgColor>
            <markers>
              6 0 
            </markers>
            <subsampling>
              1 1 
            </subsampling>
            <fieldguide>
              16 1.77778 
            </fieldguide>
            <noteColors>
              255 235 140 255 255 160 120 255 255 180 190 255 135 205 250 255 145 240 145 255 130 255 210 255 150 245 255 255 
            </noteColors>
            </sceneProperties>
          </project>"""
            # Write the XML content to a file
            file_name = "opentoonz_otprj.xml"
            full_path = os.path.join(f_opentoonz, file_name)
            with open(full_path, "w", encoding="utf-8") as file:
                file.write(xml_content)
        columns = ""
        cells = ""
        pegbars = ""
        levels_path = ""
        levels = ""
        columnfxs = ""
        xsheetfxs = ""
        xsheetfxs2 = ""
        outputfxs = ""

        def xml_create_scene():
            CONTENT = """<tnz framecount="""+'"'+str(bpy.context.scene.frame_end)+'"'+""" version="71.1">
          <generator>
            "OpenToonz 1.7.1"
          </generator>
          <properties>
            <cameras>
              <camera>
                <cameraSize>
                  16 9 
                </cameraSize>
                <cameraRes>
                  1920 1080 
                </cameraRes>
                <cameraXPrevalence>
                  1 
                </cameraXPrevalence>
                <interestRect>
                  0 0 -1 -1 
                </interestRect>
                </camera>
              </cameras>
            <outputs>
              <output name="main">
                <range>
                  0 -1 
                </range>
                <step>
                  1 
                </step>
                <shrink>
                  1 
                </shrink>
                <applyShrinkToViewer>
                  0 
                </applyShrinkToViewer>
                <fps>
                  24 
                </fps>
                <path>
                  "+outputs/.tif"
                </path>
                <bpp>
                  32 
                </bpp>
                <multimedia>
                  0 
                </multimedia>
                <threadsIndex>
                  2 
                </threadsIndex>
                <maxTileSizeIndex>
                  0 
                </maxTileSizeIndex>
                <subcameraPrev>
                  0 
                </subcameraPrev>
                <stereoscopic>
                  0 0.05 
                </stereoscopic>
                <resquality>
                  0 
                </resquality>
                <fieldprevalence>
                  0 
                </fieldprevalence>
                <gamma>
                  1 
                </gamma>
                <timestretch>
                  25 25 
                </timestretch>
                <formatsProperties>
                  <formatProperties ext="tif">
                    <property name="Byte Ordering" type="enum" value="Mac">
                      <item value="IBM PC"/>
                      <item value="Mac"/>
                      </property>
                    <property name="Compression Type" type="enum" value="Lempel-Ziv and Welch encoding">
                      <item value="Lempel-Ziv and Welch encoding"/>
                      <item value="None"/>
                      <item value="Macintosh Run-length encoding"/>
                      <item value="ThunderScan Run-length encoding"/>
                      <item value="CCITT Group 3 fax encoding"/>
                      <item value="CCITT Group 4 fax encoding"/>
                      <item value="CCITT modified Huffman Run-length encoding"/>
                      <item value="JPEG compression"/>
                      <item value="JPEG compression 6.0"/>
                      <item value="SGILog"/>
                      <item value="SGILog24"/>
                      <item value="8"/>
                      <item value="zip"/>
                      <item value="Unknown"/>
                      </property>
                    <property name="Bits Per Pixel" type="enum" value="32(RGBM)">
                      <item value="24(RGB)"/>
                      <item value="48(RGB)"/>
                      <item value=" 1(BW)"/>
                      <item value=" 8(GREYTONES)"/>
                      <item value="32(RGBM)"/>
                      <item value="64(RGBM)"/>
                      </property>
                    <property name="Orientation" type="enum" value="Top Left">
                      <item value="Top Left"/>
                      <item value="Top Right"/>
                      <item value="Bottom Right"/>
                      <item value="Bottom Left"/>
                      <item value="Left Top"/>
                      <item value="Right Top"/>
                      <item value="Right Bottom"/>
                      <item value="Left Bottom"/>
                      </property>
                    </formatProperties>
                  </formatsProperties>
                </output>
              <output name="preview">
                <range>
                  0 -1 
                </range>
                <step>
                  1 
                </step>
                <shrink>
                  1 
                </shrink>
                <applyShrinkToViewer>
                  0 
                </applyShrinkToViewer>
                <fps>
                  24 
                </fps>
                <path>
                  "+outputs/.tif"
                </path>
                <bpp>
                  32 
                </bpp>
                <syncColorSettings>
                  1 
                </syncColorSettings>
                <multimedia>
                  0 
                </multimedia>
                <threadsIndex>
                  2 
                </threadsIndex>
                <maxTileSizeIndex>
                  0 
                </maxTileSizeIndex>
                <subcameraPrev>
                  0 
                </subcameraPrev>
                <stereoscopic>
                  0 0.05 
                </stereoscopic>
                <resquality>
                  0 
                </resquality>
                <fieldprevalence>
                  0 
                </fieldprevalence>
                <gamma>
                  1 
                </gamma>
                <timestretch>
                  25 25 
                </timestretch>
                <formatsProperties>
                  <formatProperties ext="tif">
                    <property name="Byte Ordering" type="enum" value="Mac">
                      <item value="IBM PC"/>
                      <item value="Mac"/>
                      </property>
                    <property name="Compression Type" type="enum" value="Lempel-Ziv and Welch encoding">
                      <item value="Lempel-Ziv and Welch encoding"/>
                      <item value="None"/>
                      <item value="Macintosh Run-length encoding"/>
                      <item value="ThunderScan Run-length encoding"/>
                      <item value="CCITT Group 3 fax encoding"/>
                      <item value="CCITT Group 4 fax encoding"/>
                      <item value="CCITT modified Huffman Run-length encoding"/>
                      <item value="JPEG compression"/>
                      <item value="JPEG compression 6.0"/>
                      <item value="SGILog"/>
                      <item value="SGILog24"/>
                      <item value="8"/>
                      <item value="zip"/>
                      <item value="Unknown"/>
                      </property>
                    <property name="Bits Per Pixel" type="enum" value="32(RGBM)">
                      <item value="24(RGB)"/>
                      <item value="48(RGB)"/>
                      <item value=" 1(BW)"/>
                      <item value=" 8(GREYTONES)"/>
                      <item value="32(RGBM)"/>
                      <item value="64(RGBM)"/>
                      </property>
                    <property name="Orientation" type="enum" value="Top Left">
                      <item value="Top Left"/>
                      <item value="Top Right"/>
                      <item value="Bottom Right"/>
                      <item value="Bottom Left"/>
                      <item value="Left Top"/>
                      <item value="Right Top"/>
                      <item value="Right Bottom"/>
                      <item value="Left Bottom"/>
                      </property>
                    </formatProperties>
                  </formatsProperties>
                </output>
              </outputs>
            <cleanupParameters>
              <cleanupCamera>
                <cameraSize>
                  16 9 
                </cameraSize>
                <cameraRes>
                  1920 1080 
                </cameraRes>
                <cameraXPrevalence>
                  1 
                </cameraXPrevalence>
                <interestRect>
                  0 0 -1 -1 
                </interestRect>
                </cleanupCamera>
              <cleanupPalette>
                <version>
                  71 0 
                </version>
                <styles>
                  <style>
                    color_0 3 255 255 255 0 
                  </style>
                  <style>
                    color_1 2002 0 0 0 255 0 0 0 255 0 50 70 10 
                  </style>
                  </styles>
                <stylepages>
                  <page>
                    <name>
                      colors 
                    </name>
                    <indices>
                      0 1 
                    </indices>
                    </page>
                  </stylepages>
                <shortcuts>
                  -1 0 1 -1 -1 -1 -1 -1 -1 -1 
                </shortcuts>
                </cleanupPalette>
              <lineProcessing autoAdjust="0" mode="grey" sharpness="90.000000"/>
              <despeckling value="2"/>
              <aaValue value="70"/>
              <closestField value="999.000000"/>
              <fdg name=""/>
              <altBrightnessContrast>
                0 50 
              </altBrightnessContrast>
              <lpNoneFormat>
                tif 
              </lpNoneFormat>
              </cleanupParameters>
            <scanParameters>
              <paper fmt=""/>
              </scanParameters>
            <vectorizerParameters>
              <version>
                71 0 
              </version>
              <outline>
                0 
              </outline>
              <visibilityBits>
                -1 
              </visibilityBits>
              <Centerline>
                <threshold>
                  8 
                </threshold>
                <accuracy>
                  9 
                </accuracy>
                <despeckling>
                  5 
                </despeckling>
                <maxThickness>
                  200 
                </maxThickness>
                <thicknessRatioFirst>
                  100 
                </thicknessRatioFirst>
                <thicknessRatioLast>
                  100 
                </thicknessRatioLast>
                <makeFrame>
                  0 
                </makeFrame>
                <paintFill>
                  0 
                </paintFill>
                <alignBoundaryStrokesDirection>
                  0 
                </alignBoundaryStrokesDirection>
                <naaSource>
                  0 
                </naaSource>
                </Centerline>
              <Outline>
                <despeckling>
                  4 
                </despeckling>
                <accuracy>
                  8 
                </accuracy>
                <adherence>
                  50 
                </adherence>
                <angle>
                  45 
                </angle>
                <relative>
                  25 
                </relative>
                <maxColors>
                  50 
                </maxColors>
                <toneThreshold>
                  128 
                </toneThreshold>
                <transparentColor>
                  255 255 255 255 
                </transparentColor>
                <paintFill>
                  0 
                </paintFill>
                <alignBoundaryStrokesDirection>
                  0 
                </alignBoundaryStrokesDirection>
                </Outline>
              </vectorizerParameters>
            <bgColor>
              255 255 255 0 
            </bgColor>
            <markers>
              6 0 
            </markers>
            <subsampling>
              1 1 
            </subsampling>
            <fieldguide>
              16 1.77778 
            </fieldguide>
            <noteColors>
              255 235 140 255 255 160 120 255 255 180 190 255 135 205 250 255 145 240 145 255 130 255 210 255 150 245 255 255 
            </noteColors>
            </properties>
          <levelSet>
            <levels>
              """+levels_path+"""
            </levels>
            <folder name="Cast" type="default">
              <levels>
                """+ levels +"""
              </levels>
              </folder>
            <folder name="Audio">
              </folder>
            </levelSet>
          <xsheet>
            <columns>
            """+columns+"""
            </columns>
            <pegbars>
              <pegbar activeboth="yes" id="Camera1">
                <parent handle="B" id="None" parentHandle="B">
                  </parent>
                <isOpened>
                  0 
                </isOpened>
                <center>
                  0 0 0 0 
                </center>
                <status>
                  0 
                </status>
                <sx>
                  <default>
                    1 
                  </default>
                  </sx>
                <sy>
                  <default>
                    1 
                  </default>
                  </sy>
                <sc>
                  <default>
                    1 
                  </default>
                  </sc>
                <nodePos>
                  1.234e+09 5.678e+09 
                </nodePos>
                <camera>
                  <cameraSize>
                    16 9 
                  </cameraSize>
                  <cameraRes>
                    1920 1080 
                  </cameraRes>
                  <cameraXPrevalence>
                    1 
                  </cameraXPrevalence>
                  <interestRect>
                    0 0 -1 -1 
                  </interestRect>
                  </camera>
                </pegbar>
              <pegbar id="Table">
                <parent handle="B" id="None" parentHandle="B">
                  </parent>
                <isOpened>
                  0 
                </isOpened>
                <center>
                  0 0 0 0 
                </center>
                <status>
                  0 
                </status>
                <sx>
                  <default>
                    1 
                  </default>
                  </sx>
                <sy>
                  <default>
                    1 
                  </default>
                  </sy>
                <sc>
                  <default>
                    1 
                  </default>
                  </sc>
                <nodePos>
                  1.234e+09 5.678e+09 
                </nodePos>
                </pegbar>
              """+pegbars+"""
              <grid_dimension>
                1 
              </grid_dimension>
              </pegbars>
            <fxnodes>
              <terminal>
                  """+columnfxs+"""
                </terminal>
              <xsheet>
                """+xsheetfxs+"""
                  <params>
                    </params>
                  <ports>
                    </ports>
                  <numberId>
                    0 
                  </numberId>
                  <name>
                    Xsheet 
                  </name>
                  <fxId>
                    "" 
                  </fxId>
                  <opened>
                    0 
                  </opened>
                </Toonz_xsheetFx>
              </xsheet>
              <output>
                """+outputfxs+"""
                  <params>
                    </params>
                  <ports>
                    <source>
                      """+xsheetfxs2+"""
                    </source>
                    </ports>
                  <numberId>
                    0 
                  </numberId>
                  <name>
                    Output 
                  </name>
                  <fxId>
                    "" 
                  </fxId>
                  <opened>
                    0 
                  </opened>
                </Toonz_outputFx>
              </output>
              <grid_dimension>
                1 
              </grid_dimension>
              </fxnodes>
            </xsheet>
          <history>
            "| #    DATE:       Time:   MACHINE:    USER:           |"
            "| #1   28 Oct 25   15:24                |"
          </history>
          </tnz>"""
            f_name = "scene.tnz"
            filename = os.path.join(f_scenes, f_name)
            with open(filename, "w", encoding="utf-8", newline="\n") as f:
                f.write(CONTENT) 
        if not os.path.isdir(f_opentoonz): # checks whether the directory exists
            os.mkdir(f_opentoonz) # if it does not yet exist, makes it
            layers = GPData.split(',');
            nb = 2
            nb_ = -1
            nbb = 3
            for l in layers:
                nb_ += 1
                nb+=1 + nb_
                nbb+=1 + nb_
                levelz_path = str("<level id='"+str(layers.index(l)+1)+"'>"+str(l)+"<info dpix='"+str(120.000000)+"' dpiy='"+str(120.000000)+"'/><path>"+'"'+"+extras/"+str(l)+"..tif"+'"'+"</path></level>")
                levels_path += levelz_path
                levelz = str("<level id='"+str(layers.index(l)+1)+"'/>")
                levels += levelz
                ##
                pegbarz = str("<pegbar id="+'"'+"Col"+str(layers.index(l)+1)+'"'+"><parent handle="+'"B"'+" id="+'"Table"'+" parentHandle="+'"B"'+"></parent><name>"+str(l)+"</name><isOpened>0</isOpened><center>0 0 0 0</center><status>0</status><sx><default>1</default></sx><sy><default>1</default></sy><sc><default>1</default></sc><nodePos>1.234e+09 5.678e+09</nodePos></pegbar>")
                pegbars += pegbarz
                columnfxz = str("<fxnode><Toonz_columnFx id='"+str(nbb)+"'/></fxnode>")
                columnfxs += columnfxz
                xsheetfxz = str("<Toonz_xsheetFx id='"+str(nbb + 1)+"'>")
                xsheetfxs = xsheetfxz
                outputfxz = str("<Toonz_outputFx id='"+str(nbb + 2)+"'>")
                outputfxs = outputfxz
                xsheetfxz2 = str("<Toonz_xsheetFx id='"+str(nbb + 1)+"'/>")
                xsheetfxs2 = xsheetfxz2
        #        for a in bpy.data.objects:
                for b in layers:
                    bpy.data.objects[str(b)].hide_render = True
                bpy.data.objects[str(l)].hide_render = False
                scene = bpy.context.scene
                fp = abs_filepath+"opentoonz"+"/"+"extras"+"/"  # Get existing output path
        #        for b in bpy.data.objects:
                frames = []
                frames_key = []
                frames_extreme = []
        #            obj = bpy.data.objects[str(b.name)]
                obj = bpy.data.objects[str(l)]
        #            if obj.type == 'GREASEPENCIL':
                for i in obj.data.layers.active.frames:
                    if skip_extreme == True and i.keyframe_type == "EXTREME":
                        frames_extreme.append(int(i.frame_number))
                    else:
                        frames_key.append(int(i.frame_number))
                    path = bpy.context.blend_data.filepath
                    frames.append(int(i.frame_number))
                number = 0
                if obj.hide_render == False:
        #                print(frames)
                    filename_number = 0
                    print(frames_key)
                    for frame_nr in frames_key:
                        scene.frame_set(frame_nr)  # Set current frame to the desired frame
                        filename_number += 1
                        scene.render.filepath = fp + str(l) + "." + str(filename_number).zfill(4)
                        bpy.ops.render.render(write_still=True)  # Render still image
                    scene.render.filepath = fp
                    for idx, elem in enumerate(frames):
                        this_elem = elem
                        next_elem = frames[(idx + 1) % len(frames)]
                        last_elem = frames[-1]
                        if this_elem in frames_key:
                            number += 1 
                        else:pass
                        x = str(number).zfill(4)
                        a = this_elem-1
                        bn = next_elem
                        b =  (bn - a) - 1
                        endn = bpy.context.scene.frame_end
                        end = (endn - a) -1
                        if this_elem == last_elem :
                            cellz = str("<cell>"+str(a)+" "+str(end)+" "+"<level id='"+str(layers.index(l)+1)+"'/>"+x+" "+"0"+" </cell>")
                            cells += cellz
                        elif this_elem in frames_extreme:
                            pass
                        else:
                            cellz = str("<cell>"+str(a)+" "+str(b)+" "+"<level id='"+str(layers.index(l)+1)+"'/>"+x+" "+"0"+" </cell>")
                            cells += cellz
                else:
                    pass
                columnz = str("<levelColumn id='"+str(nb)+"'><status>0</status><cells>"+str(cells)+"</cells><fx><Toonz_columnFx id='"+str(nbb)+"'><params></params><ports></ports><numberId>0 </numberId><name>LevelColumn </name><fxId>"+'""'+"</fxId><opened>0</opened></Toonz_columnFx></fx></levelColumn>")
                columns += columnz  
                cells = ""
            xml_otprj()
            xml_scenes()
            xml_create_scene()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


    
def register():
    
    bpy.types.Scene.sna_camera_action_1_name = bpy.props.StringProperty(name='Camera Action 1 Name', description='', default='CameraAction', subtype='NONE', maxlen=0)
    bpy.types.Scene.sna_camera_action_2_name = bpy.props.StringProperty(name='Camera Action 2 Name', description='', default='CameraOverscan', subtype='NONE', maxlen=0)
    bpy.types.Scene.sna_toggle_overscan_as_well = bpy.props.BoolProperty(name='Toggle Overscan as well', description='', default=True)
    bpy.types.Scene.sna_type_which_gp_to_renderexport = bpy.props.StringProperty(name='Type which GP to render/export', description='', default='A,B,C', subtype='NONE', maxlen=0)
    bpy.types.Scene.sna_frame_number_filenames = bpy.props.EnumProperty(name='Frame number filenames', description='', items=[('Counting Numbers', 'Counting Numbers', '', 0, 0), ('Layer name + Counting Numbers', 'Layer name + Counting Numbers', '', 0, 1), ('Frame Numbers', 'Frame Numbers', '', 0, 2), ('Layer name + Frame Numbers', 'Layer name + Frame Numbers', '', 0, 3)])
    bpy.types.Scene.sna_skip_extreme_type = bpy.props.BoolProperty(name='Skip Extreme Type', description='', default=False)
    bpy.utils.register_class(SNA_PT_menu_6D4CE)
    bpy.utils.register_class(SNA_OT_Set_To_Mp4_4Fc1E)
    bpy.utils.register_class(SNA_OT_Set_To_Mov_4C792)
    bpy.utils.register_class(SNA_OT_Set_To_Png_9C466)
    bpy.utils.register_class(SNA_OT_Render_Layer_Keyframes_Default_Ec843)
    bpy.utils.register_class(SNA_OT_Export_Xdts_457Ec)
    bpy.utils.register_class(SNA_OT_Render_Layer_Keyframes_Svg_3543E)
    bpy.utils.register_class(SNA_OT_Set_To_Tga_Fd0A3)
    bpy.utils.register_class(SNA_OT_Render_All_Keyframes__B07Bc)
    bpy.utils.register_class(SNA_OT_Add_Antialiasing_B88D6)
    bpy.utils.register_class(SNA_OT_Remove_Antialiasing_Bb2Ae)
#    bpy.utils.register_class(SNA_OT_Open_Output_Folder001_5D731)
    bpy.utils.register_class(SNA_OT_Set_To_Jpg_67847)
#    bpy.utils.register_class(SNA_OT_Open_Output_Folder_Ac060)
    bpy.utils.register_class(SNA_OT_Export_Opentoonz_647D7)
def unregister():
    del bpy.types.Scene.sna_skip_extreme_type
    del bpy.types.Scene.sna_frame_number_filenames
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
    bpy.utils.unregister_class(SNA_OT_Render_Layer_Keyframes_Svg_3543E)
    bpy.utils.unregister_class(SNA_OT_Set_To_Tga_Fd0A3)
    bpy.utils.unregister_class(SNA_OT_Render_All_Keyframes__B07Bc)
    bpy.utils.unregister_class(SNA_OT_Add_Antialiasing_B88D6)
    bpy.utils.unregister_class(SNA_OT_Remove_Antialiasing_Bb2Ae)
#    bpy.utils.unregister_class(SNA_OT_Open_Output_Folder001_5D731)
    bpy.utils.unregister_class(SNA_OT_Set_To_Jpg_67847)
#    bpy.utils.unregister_class(SNA_OT_Open_Output_Folder_Ac060)
    bpy.utils.unregister_class(SNA_OT_Export_Opentoonz_647D7)
if __name__ == "__main__":
    register()