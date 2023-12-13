import bpy

BONE_PREFIX = "ValveBiped.Bip01_"


class SATRenameBonesOperator(bpy.types.Operator):
    bl_idname = "sat.rename_bones"
    bl_label = "Convert"

    def execute(self, context):
        properties = context.scene.satproperties
        armature_data = properties.target_armature.data

        valvebones = []

        for bone in armature_data.bones:
            if bone.name.startswith(BONE_PREFIX):
                valvebones.append(bone)

        for bone in valvebones:
            bone_name = bone.name[len(BONE_PREFIX):]

            if bone_name.startswith("L_"):
                bone_name_trimmed = bone_name[len("L"):]

                bone.name = "ValveBiped.Bip01" + bone_name_trimmed + "_L"

            if bone_name.startswith("R_"):
                bone_name_trimmed = bone_name[len("R"):]

                bone.name = "ValveBiped.Bip01" + bone_name_trimmed + "_R"

        return {'FINISHED'}


class SATRestoreBonesOperator(bpy.types.Operator):
    bl_idname = "sat.restore_bones"
    bl_label = "Restore"

    def execute(self, context):
        properties = context.scene.satproperties
        armature_data = properties.target_armature.data

        valvebones = []

        for bone in armature_data.bones:
            if bone.name.startswith(BONE_PREFIX):
                valvebones.append(bone)

        for bone in valvebones:
            bone_name = bone.name[len(BONE_PREFIX):]

            if bone_name.endswith("_L"):
                bone.name = BONE_PREFIX + "L_" + bone_name[:-len("_L")]

            if bone_name.endswith("_R"):
                bone.name = BONE_PREFIX + "R_" + bone_name[:-len("_R")]

        return {'FINISHED'}


class SATSymmetryAddOperator(bpy.types.Operator):
    bl_idname = "sat.symmetry_add"
    bl_label = "Add"

    def execute(self, context):
        bpy.ops.sat.symmetry_remove()

        properties = context.scene.satproperties
        armature = properties.target_armature

        valvebones = []

        for bone_name in armature.pose.bones.keys():
            if bone_name.startswith(BONE_PREFIX):
                valvebones.append(bone_name[len(BONE_PREFIX):])

        paired_bones = []

        for bone_name in valvebones:
            # TODO: Create functions or something to make this repeat less.
            if bone_name.startswith("L_"):
                pair_bone_name = "R_" + bone_name[len("L_"):]

                if pair_bone_name in valvebones:
                    paired_bones.append((bone_name, pair_bone_name))
                    valvebones.remove(pair_bone_name)

                valvebones.remove(bone_name)

            if bone_name.endswith("_L"):
                pair_bone_name = bone_name[:-len("_L")] + "_R"

                if pair_bone_name in valvebones:
                    paired_bones.append((bone_name, pair_bone_name))
                    valvebones.remove(pair_bone_name)

                valvebones.remove(bone_name)

            if bone_name.startswith("R_"):
                pair_bone_name = "L_" + bone_name[len("R_"):]

                if pair_bone_name in valvebones:
                    paired_bones.append((pair_bone_name, bone_name))
                    valvebones.remove(pair_bone_name)

                valvebones.remove(bone_name)

            if bone_name.endswith("_R"):
                pair_bone_name = bone_name[:-len("_R")] + "_L"

                if pair_bone_name in valvebones:
                    paired_bones.append((pair_bone_name, bone_name))
                    valvebones.remove(pair_bone_name)

                valvebones.remove(bone_name)

        for left_bone_name, right_bone_name in paired_bones:
            left_bone = armature.pose.bones.get(BONE_PREFIX + left_bone_name)
            right_bone = armature.pose.bones.get(BONE_PREFIX + right_bone_name)

            # TODO: There is only two things that change between left and right so lot of duplicent code to be removed.
            if properties.symmetry_side == "SATSR":
                rotation_constraint = right_bone.constraints.new('COPY_ROTATION')
                rotation_constraint.name = "SAT Symmetry Rotation"
                rotation_constraint.target = armature
                rotation_constraint.subtarget = left_bone.name
                rotation_constraint.invert_x = True
                rotation_constraint.invert_y = True
                rotation_constraint.target_space = 'LOCAL_WITH_PARENT'
                rotation_constraint.owner_space = 'LOCAL_WITH_PARENT'

                if properties.symmetry_fix is True and "UpperArm" in right_bone_name:
                    rotation_constraint.invert_y = False
                    rotation_constraint.invert_z = True

                location_constraint = right_bone.constraints.new('COPY_LOCATION')
                location_constraint.name = "SAT Symmetry Location"
                location_constraint.target = armature
                location_constraint.subtarget = left_bone.name
                location_constraint.invert_x = True

                if properties.symmetry_offset is True:
                    location_constraint.invert_x = False
                    location_constraint.invert_z = True
                    location_constraint.target_space = 'LOCAL'
                    location_constraint.owner_space = 'LOCAL'

            if properties.symmetry_side == "SATSL":
                rotation_constraint = left_bone.constraints.new('COPY_ROTATION')
                rotation_constraint.name = "SAT Symmetry Rotation"
                rotation_constraint.target = armature
                rotation_constraint.subtarget = right_bone.name
                rotation_constraint.invert_x = True
                rotation_constraint.invert_y = True
                rotation_constraint.target_space = 'LOCAL_WITH_PARENT'
                rotation_constraint.owner_space = 'LOCAL_WITH_PARENT'

                if properties.symmetry_fix is True and "UpperArm" in left_bone_name:
                    rotation_constraint.invert_y = False
                    rotation_constraint.invert_z = True

                location_constraint = left_bone.constraints.new('COPY_LOCATION')
                location_constraint.name = "SAT Symmetry Location"
                location_constraint.target = armature
                location_constraint.subtarget = right_bone.name
                location_constraint.invert_x = True

                if properties.symmetry_offset is True:
                    location_constraint.invert_x = False
                    location_constraint.invert_z = True
                    location_constraint.target_space = 'LOCAL'
                    location_constraint.owner_space = 'LOCAL'

        return {'FINISHED'}


class SATSymmetryRemoveOperator(bpy.types.Operator):
    bl_idname = "sat.symmetry_remove"
    bl_label = "Remove"

    def execute(self, context):
        properties = context.scene.satproperties
        armature = properties.target_armature

        for bone in armature.pose.bones:
            for constraint in bone.constraints:
                if constraint.name.startswith("SAT Symmetry"):
                    bone.constraints.remove(constraint)

        return {'FINISHED'}


class SATSymmetryApplyOperator(bpy.types.Operator):
    bl_idname = "sat.symmetry_apply"
    bl_label = "Apply"

    def execute(self, context):
        return {'FINISHED'}


class SATWeightGenerateOperator(bpy.types.Operator):
    bl_idname = "sat.weight_create"
    bl_label = "Generate"

    def execute(self, context):
        return {'FINISHED'}


class SATWeightRemoveOperator(bpy.types.Operator):
    bl_idname = "sat.weight_delete"
    bl_label = "Delete"

    def execute(self, context):
        return {'FINISHED'}
