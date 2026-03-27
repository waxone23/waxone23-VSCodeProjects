import bpy
import random
import math


def create_infinite_tunnel():
    # 1. Clear scene
    if bpy.context.object and bpy.context.object.mode != "OBJECT":
        bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()

    # Settings
    NUM_POINTS = 100
    TUNNEL_LENGTH = 30
    LINE_THICKNESS = 0.15
    FRAMES = 120

    def create_segment(name, offset_z):
        mesh = bpy.data.meshes.new(name + "_Mesh")
        obj = bpy.data.objects.new(name, mesh)
        bpy.context.collection.objects.link(obj)

        verts = [
            (
                random.uniform(-6, 6),
                random.uniform(-6, 6),
                random.uniform(0, TUNNEL_LENGTH),
            )
            for _ in range(NUM_POINTS)
        ]
        edges = []
        for i in range(len(verts)):
            for j in range(i + 1, len(verts)):
                if math.dist(verts[i], verts[j]) < 3.5:
                    edges.append((i, j))

        mesh.from_pydata(verts, edges, [])
        wire = obj.modifiers.new(name="Wire", type="WIREFRAME")
        wire.thickness = LINE_THICKNESS

        # Animation
        obj.location[2] = offset_z
        obj.keyframe_insert(data_path="location", index=2, frame=1)
        obj.location[2] = offset_z - TUNNEL_LENGTH
        obj.keyframe_insert(data_path="location", index=2, frame=FRAMES + 1)

        # Set Linear motion
        if obj.animation_data and obj.animation_data.action:
            curves = (
                obj.animation_data.action.fcurves
                if hasattr(obj.animation_data.action, "fcurves")
                else []
            )
            for fcurve in curves:
                for kp in fcurve.keyframe_points:
                    kp.interpolation = "LINEAR"
        return obj

    # Create two segments for the loop
    create_segment("Plexus_A", 0)
    create_segment("Plexus_B", TUNNEL_LENGTH)

    # Setup Camera
    if "Camera" not in bpy.data.objects:
        bpy.ops.object.camera_add(location=(0, 0, 15), rotation=(0, 0, 0))
    bpy.context.scene.camera = bpy.data.objects["Camera"]
    bpy.context.scene.frame_end = FRAMES


create_infinite_tunnel()
