import bpy

from . import properties
from . import interface
from . import operators

bl_info = {
    "name": "Source Armature Toolkit",
    "description": "Various utilities to ease the work while working with Source engine armatures.",
    "author": "Haggets, Jakobg1215",
    "version": (1, 1, 0),
    "blender": (4, 0, 0),
    "location": "Properties > Object Data (Armature)",
    "support": "COMMUNITY",
    "doc_url": "https://github.com/Haggets/source-armature-toolkit/wiki",
    "tracker_url": "https://github.com/jakobg1215/source-armature-toolkit/issues",
    "category": "Rigging"
}


def register():
    bpy.utils.register_class(properties.SourceArmatureToolkitProperties)
    bpy.types.Scene.satproperties = bpy.props.PointerProperty(type=properties.SourceArmatureToolkitProperties)

    bpy.utils.register_class(interface.SATMainPanel)
    bpy.utils.register_class(interface.SATBoneRenamingPanel)
    bpy.utils.register_class(interface.SATSymmetryPanel)
    bpy.utils.register_class(interface.SATWeightArmaturePanel)

    bpy.utils.register_class(operators.SATRenameBonesOperator)
    bpy.utils.register_class(operators.SATRestoreBonesOperator)
    bpy.utils.register_class(operators.SATSymmetryAddOperator)
    bpy.utils.register_class(operators.SATSymmetryRemoveOperator)
    bpy.utils.register_class(operators.SATSymmetryApplyOperator)
    bpy.utils.register_class(operators.SATWeightGenerateOperator)
    bpy.utils.register_class(operators.SATWeightRemoveOperator)


def unregister():
    bpy.utils.unregister_class(properties.SourceArmatureToolkitProperties)
    del bpy.types.Scene.satproperties

    bpy.utils.unregister_class(interface.SATMainPanel)
    bpy.utils.unregister_class(interface.SATBoneRenamingPanel)
    bpy.utils.unregister_class(interface.SATSymmetryPanel)
    bpy.utils.unregister_class(interface.SATWeightArmaturePanel)

    bpy.utils.unregister_class(operators.SATRenameBonesOperator)
    bpy.utils.unregister_class(operators.SATRestoreBonesOperator)
    bpy.utils.unregister_class(operators.SATSymmetryAddOperator)
    bpy.utils.unregister_class(operators.SATSymmetryRemoveOperator)
    bpy.utils.unregister_class(operators.SATSymmetryApplyOperator)
    bpy.utils.unregister_class(operators.SATWeightGenerateOperator)
    bpy.utils.unregister_class(operators.SATWeightRemoveOperator)


if __name__ == "__main__":
    register()
