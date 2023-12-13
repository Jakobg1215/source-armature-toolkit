import bpy


class SATMainPanel(bpy.types.Panel):
    bl_label = "Source Armature Toolkit"
    bl_idname = "SCENE_PT_satmain"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'scene'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        properties = context.scene.satproperties

        col = layout.column()
        col.prop(properties, 'target_armature', icon='OUTLINER_OB_ARMATURE')


class SATBoneRenamingPanel(bpy.types.Panel):
    bl_label = "Bone Renaming"
    bl_idname = "SAT_PT_rename"
    bl_parent_id = "SCENE_PT_satmain"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'scene'
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        properties = context.scene.satproperties

        return properties.target_armature is not None

    def draw(self, _context):
        layout = self.layout

        row = layout.row()
        row.operator("sat.rename_bones")
        row.operator("sat.restore_bones")


class SATSymmetryPanel(bpy.types.Panel):
    bl_label = "Symmetry Constraint"
    bl_idname = "SAT_PT_symmetry"
    bl_parent_id = "SCENE_PT_satmain"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'scene'
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        properties = context.scene.satproperties

        return properties.target_armature is not None

    def draw(self, context):
        layout = self.layout
        properties = context.scene.satproperties

        row = layout.row()
        row.operator("sat.symmetry_add")
        row.operator("sat.symmetry_remove")

        row = layout.row()
        row.prop(properties, "symmetry_side", expand=True)

        col = layout.column()
        col.operator("sat.symmetry_apply")

        col = layout.column()
        col.prop(properties, "symmetry_offset")
        col.prop(properties, "symmetry_fix")


class SATWeightArmaturePanel(bpy.types.Panel):
    bl_label = "Weight Armature"
    bl_idname = "SAT_PT_weight"
    bl_parent_id = "SCENE_PT_satmain"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'scene'
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        properties = context.scene.satproperties

        return properties.target_armature is not None

    def draw(self, _context):
        layout = self.layout

        row = layout.row()
        row.operator("sat.weight_create")
        row.operator("sat.weight_delete")
