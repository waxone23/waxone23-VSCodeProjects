import bpy
import random


def create_wax_films_cinematic():
    # 1. CLEANUP: Wipe the slate clean
    if bpy.context.object and bpy.context.object.mode != "OBJECT":
        bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()

    # 2. THE LOGO: Create 3D Text
    bpy.ops.object.text_add(location=(0, 0, 1))
    text_obj = bpy.context.object
    text_obj.data.body = "WAX FILMS"
    text_obj.name = "WaxFilms_Text"

    # Typography settings for a high-end feel
    text_obj.data.extrude = 0.25
    text_obj.data.bevel_depth = 0.03
    text_obj.data.align_x = "CENTER"
    text_obj.data.align_y = "CENTER"
    text_obj.rotation_euler[0] = 1.5708  # 90 degrees

    # 3. REFLECTIVE FLOOR
    bpy.ops.mesh.primitive_plane_add(size=100, location=(0, 0, 0))
    floor = bpy.context.object
    floor.name = "Studio_Floor"

    # 4. MATERIALS: Neon Glow & Dark Mirror
    # Neon Material (Electric Blue)
    neon_mat = bpy.data.materials.new(name="Neon_Wax")
    neon_mat.use_nodes = True
    nodes = neon_mat.node_tree.nodes
    nodes.clear()

    node_emiss = nodes.new(type="ShaderNodeEmission")
    node_emiss.inputs[0].default_value = (0.05, 0.4, 1.0, 1.0)  # Blue
    node_emiss.inputs[1].default_value = 25.0  # Strong brightness

    node_out = nodes.new(type="ShaderNodeOutputMaterial")
    neon_mat.node_tree.links.new(node_emiss.outputs[0], node_out.inputs[0])
    text_obj.data.materials.append(neon_mat)

    # Mirror Floor Material
    floor_mat = bpy.data.materials.new(name="Mirror_Floor")
    floor_mat.use_nodes = True
    f_nodes = floor_mat.node_tree.nodes
    # Standard Principled BSDF setup
    bsdf = f_nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (0.01, 0.01, 0.01, 1)  # Black
    bsdf.inputs["Roughness"].default_value = 0.05  # Sharp reflection
    bsdf.inputs["Metallic"].default_value = 1.0
    floor.data.materials.append(floor_mat)

    # 5. RENDER SETTINGS (The Fix for the Error)
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"  # Changed from 'BLENDER_EEVEE_NEXT'

    # Darken World background for better contrast
    scene.world.use_nodes = True
    scene.world.node_tree.nodes["Background"].inputs[0].default_value = (0, 0, 0, 1)

    # Enable Bloom for the glow
    if hasattr(scene.eevee, "use_bloom"):
        scene.eevee.use_bloom = True
    if hasattr(scene.eevee, "use_ssr"):
        scene.eevee.use_ssr = True

    # 6. CAMERA & ANIMATION
    bpy.ops.object.camera_add(location=(0, -12, 3), rotation=(1.45, 0, 0))
    cam = bpy.context.object
    scene.camera = cam

    # Keyframe the camera push-in
    cam.keyframe_insert(data_path="location", frame=1)
    cam.location = (0, -7.5, 2.2)
    cam.keyframe_insert(data_path="location", frame=120)

    # 7. LIGHTING: Area light to catch the top bevels
    bpy.ops.object.light_add(type="AREA", location=(0, -2, 6))
    top_light = bpy.context.object
    top_light.data.energy = 200
    top_light.scale = (10, 2, 1)

    print("WAX FILMS Scene generated successfully.")


create_wax_films_cinematic()
