bl_info = {
    "name": "SakugaGP - Extras",
    "author": "Sadewoo (Spikysaurus)",
    "description": "Extra stuff for SakugaGP",
    "blender": (5, 0, 0),
    "version": (0, 1, 2),
    "doc_url": "https://spikysaurus.github.io/",
    "category": "Animation"
}

import bpy, bpy.utils.previews

def string_to_icon(value):
    icons = bpy.types.UILayout.bl_rna.functions["prop"].parameters["icon"].enum_items
    return icons[value].value if value in icons.keys() else int(value)

def get_gp_layer_keyframes(obj, skip_flags=None):
    if not obj or obj.type != 'GREASEPENCIL': return []
    layer = obj.data.layers.active
    if not layer: return []
    return sorted(f.frame_number for f in layer.frames
                  if not (skip_flags and (skip_flags.get('NONE') and f.keyframe_type == 'KEYFRAME'
                                          or skip_flags.get(f.keyframe_type))))

class SNA_PT_EXTRAS(bpy.types.Panel):
    bl_label, bl_idname = 'Extras', 'SNA_PT_EXTRAS'
    bl_space_type, bl_region_type, bl_category = 'VIEW_3D', 'UI', 'SakugaGP'
    def draw(self, context): pass

class CycleGPKeyframeJump(bpy.types.Operator):
    bl_idname, bl_label = "screen.cycle_gp_keyframe_jump", "Cycle GP Keyframe Jump"
    next: bpy.props.BoolProperty(default=True)

    def execute(self, context):
        obj, current, wm = context.active_object, context.scene.frame_current, context.window_manager
        skip_flags = {k: getattr(wm, f"skip_{k.lower()}") for k in ['NONE','BREAKDOWN','MOVING_HOLD','EXTREME','JITTER','GENERATED']}
        keyframes = get_gp_layer_keyframes(obj, skip_flags)
        if not keyframes: return self.report({'WARNING'}, "No grease pencil keyframes found") or {'CANCELLED'}
        context.scene.frame_current = (min((f for f in keyframes if f > current), default=keyframes[0])
                                       if self.next else max((f for f in keyframes if f < current), default=keyframes[-1]))
        return {'FINISHED'}

class SNA_PT_ANIMATION(bpy.types.Panel):
    bl_label, bl_idname, bl_parent_id = 'Animation', 'SNA_PT_ANIMATION', 'SNA_PT_EXTRAS'
    bl_space_type, bl_region_type = 'VIEW_3D', 'UI'

    def draw(self, context):
        layout, wm = self.layout, context.window_manager
        
        row = layout.row(align=True)
        row.label(text="Jump to Keyframe :")
        row.operator("screen.cycle_gp_keyframe_jump", text="Prev", icon_value=string_to_icon('FRAME_PREV')).next = False
        row.operator("screen.cycle_gp_keyframe_jump", text="Next", icon_value=string_to_icon('FRAME_NEXT')).next = True

        
        row = layout.row(align=True)
        row.label(text="Skip Type:")
        icon_map = {
            'none': 'KEYTYPE_KEYFRAME_VEC',
            'breakdown': 'KEYTYPE_BREAKDOWN_VEC',
            'moving_hold': 'KEYTYPE_MOVING_HOLD_VEC',
            'extreme': 'KEYTYPE_EXTREME_VEC',
            'jitter': 'KEYTYPE_JITTER_VEC',
            'generated': 'KEYTYPE_GENERATED_VEC'
        }
        for k, icon in icon_map.items():
            row.prop(wm, f"skip_{k}", text="", icon_value=string_to_icon(icon), toggle=True)



import gpu, os, aud
from gpu_extras.batch import batch_for_shader

# --- Properties ---
class CountdownProperties(bpy.types.PropertyGroup):
    image_dir: bpy.props.StringProperty(name="Image Directory", subtype='DIR_PATH')
    audio_file: bpy.props.StringProperty(name="Audio File", subtype='FILE_PATH')
    timer_duration: bpy.props.FloatProperty(name="Frame Duration", default=0.04, min=0.01)
    countdown_hours: bpy.props.IntProperty(name="Hours", default=0, min=0)
    countdown_minutes: bpy.props.IntProperty(name="Minutes", default=30, min=0, max=59)
    countdown_seconds: bpy.props.IntProperty(name="Seconds", default=0, min=0, max=59)
    countdown_label: bpy.props.StringProperty(name="Countdown Label", default="00:00:00")

# --- Globals ---
images, current_index, texture = [], 0, None
shader = gpu.shader.from_builtin('IMAGE')
device, handle, sound = aud.Device(), None, None
countdown_value, draw_handle = 0, None

# --- Drawing (images only) ---
def draw():
    global texture
    if not texture: return
    region = bpy.context.region; w, h = region.width, region.height
    iw, ih = texture.width, texture.height; ia, va = iw/ih, w/h
    sw, sh = (h*ia, h) if ia > va else (w, w/ia)
    x0, y0, x1, y1 = (w-sw)/2, (h-sh)/2, (w+sw)/2, (h+sh)/2
    batch = batch_for_shader(shader, 'TRI_STRIP',
        {"pos": ((x0,y0),(x1,y0),(x0,y1),(x1,y1)), "texCoord": ((0,0),(1,0),(0,1),(1,1))})
    gpu.state.blend_set('ALPHA'); shader.bind(); shader.uniform_sampler("image", texture); batch.draw(shader); gpu.state.blend_set('NONE')

def countdown_timer():
    global countdown_value, handle, sound, draw_handle, texture, current_index
    props = bpy.context.scene.countdown_props
    if countdown_value > 1:
        countdown_value -= 1
        hh, mm, ss = countdown_value // 3600, (countdown_value % 3600) // 60, countdown_value % 60
        props.countdown_label = f"{hh:02}:{mm:02}:{ss:02}"
        redraw(); return 1.0
    countdown_value = 0; props.countdown_label = "00:00:00"

    # Play audio only if loaded
    if sound: handle = device.play(sound)

    # Show images only if loaded
    if images:
        current_index, texture = 0, gpu.texture.from_image(images[0])
        if not draw_handle: draw_handle = bpy.types.SpaceView3D.draw_handler_add(draw, (), 'WINDOW', 'POST_PIXEL')
        bpy.app.timers.register(advance_frame)

    # Always check audio status
    bpy.app.timers.register(check_audio)
    return None

def advance_frame():
    global current_index, texture, images
    props = bpy.context.scene.countdown_props
    if current_index < len(images)-1:
        current_index += 1; texture = gpu.texture.from_image(images[current_index]); redraw(); return props.timer_duration
    texture = None; redraw()
    for img in list(images):
        try: bpy.data.images.remove(img, do_unlink=True)
        except ReferenceError: pass
    images.clear(); return None

def check_audio():
    global handle, sound
    if handle and not handle.status: handle, sound = None, None; return None
    return 0.5

def redraw():
    for area in bpy.context.screen.areas:
        for region in area.regions: region.tag_redraw()

class StartCountdownOperator(bpy.types.Operator):
    bl_idname, bl_label = "wm.start_countdown", ""
    def execute(self, context):
        global images, texture, current_index, sound, countdown_value, handle, draw_handle
        props = context.scene.countdown_props

        # Reset playback
        if handle: handle.stop(); handle = None
        sound, texture = None, None
        if draw_handle: bpy.types.SpaceView3D.draw_handler_remove(draw_handle, 'WINDOW'); draw_handle = None
        for img in list(images):
            try: bpy.data.images.remove(img, do_unlink=True)
            except ReferenceError: pass
        images.clear()
        for fn in (countdown_timer, advance_frame, check_audio):
            try: bpy.app.timers.unregister(fn)
            except ValueError: pass

        # Load images if directory is set
        if props.image_dir and os.path.isdir(props.image_dir):
            images = [bpy.data.images.load(os.path.join(props.image_dir,f))
                      for f in sorted(os.listdir(props.image_dir))
                      if f.lower().endswith((".png",".jpg",".jpeg"))]

        # Load audio if file is set
        if props.audio_file and os.path.isfile(props.audio_file):
            sound = aud.Sound(props.audio_file)

        # Init countdown
        countdown_value = props.countdown_hours*3600 + props.countdown_minutes*60 + props.countdown_seconds
        props.countdown_label = f"{props.countdown_hours:02}:{props.countdown_minutes:02}:{props.countdown_seconds:02}"

        bpy.app.timers.register(countdown_timer)
        return {'FINISHED'}

class StopCountdownOperator(bpy.types.Operator):
    bl_idname, bl_label = "wm.stop_countdown", ""
    def execute(self, context):
        global handle, sound, texture, images, countdown_value, draw_handle
        countdown_value = 0; context.scene.countdown_props.countdown_label = "00:00:00"
        if handle: handle.stop(); handle = None
        sound, texture = None, None
        if draw_handle: bpy.types.SpaceView3D.draw_handler_remove(draw_handle, 'WINDOW'); draw_handle = None
        for img in list(images):
            try: bpy.data.images.remove(img, do_unlink=True)
            except ReferenceError: pass
        images.clear()
        for fn in (countdown_timer, advance_frame, check_audio):
            try: bpy.app.timers.unregister(fn)
            except ValueError: pass
        redraw(); return {'FINISHED'}
    
class Timer_Preferences_popover(bpy.types.Panel):
    bl_idname = "Timer_Preferences_popover"
    bl_label = "Timer Preferences"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'

    def draw(self, context):
        layout, props = self.layout, context.scene.countdown_props
        layout.prop(props,"image_dir")
        layout.prop(props,"audio_file")
        layout.prop(props,"timer_duration")
        row = layout.column(align=True); row.prop(props,"countdown_hours"); row.prop(props,"countdown_minutes"); row.prop(props,"countdown_seconds")
        
        
# --- Panel ---
class CountdownPanel(bpy.types.Panel):
#    bl_label, bl_idname, bl_space_type, bl_region_type, bl_category = "Countdown Player","VIEW3D_PT_countdown","VIEW_3D","UI","Countdown"
    bl_label, bl_idname, bl_parent_id = 'Timer', 'CountdownPanel', 'SNA_PT_EXTRAS'
    bl_space_type, bl_region_type = 'VIEW_3D', 'UI'
    
    def draw(self, context):
        layout, props = self.layout, context.scene.countdown_props

        row = layout.row(align=True)
        row.popover("Timer_Preferences_popover", text="", icon="PREFERENCES") 
        row.operator("wm.start_countdown", icon="PLAY")
        row.operator("wm.stop_countdown", icon="LOOP_BACK")
        row.label(icon="MOD_TIME", text=f"{props.countdown_label}")

_icons = None

classes = [
    SNA_PT_EXTRAS, CycleGPKeyframeJump, SNA_PT_ANIMATION,
    CountdownProperties, StartCountdownOperator, StopCountdownOperator, CountdownPanel,Timer_Preferences_popover
]

def _process_registration(registering=True):
    global _icons
    if registering:
        _icons = bpy.utils.previews.new()
        for cls in classes:
            bpy.utils.register_class(cls)
        bpy.types.Scene.countdown_props = bpy.props.PointerProperty(type=CountdownProperties)
        for k in ['none','breakdown','moving_hold','extreme','jitter','generated']:
            setattr(bpy.types.WindowManager, f"skip_{k}",
                    bpy.props.BoolProperty(name=k.replace('_',' ').title(), default=False))
    else:
        bpy.utils.previews.remove(_icons)
        for k in ['none','breakdown','moving_hold','extreme','jitter','generated']:
            if hasattr(bpy.types.WindowManager, f"skip_{k}"):
                delattr(bpy.types.WindowManager, f"skip_{k}")
        del bpy.types.Scene.countdown_props
        for cls in reversed(classes):
            bpy.utils.unregister_class(cls)

def register():
    _process_registration(registering=True)

def unregister():
    _process_registration(registering=False)

if __name__ == "__main__":
    register()


