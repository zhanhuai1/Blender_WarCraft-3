
import os

import bpy
from . import classes
from . import constants
from . import parser
from . import utils
from bpy_extras import io_utils


class WarCraft3OperatorImportMDX(bpy.types.Operator, io_utils.ImportHelper):
    bl_idname = 'warcraft_3.import_mdx'
    bl_label = 'Import *.mdx'
    bl_description = 'Import *.mdx files (3d models of WarCraft 3)'
    bl_options = {'UNDO'}

    filename_ext = '.mdx'
    filter_glob = bpy.props.StringProperty(default='*.mdx', options={'HIDDEN'})
    filepath = bpy.props.StringProperty(name='File Path', maxlen=1024, default='')
    useCustomFPS = bpy.props.BoolProperty(name='Use Custom FPS', default=False)
    animationFPS = bpy.props.FloatProperty(name='Animation FPS', default=30.0, min=1.0, max=1000.0)
    boneSize = bpy.props.FloatProperty(name='Bone Size', default=5.0, min=0.0001, max=1000.0)
    teamColor = bpy.props.FloatVectorProperty(
        name='Team Color',
        default=constants.TEAM_COLORS['RED'],
        min=0.0,
        max=1.0,
        size=3,
        subtype='COLOR',
        precision=3
        )
    setTeamColor = bpy.props.EnumProperty(
        items=[
            ('RED', 'Red', ''),
            ('DARK_BLUE', 'Dark Blue', ''),
            ('TURQUOISE', 'Turquoise', ''),
            ('VIOLET', 'Violet', ''),
            ('YELLOW', 'Yellow', ''),
            ('ORANGE', 'Orange', ''),
            ('GREEN', 'Green', ''),
            ('PINK', 'Pink', ''),
            ('GREY', 'Grey', ''),
            ('BLUE', 'Blue', ''),
            ('DARK_GREEN', 'Dark Green', ''),
            ('BROWN', 'Brown', ''),
            ('BLACK', 'Black', '')
            ],
        name='Set Team Color',
        update=utils.set_team_color_property,
        default='RED'
        )

    def draw(self, context):
        layout = self.layout
        split = layout.split(percentage=0.9)
        subSplit = split.split(percentage=0.5)
        subSplit.label('Team Color:')
        subSplit.prop(self.properties, 'setTeamColor', text='')
        split.prop(self.properties, 'teamColor', text='')
        layout.prop(self.properties, 'boneSize')
        layout.prop(self.properties, 'useCustomFPS')
        if self.properties.useCustomFPS:
            layout.prop(self.properties, 'animationFPS')

    def execute(self, context):
        importProperties = classes.MDXImportProperties()
        importProperties.mdx_file_path = self.properties.filepath
        importProperties.set_team_color = self.properties.setTeamColor
        importProperties.bone_size = self.properties.boneSize
        importProperties.use_custom_fps = self.properties.useCustomFPS
        importProperties.fps = self.properties.animationFPS
        importProperties.calculate_frame_time()
        oldObjects = set(bpy.context.scene.objects)
        parser.load_mdx(importProperties)
        newObjects = set(bpy.context.scene.objects) - oldObjects
        newObjects = set(obj for obj in newObjects if obj.type == 'MESH')
        self.export_fbx(newObjects)
        return {'FINISHED'}

    def export_fbx(self, objects):
        if not objects:
            self.report({'WARNING'}, 'no mesh objects to export')
            return
        if not hasattr(bpy.ops.export_scene, 'fbx'):
            self.report({'WARNING'}, 'io_scene_fbx addon not enabled, skip FBX export')
            return
        fbxFilePath = os.path.splitext(self.properties.filepath)[0] + '.fbx'
        bpy.ops.object.select_all(action='DESELECT')
        for obj in objects:
            obj.scale = (0.01, 0.01, 0.01)
            obj.select = True
        bpy.ops.export_scene.fbx(
            filepath=fbxFilePath,
            use_selection=True,
            use_anim=False,
            axis_forward='X',
            axis_up='Z'
            )
        bpy.ops.object.select_all(action='DESELECT')

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class WarCraft3OperatorImportMDXBatch(bpy.types.Operator):
    bl_idname = 'warcraft_3.import_mdx_batch'
    bl_label = 'Import *.mdx (batch)'
    bl_description = 'Import all *.mdx files from a directory and export them as *.fbx'
    bl_options = {'UNDO'}

    directory = bpy.props.StringProperty(name='Directory', maxlen=1024, subtype='DIR_PATH')
    useCustomFPS = bpy.props.BoolProperty(name='Use Custom FPS', default=False)
    animationFPS = bpy.props.FloatProperty(name='Animation FPS', default=30.0, min=1.0, max=1000.0)
    boneSize = bpy.props.FloatProperty(name='Bone Size', default=5.0, min=0.0001, max=1000.0)
    teamColor = bpy.props.FloatVectorProperty(
        name='Team Color',
        default=constants.TEAM_COLORS['RED'],
        min=0.0,
        max=1.0,
        size=3,
        subtype='COLOR',
        precision=3
        )
    setTeamColor = bpy.props.EnumProperty(
        items=[
            ('RED', 'Red', ''),
            ('DARK_BLUE', 'Dark Blue', ''),
            ('TURQUOISE', 'Turquoise', ''),
            ('VIOLET', 'Violet', ''),
            ('YELLOW', 'Yellow', ''),
            ('ORANGE', 'Orange', ''),
            ('GREEN', 'Green', ''),
            ('PINK', 'Pink', ''),
            ('GREY', 'Grey', ''),
            ('BLUE', 'Blue', ''),
            ('DARK_GREEN', 'Dark Green', ''),
            ('BROWN', 'Brown', ''),
            ('BLACK', 'Black', '')
            ],
        name='Set Team Color',
        update=utils.set_team_color_property,
        default='RED'
        )

    def draw(self, context):
        layout = self.layout
        split = layout.split(percentage=0.9)
        subSplit = split.split(percentage=0.5)
        subSplit.label('Team Color:')
        subSplit.prop(self.properties, 'setTeamColor', text='')
        split.prop(self.properties, 'teamColor', text='')
        layout.prop(self.properties, 'boneSize')
        layout.prop(self.properties, 'useCustomFPS')
        if self.properties.useCustomFPS:
            layout.prop(self.properties, 'animationFPS')

    def execute(self, context):
        if not self.directory:
            self.report({'ERROR'}, 'no directory selected')
            return {'CANCELLED'}
        mdxFiles = sorted(fileName for fileName in os.listdir(self.directory) if fileName.lower().endswith('.mdx'))
        wm = context.window_manager
        wm.progress_begin(0, len(mdxFiles))
        for index, fileName in enumerate(mdxFiles):
            filePath = os.path.join(self.directory, fileName)
            try:
                bpy.ops.warcraft_3.import_mdx(
                    filepath=filePath,
                    setTeamColor=self.setTeamColor,
                    boneSize=self.boneSize,
                    useCustomFPS=self.useCustomFPS,
                    animationFPS=self.animationFPS
                    )
            except Exception as e:
                self.report({'ERROR'}, '{0}: {1}'.format(fileName, e))
            wm.progress_update(index + 1)
        wm.progress_end()
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class WarCraft3OperatorAddSequenceToArmature(bpy.types.Operator):
    bl_idname = 'warcraft_3.add_sequence_to_armature'
    bl_label = 'WarCraft 3 Add Sequence to Armature'
    bl_description = 'WarCraft 3 Add Sequence to Armature'
    bl_options = {'UNDO'}

    def execute(self, context):
        if context.armature:
            warcraft3data = context.armature.warcraft_3
            sequence = warcraft3data.sequencesList.add()
            sequence.name = '#UNANIMATED'
        return {'FINISHED'}


class WarCraft3OperatorRemoveSequenceToArmature(bpy.types.Operator):
    bl_idname = 'warcraft_3.remove_sequence_to_armature'
    bl_label = 'WarCraft 3 Remove Sequence to Armature'
    bl_description = 'WarCraft 3 Remove Sequence to Armature'
    bl_options = {'UNDO'}

    def execute(self, context):
        if context.armature:
            warcraft3data = context.armature.warcraft_3
            warcraft3data.sequencesList.remove(warcraft3data.sequencesListIndex)
        return {'FINISHED'}


class WarCraft3OperatorUpdateBoneSettings(bpy.types.Operator):
    bl_idname = 'warcraft_3.update_bone_settings'
    bl_label = 'WarCraft 3 Update Bone Settings'
    bl_description = 'WarCraft 3 Update Bone Settings'
    bl_options = {'UNDO'}

    def execute(self, context):
        object = context.object
        for bone in object.data.bones:
            nodeType = bone.warcraft_3.nodeType
            boneGroup = object.pose.bone_groups.get(nodeType.lower() + 's', None)
            if not boneGroup:
                if nodeType in {'BONE', 'ATTACHMENT', 'COLLISION_SHAPE', 'EVENT', 'HELPER'}:
                    bpy.ops.pose.group_add()
                    boneGroup = object.pose.bone_groups.active
                    boneGroup.name = nodeType.lower() + 's'
                    if nodeType == 'BONE':
                        boneGroup.color_set = 'THEME04'
                    elif nodeType == 'ATTACHMENT':
                        boneGroup.color_set = 'THEME09'
                    elif nodeType == 'COLLISION_SHAPE':
                        boneGroup.color_set = 'THEME02'
                    elif nodeType == 'EVENT':
                        boneGroup.color_set = 'THEME03'
                    elif nodeType == 'HELPER':
                        boneGroup.color_set = 'THEME01'
                else:
                    boneGroup = None
            object.pose.bones[bone.name].bone_group = boneGroup
        return {'FINISHED'}
