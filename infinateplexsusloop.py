import bpy
import random
import math


def create_retina_plexus():
    # 1. CLEANUP: Clear the scene for a fresh start
    if bpy.context.object and bpy.context.object.mode != "OBJECT":
        bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()

    # --- SETTINGS (Modified for High-Resolution Screens) ---
    NUM_POINTS = 80
    TUNNEL_LENGTH = 30
    # BOOSTED THICKNESS: 0.4 is thick enough to see clearly on a Mac
    LINE_THICKNESS = 0.4
    FRAMES = 120

    def create_segment(name, offset_z):
        mesh = bpy.data.meshes.new(name + "_Mesh")
        obj = bpy.data.objects.new(name, mesh)
        bpy.context.collection.objects.link(obj)

        # Generate random points in a 3D volume
        verts = [
            (
                random.uniform(-8, 8),
                random.uniform(-8, 8),
                random.uniform(0, TUNNEL_LENGTH),
            )
            for _ in range(NUM_POINTS)
        ]
        edges = []

        # Connect points that are close to each other
        for i in range(len(verts)):
            for j in range(i + 1, len(verts)):
                if math.dist(verts[i], verts[j]) < 4.5:
                    edges.append((i, j))

        mesh.from_pydata(verts, edges, [])

        # ADD WIREFRAME: This turns the invisible edges into visible "pipes"
        wire = obj.modifiers.new(name="VisibleLines", type="WIREFRAME")
        wire.thickness = LINE_THICKNESS
        wire.use_relative_offset = False

        # ANIMATION: Constant linear motion
        obj.location[2] = offset_z
        obj.keyframe_insert(data_path="location", index=2, frame=1)
        obj.location[2] = offset_z - TUNNEL_LENGTH
        obj.keyframe_insert(data_path="location", index=2, frame=FRAMES + 1)

        # Set Interpolation to LINEAR for a smooth loop
        if obj.animation_data and obj.animation_data.action:
            # Blender 5.0 compatible curve access
            action = obj.animation_data.action
            curves = (
                action.fcurves
                if hasattr(action, "fcurves")
                else getattr(action, "curves", [])
            )
            for fcurve in curves:
                for kp in fcurve.keyframe_points:
                    kp.interpolation = "LINEAR"
        return obj

    # Create two segments to make the loop seamless
    create_segment("Plexus_A", 0)
    create_segment("Plexus_B", TUNNEL_LENGTH)

    # 2. CAMERA SETUP
    if "Camera" not in bpy.data.objects:
        bpy.ops.object.camera_add(location=(0, 0, 15), rotation=(0, 0, 0))

    cam_obj = bpy.data.objects["Camera"]
    bpy.context.scene.camera = cam_obj
    cam_obj.location = (0, 0, 18)
    cam_obj.rotation_euler = (0, 0, 0)
    cam_obj.data.clip_end = 1000  # Make sure we can see the whole tunnel

    # 3. SCENE SETTINGS
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = FRAMES
    bpy.context.scene.frame_set(1)

    print("Retina Plexus Created: Thickened to 0.4 for visibility.")


create_retina_plexus()
