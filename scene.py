
import bpy, math, os
from mathutils import Vector

# ============================================================
# C.D. Villa de Buitrago - V4 Blender
# Real 3D stadium scene, animated camera and animated jersey.
# ============================================================

# ---------- clean ----------
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for datablocks in (bpy.data.meshes, bpy.data.curves, bpy.data.materials, bpy.data.cameras, bpy.data.lights):
    pass

# ---------- materials ----------
def mat(name, color, rough=0.6, metallic=0.0, emission=None, emission_strength=0):
    m=bpy.data.materials.new(name)
    m.diffuse_color=(*color,1)
    m.use_nodes=True
    bs=m.node_tree.nodes.get("Principled BSDF")
    bs.inputs["Base Color"].default_value=(*color,1)
    bs.inputs["Roughness"].default_value=rough
    bs.inputs["Metallic"].default_value=metallic
    if emission:
        bs.inputs["Emission Color"].default_value=(*emission,1)
        bs.inputs["Emission Strength"].default_value=emission_strength
    return m

grass=mat("Grass",(0.018,0.20,0.055),.88)
grass2=mat("Grass stripes",(0.025,0.25,0.07),.88)
line_mat=mat("Field lines",(0.92,0.94,0.86),.45)
concrete=mat("Concrete",(0.035,0.045,0.04),.9)
seat_green=mat("Seats green",(0.015,0.16,0.07),.7)
seat_dark=mat("Seats dark",(0.008,0.035,0.02),.8)
metal=mat("Goal metal",(0.82,0.84,0.78),.25,0.55)
net_mat=mat("Goal net",(0.8,0.86,0.80),.8)
gold=mat("Gold",(0.70,0.50,0.06),.35,0.35)
shirt_mat=mat("Villa green shirt",(0.01,0.31,0.09),.48)
shirt_dark=mat("Shirt shadow",(0.005,0.09,0.025),.62)
yellow=mat("Away yellow",(0.88,0.58,0.015),.48)
white=mat("White",(0.9,0.92,0.88),.4)
skin=mat("Skin",(0.42,0.22,0.13),.7)
black=mat("Boots",(0.008,0.01,0.009),.45)
sky=mat("Night",(0.003,0.006,0.004),1)

# ---------- helpers ----------
def cube(name, loc, scale, material, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o=bpy.context.object; o.name=name; o.scale=scale
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if material: o.data.materials.append(material)
    if bevel:
        mod=o.modifiers.new("Soft edges","BEVEL"); mod.width=bevel; mod.segments=3
    return o

def cyl(name, loc, radius, depth, material, vertices=32):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc)
    o=bpy.context.object; o.name=name
    if material:o.data.materials.append(material)
    return o

def curve_line(name, pts, bevel, material):
    cu=bpy.data.curves.new(name,"CURVE"); cu.dimensions="3D"; cu.bevel_depth=bevel; cu.bevel_resolution=2
    sp=cu.splines.new("POLY"); sp.points.add(len(pts)-1)
    for p,co in zip(sp.points,pts): p.co=(*co,1)
    o=bpy.data.objects.new(name,cu); bpy.context.collection.objects.link(o); o.data.materials.append(material)
    return o

# ---------- ground ----------
cube("Stadium ground",(0,-0.35,0),(38,0.35,48),concrete)

# ---------- pitch ----------
cube("Pitch",(0,0,0),(16,0.08,26),grass)

# turf stripes as real surfaces
for i in range(16):
    x=-15 + i*2
    cube("Turf stripe",(x,0.085,0),(1,0.008,25.9),grass2 if i%2 else grass)

# field markings
def field_line(a,b,width=0.09):
    return curve_line("Field line",[a,b],width,line_mat)

field_line((-16,.18,-26),(16,.18,-26),.09)
field_line((-16,.18,26),(16,.18,26),.09)
field_line((-16,.18,-26),(-16,.18,26),.09)
field_line((16,.18,-26),(16,.18,26),.09)
field_line((-16,.18,0),(16,.18,0),.09)

# circles
def circle(name, radius, z, material):
    cu=bpy.data.curves.new(name,"CURVE"); cu.dimensions="3D"; cu.bevel_depth=.085; cu.bevel_resolution=2
    sp=cu.splines.new("POLY"); n=128; sp.points.add(n)
    for i in range(n+1):
        a=2*math.pi*i/n
        sp.points[i].co=(radius*math.cos(a),.18,z+radius*math.sin(a),1)
    o=bpy.data.objects.new(name,cu); bpy.context.collection.objects.link(o); o.data.materials.append(material)
    return o
circle("Center circle",4.8,0,line_mat)
cyl("Center spot",(0,.2,0),.10,.06,line_mat)

# penalty areas
for s in (-1,1):
    z=s*20.5
    # 18.3m wide, 11m deep
    field_line((-9.15,.18,z),(9.15,.18,z),.085)
    field_line((-9.15,.18,z),( -9.15,.18,z-s*5.5),.085)
    field_line((9.15,.18,z),( 9.15,.18,z-s*5.5),.085)
    field_line((-9.15,.18,z-s*5.5),(9.15,.18,z-s*5.5),.085)

# ---------- goals with real posts and net ----------
def goal(z, direction):
    # direction points away from field
    for x in (-4.0,4.0):
        cyl("Goal post",(x,2.05,z),.11,4.1,metal)
    cube("Goal crossbar",(0,4.1,z),(4.1,.11,.11),metal,0.03)
    # depth frame
    back=z+direction*2.4
    for x in (-4.0,4.0):
        cyl("Goal back post",(x,2.05,back),.07,4.1,metal)
    cube("Goal backbar",(0,4.1,back),(4.0,.07,.07),metal)
    # net as translucent-ish grid lines
    for x in range(-4,5):
        curve_line("Net",[(x,0.2,z),(x,4.0,back)],.012,net_mat)
    for y in range(1,5):
        curve_line("Net", [(-4,y,z),(4,y, z)], .012, net_mat)
        curve_line("Net", [(-4,y,back),(4,y,back)], .012, net_mat)
    for x in (-4,4):
        curve_line("Net",[(x,.2,z),(x,4,back)],.012,net_mat)

goal(-26.0,-1)
goal(26.0,1)

# ---------- stands ----------
def stand_block(side):
    sign=1 if side>0 else -1
    base_z=sign*31
    for row in range(7):
        z=base_z + sign*row*1.75
        h=.8+row*.18
        cube("Terrace",(0,h/2,z),(25,.45,0.65),concrete,0.05)
        for x in range(-24,25,2):
            seat=cube("Seat",(x,h+0.35,z-sign*.25),(.72,.25,.32),seat_green if (x+row)%3 else seat_dark,.06)
    # roof
    cube("Stand roof",(0,8.4,sign*43),(28,.25,5.2),concrete,.15)

stand_block(-1); stand_block(1)

def side_stand(side):
    sign=1 if side>0 else -1
    base_x=sign*21
    for row in range(5):
        x=base_x+sign*row*1.5
        h=.8+row*.18
        cube("Side terrace",(x,h/2,0),(.65,.45,25),concrete,.05)
        for z in range(-23,24,2):
            cube("Side seat",(x-sign*.25,h+.35,z),(.32,.25,.72),seat_green if (z+row)%3 else seat_dark,.06)
side_stand(-1); side_stand(1)

# ---------- floodlights ----------
def floodlight(x,z):
    pole=cyl("Floodlight pole",(x,7,z),.16,14,metal)
    cube("Floodlight head",(x,14,z),(1.5,.35,.35),metal,.08)
    for dx in (-1,-.5,0,.5,1):
        lamp=cube("Lamp",(x+dx,14,z-.35),(.18,.18,.08),white,.03)
        lamp.data.materials[0]=mat("Lamp emission",(1,.86,.58),.25,0,(1,.78,.38),7)
floodlight(-25,-25); floodlight(25,-25); floodlight(-25,25); floodlight(25,25)

# ---------- animated jersey, actual 3D ----------
# shirt body as bevelled mesh-like object
body=cube("Jersey body",(0,3.3,0),(1.65,.15,2.05),shirt_mat,.22)
# shoulders and sleeves
left=cube("Left sleeve",(-1.72,3.45,0),(.45,.14,.65),shirt_mat,.18)
right=cube("Right sleeve",(1.72,3.45,0),(.45,.14,.65),shirt_mat,.18)
# collar
cyl("Collar",(0,3.52,-.02),.48,.16,shirt_dark,48)
# lower hem accent
cube("Gold hem",(0,1.35,-.03),(1.55,.05,.10),gold,.04)
# number plate on front
def text_obj(body_text, loc, size, extrude=.015, material=white):
    cu=bpy.data.curves.new(body_text,"FONT"); cu.body=body_text; cu.align_x="CENTER"; cu.align_y="CENTER"
    cu.size=size; cu.extrude=extrude; cu.bevel_depth=.004
    o=bpy.data.objects.new(body_text,cu); bpy.context.collection.objects.link(o); o.location=loc
    o.rotation_euler=(math.pi/2,0,0); o.data.materials.append(material)
    return o
# We want front facing camera at negative Y, so text lies roughly in X-Z plane
num=text_obj("10",(0,-.20,3.55),1.55,.025,gold)
name=text_obj("JUANITO",(0,-.22,2.72),.34,.012,white)
# reposition after text helper creates local orientation
for o in (num,name):
    o.parent=body

# sleeves and body parent to empty
jersey=bpy.data.objects.new("ANIMATED JERSEY",None); bpy.context.collection.objects.link(jersey)
for o in (body,left,right):
    o.parent=jersey
# Texts already parented to body; body moves everything.

jersey.location=(-6,2.0,-7)
jersey.rotation_euler=(math.radians(8),math.radians(-25),math.radians(-5))
jersey.scale=(.85,.85,.85)

# animation: fly in, rotate, settle, float
jersey.keyframe_insert("location",frame=1)
jersey.keyframe_insert("rotation_euler",frame=1)
jersey.keyframe_insert("scale",frame=1)
jersey.location=(3,3.0,-1); jersey.rotation_euler=(0,math.radians(15),math.radians(5)); jersey.scale=(1.0,1.0,1.0)
jersey.keyframe_insert("location",frame=34); jersey.keyframe_insert("rotation_euler",frame=34); jersey.keyframe_insert("scale",frame=34)
jersey.location=(0,2.0,0); jersey.rotation_euler=(0,0,0)
jersey.keyframe_insert("location",frame=60); jersey.keyframe_insert("rotation_euler",frame=60)
jersey.location=(0,2.0,0.25); jersey.keyframe_insert("location",frame=76)
jersey.location=(0,2.0,-0.1); jersey.keyframe_insert("location",frame=92)
jersey.location=(0,2.0,0); jersey.keyframe_insert("location",frame=108)
if jersey.animation_data and jersey.animation_data.action:
    for fc in jersey.animation_data.action.fcurves:
        for kp in fc.keyframe_points: kp.interpolation='BEZIER'

# ---------- camera ----------
bpy.ops.object.camera_add(location=(29,16,-39))
cam=bpy.context.object; cam.name="Cinematic Camera"
cam.data.lens=52
cam.data.dof.use_dof=True
cam.data.dof.focus_object=jersey
cam.data.dof.aperture_fstop=2.8
bpy.context.scene.camera=cam

def look_at(obj, target):
    direction=Vector(target)-obj.location
    obj.rotation_euler=direction.to_track_quat('-Z','Y').to_euler()

look_at(cam,(0,2,0))

cam.keyframe_insert("location",frame=1); cam.keyframe_insert("rotation_euler",frame=1)
cam.location=(18,10,-28); look_at(cam,(0,2,0))
cam.keyframe_insert("location",frame=60); cam.keyframe_insert("rotation_euler",frame=60)
cam.location=(10,8,-20); look_at(cam,(0,2,0))
cam.keyframe_insert("location",frame=144); cam.keyframe_insert("rotation_euler",frame=144)

# ---------- lighting / world ----------
world=bpy.context.scene.world
world.color=(.003,.006,.004)
world.use_nodes=True
world.node_tree.nodes["Background"].inputs["Color"].default_value=(.003,.007,.004,1)
world.node_tree.nodes["Background"].inputs["Strength"].default_value=.18

# area lights imitate stadium beams
for x,z in [(-20,-18),(20,-18),(-20,18),(20,18)]:
    data=bpy.data.lights.new("Stadium light","AREA"); data.energy=1500; data.shape="DISK"; data.size=8
    o=bpy.data.objects.new("Stadium light",data); bpy.context.collection.objects.link(o); o.location=(x,13,z)
    o.rotation_euler=(math.radians(18),0,0)

# warm key
data=bpy.data.lights.new("Key","AREA"); data.energy=900; data.size=10
key=bpy.data.objects.new("Key",data); bpy.context.collection.objects.link(key); key.location=(0,18,-10)
look_at(key,(0,0,0))

# ---------- render settings ----------
sc=bpy.context.scene
sc.frame_start=1; sc.frame_end=144; sc.render.fps=24
sc.render.engine='BLENDER_EEVEE_NEXT'
sc.render.resolution_x=540
sc.render.resolution_y=960
sc.render.resolution_percentage=100
sc.render.image_settings.file_format='FFMPEG'
sc.render.ffmpeg.format='MPEG4'
sc.render.ffmpeg.codec='H264'
sc.render.ffmpeg.constant_rate_factor='MEDIUM'
sc.render.filepath=os.path.abspath("villa-v4-preview.mp4")
sc.render.film_transparent=False
sc.view_settings.look='AgX - Medium High Contrast'

# Motion blur if supported
try:
    sc.render.use_file_extension=True
except: pass

# save blend
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath("villa-v4.blend"))

# render animation
bpy.ops.render.render(animation=True)
