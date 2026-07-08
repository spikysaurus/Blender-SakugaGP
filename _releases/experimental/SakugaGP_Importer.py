bl_info={"name":"SakugaGP - Importer","author":"Sadewoo","version":(0,0,2),
"blender":(5,0,0),"location":"View3D > Sidebar > SakugaGP > Importer",
"description":"Import image as mesh/ref via drop or clipboard","category":"Import-Export"}

import bpy,os,sys,subprocess,tempfile,importlib.util,time,uuid
from bpy.props import EnumProperty,StringProperty,CollectionProperty
from bpy.types import Operator,FileHandler,OperatorFileListElement,Menu,Panel

def clip_img(backend="auto"):
    fn=f"{backend}_{int(time.time())}_{uuid.uuid4().hex[:6]}.png"
    p=os.path.join(tempfile.gettempdir(),fn)
    try:
        from PIL import ImageGrab
        if backend in("auto","pil"):
            img=ImageGrab.grabclipboard()
            if img: img.save(p,"PNG"); return p
    except: pass
    if backend in("auto","wl"):
        try: d=subprocess.check_output(["wl-paste","-t","image/png"])
        except: d=None
        if d: open(p,"wb").write(d); return p
    if backend in("auto","xclip"):
        try: d=subprocess.check_output(["xclip","-selection","clipboard","-t","image/png","-o"])
        except: d=None
        if d: open(p,"wb").write(d); return p
    if backend in("auto","copyq"):
        try: d=subprocess.check_output(["copyq","read","image/png"])
        except: d=None
        if d: open(p,"wb").write(d); return p
    try:
        imgs=[os.path.join(tempfile.gettempdir(),f) for f in os.listdir(tempfile.gettempdir())
              if f.lower().endswith((".png",".jpg",".jpeg",".bmp",".tiff",".webp"))]
        if imgs: return max(imgs,key=os.path.getmtime)
    except: pass
    return None

def has_pil(): return importlib.util.find_spec("PIL") is not None

class OT_DropM(Operator):
    bl_idname,bl_label,bl_options="view3d.drop_m","Drop Mesh",{'UNDO'}
    fp:StringProperty(subtype='FILE_PATH');dr:StringProperty(subtype='DIR_PATH',options={'SKIP_SAVE','HIDDEN'})
    fl:CollectionProperty(type=OperatorFileListElement,options={'SKIP_SAVE','HIDDEN'})
    def invoke(self,ctx,e):
        if not self.fp or not os.path.exists(self.fp): return {'CANCELLED'}
        self.dr,base=os.path.dirname(self.fp),os.path.basename(self.fp)
        self.fl.clear();self.fl.add().name=base;return self.execute(ctx)
    def execute(self,ctx):
        s=ctx.scene.set
        f=[{"name":x.name} for x in self.fl] or [{"name":os.path.basename(self.fp)}]
        bpy.ops.image.import_as_mesh_planes(files=f,directory=self.dr,size_mode=s.sz,shader=s.sh,fill_mode=s.flm)
        return {'FINISHED'}

class OT_DropR(Operator):
    bl_idname,bl_label,bl_options="view3d.drop_r","Drop Ref",{'UNDO'}
    fp:StringProperty(subtype='FILE_PATH')
    def execute(self,ctx):
        if not self.fp or not os.path.exists(self.fp): return {'CANCELLED'}
        bpy.ops.object.empty_image_add(filepath=self.fp,background=False,align='VIEW');return {'FINISHED'}

class OT_ClipM(Operator):
    bl_idname,bl_label,bl_options="view3d.clip_m","Mesh Plane",{'UNDO'}
    def execute(self,ctx):
        s=ctx.scene.set;p=clip_img(s.backend)
        if not p: self.report({'WARNING'},"No img");return {'CANCELLED'}
        bpy.ops.image.import_as_mesh_planes(files=[{"name":os.path.basename(p)}],directory=os.path.dirname(p),
            size_mode=s.sz,shader=s.sh,fill_mode=s.flm);return {'FINISHED'}

class OT_ClipR(Operator):
    bl_idname,bl_label,bl_options="view3d.clip_r","Reference",{'UNDO'}
    def execute(self,ctx):
        s=ctx.scene.set;p=clip_img(s.backend)
        if not p: self.report({'WARNING'},"No img");return {'CANCELLED'}
        bpy.ops.object.empty_image_add(filepath=p,background=False,align='VIEW');return {'FINISHED'}

class OT_Pil(Operator):
    bl_idname,bl_label,bl_options="view3d.install_pil","Install Pillow",{'INTERNAL'}
    def execute(self,ctx):
        try: subprocess.check_call([sys.executable,"-m","pip","install","Pillow"]);self.report({'INFO'},"Installed. Restart.")
        except Exception as e: self.report({'ERROR'},f"Fail: {e}");return {'CANCELLED'}
        return {'FINISHED'}

class MT_Drop(Menu):
    bl_label = "Import Image/Video as.."
    bl_idname = "MT_Drop"

    def draw(self, ctx):
        fp = ctx.window_manager.get("drop_fp", "")
        layout = self.layout
        layout.operator(OT_DropM.bl_idname, text="Mesh Plane", icon='MESH_PLANE').fp = fp
        layout.operator(OT_DropR.bl_idname, text="Reference", icon='FILE_IMAGE').fp = fp


class OT_Router(Operator):
    bl_idname,bl_label="view3d.router","Import Image/Video as.."
    fp:StringProperty(subtype='FILE_PATH')
    def execute(self,ctx):
        ctx.window_manager["drop_fp"]=self.fp;bpy.ops.wm.call_menu(name=MT_Drop.__name__);return {'FINISHED'}

class Set(bpy.types.PropertyGroup):
    sz:EnumProperty(name="Size",items=[('CAMERA',"Camera",""),('ABSOLUTE',"Absolute",""),('DPI',"DPI","")],default='CAMERA')
    sh:EnumProperty(name="Shader",items=[('SHADELESS',"Shadeless",""),('PRINCIPLED',"Principled",""),('EMISSION',"Emission","")],default='SHADELESS')
    flm:EnumProperty(name="Fill",items=[('FIT',"Fit",""),('FILL',"Fill","")],default='FIT')
    backend:EnumProperty(name="",
        items=[('auto',"Auto","Detect automatically"),('pil',"Pillow","Windows/macOS"),
               ('wl',"wl-paste","Wayland"),('xclip',"xclip","X11"),('copyq',"CopyQ","CopyQ tool")],
        default='auto')

class PT_Drop(Panel):
    bl_label,bl_idname,bl_space_type,bl_region_type,bl_category="Importer","PT_Drop",'VIEW_3D','UI','SakugaGP'
    def draw(self,ctx):
        s=ctx.scene.set
        b=self.layout.box();b.label(text="Mesh Settings",icon='IMAGE_DATA');b.prop(s,"sz");b.prop(s,"sh");b.prop(s,"flm")
        self.layout.label(text="Clipboard",icon='PASTEDOWN');self.layout.prop(s,"backend")
        if has_pil():
            layout = self.layout
            col = layout.column(align=True)
            col.operator("view3d.clip_m",icon='MESH_PLANE');
            col.operator("view3d.clip_r",icon='FILE_IMAGE')
        else:
            self.layout.label(text="Pillow ❌",icon='ERROR');self.layout.operator("view3d.install_pil",icon='CONSOLE')

class FH_Drop(FileHandler):
    bl_idname,bl_label,bl_import_operator="FH_Drop","Drop Handler","view3d.router"
    bl_file_extensions=".png;.jpg;.jpeg;.exr;.hdr;.tga;.tiff;.tif;.bmp;.webp;.mp4;.mov;.mkv;.avi;.gif;"
    @classmethod
    def poll_drop(cls,ctx): return ctx.area and ctx.area.type=='VIEW_3D'

cls=(Set,OT_DropM,OT_DropR,OT_ClipM,OT_ClipR,OT_Pil,MT_Drop,OT_Router,PT_Drop,FH_Drop)
def register():
    for c in cls:bpy.utils.register_class(c)
    bpy.types.Scene.set=bpy.props.PointerProperty(type=Set)
def unregister():
    for c in reversed(cls):bpy.utils.unregister_class(c)
    del bpy.types.Scene.set

if __name__=="__main__":register()

