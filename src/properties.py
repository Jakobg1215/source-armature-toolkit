import bpy


class SourceArmatureToolkitProperties(bpy.types.PropertyGroup):
    def poll_armature(self, object):
        if object.name.endswith(".SAT"):
            return False
        return object.type == 'ARMATURE'

    target_armature: bpy.props.PointerProperty(
        type=bpy.types.Object,
        name="Armature",
        description="Armature that will be used to perform operations on",
        poll=poll_armature
    )

    symmetry_side: bpy.props.EnumProperty(
        name="Affected side",
        description="Side that will be used for applying symmetry constraints",
        items=[
            ("SATSR", "Right", "Left to Right"),
            ("SATSL", "Left", "Right to Left")
        ]
    )

    symmetry_offset: bpy.props.BoolProperty(
        name="Relative Offset",
        description="If disabled, the location of bones will be the opposite of the location of its pair, else its initial locationn ill be unchanged",
        default=False,
    )

    symmetry_fix: bpy.props.BoolProperty(
        name="Opposite Arm Rotation Fix",
        description="If the opposite arm rotates in the wrong direction, enable this",
        default=False,
    )
