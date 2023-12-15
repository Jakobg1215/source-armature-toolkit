import re

VALVEBIPED_PREFIX = "ValveBiped."

valvebiped_bone_names = [
    "Pelvis",
    "Spine",
    "Spine1",
    "Spine2",
    "Spine4",
    "Neck1",
    "Head1",
    "Thigh",
    "Calf",
    "Foot",
    "Toe0",
    "Clavicle",
    "UpperArm",
    "Forearm",
    "Hand",
    "Finger4",
    "Finger41",
    "Finger42",
    "Finger3",
    "Finger31",
    "Finger32",
    "Finger2",
    "Finger21",
    "Finger22",
    "Finger1",
    "Finger11",
    "Finger12",
    "Finger0",
    "Finger01",
    "Finger02"
]

valvebiped_helperbones_names = [
    "Ankle",
    "Bicep",
    "Elbow",
    "Hip",
    "Knee",
    "Latt",
    "Pectoral",
    "Quadricep",
    "Shin",
    "Shoulder",
    "Sartorius",
    "Trapezius",
    "Ulna",
    "Wrist"
]


def sort_bones(context):
    properties = context.scene.satproperties
    if properties.target_armature is None:
        return
    armature_data = properties.target_armature.data

    valvebiped_bones = []
    for bone in armature_data.bones:
        if bone.name.startswith(VALVEBIPED_PREFIX):
            valvebiped_bones.append(bone)

    bip_bones = filter_bip_bones(valvebiped_bones)

    create_bone_collections(armature_data)

    sort_bones_to_collections(armature_data, bip_bones)


def filter_bip_bones(valvebiped_bones):
    bip_bones = []

    for bone in valvebiped_bones:
        name_pattern = re.compile(r'^ValveBiped\.Bip01_(L_|R_|)?(.+?)(_L|_R)?$')

        pattern_matches = name_pattern.match(bone.name)

        if not pattern_matches:
            continue

        prefix, bone_name, postfix = pattern_matches.groups()

        if bone_name not in valvebiped_bone_names:
            continue  # TODO: Handle helper bones

        if prefix != "" or postfix is not None:
            if prefix == "R_" or postfix == "_R":
                bip_bones.append((bone, bone_name, True))
                continue

            bip_bones.append((bone, bone_name, False))
            continue

        bip_bones.append((bone, bone_name, None))

    return bip_bones


def create_bone_collections(armature_data):
    if armature_data.collections.get("Central Bones") is None:
        armature_data.collections.new("Central Bones")
    if armature_data.collections.get("Left Leg Bones") is None:
        armature_data.collections.new("Left Leg Bones")
    if armature_data.collections.get("Right Leg Bones") is None:
        armature_data.collections.new("Right Leg Bones")
    if armature_data.collections.new("Left Arm Bones") is None:
        armature_data.collections.new("Left Arm Bones")
    if armature_data.collections.new("Right Arm Bones") is None:
        armature_data.collections.new("Right Arm Bones")
    # if armature_data.collections.new("Helper Bones") is None:
    #     armature_data.collections.new("Helper Bones")
    # if armature_data.collections.new("Attachments Bones") is None:
    #     armature_data.collections.new("Attachments Bones")


def sort_bones_to_collections(armature_data, bip_bones):
    central_bones_collection = armature_data.collections.get("Central Bones")
    left_leg_bones_collection = armature_data.collections.get("Left Leg Bones")
    right_leg_bones_collection = armature_data.collections.get("Right Leg Bones")
    left_arm_bones_collection = armature_data.collections.get("Left Arm Bones")
    right_arm_bones_collection = armature_data.collections.get("Right Arm Bones")
    # helper_bones_collection = armature_data.collections.new("Helper Bones")
    # attachments_bones_collection = armature_data.collections.new("Attachments Bones")

    for bone, bone_name, is_right_side in bip_bones:
        # TODO: Check if its an actual central bone.
        if is_right_side is None:
            central_bones_collection.assign(bone)
            bone.color.palette = 'THEME03'
            continue

        if bone_name in valvebiped_bone_names[7:11]:
            if is_right_side:
                right_leg_bones_collection.assign(bone)
                bone.color.palette = 'THEME04'
                continue
            left_leg_bones_collection.assign(bone)
            bone.color.palette = 'THEME01'
            continue

        if bone_name in valvebiped_bone_names[11:]:
            if is_right_side:
                right_arm_bones_collection.assign(bone)
                bone.color.palette = 'THEME04'
                continue
            left_arm_bones_collection.assign(bone)
            bone.color.palette = 'THEME01'
