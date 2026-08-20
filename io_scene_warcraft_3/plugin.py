
import bpy
from . import operators
from . import preferences
from . import types
from . import ui


def menu_import_mdx(self, context):
    self.layout.operator(operators.WarCraft3OperatorImportMDX.bl_idname, text='WarCraft 3 (.mdx)')
    self.layout.operator(operators.WarCraft3OperatorImportMDXBatch.bl_idname, text='WarCraft 3 (.mdx) (batch)')


def menu_object(self, context):
    self.layout.operator(operators.WarCraft3OperatorLimitMeshSize.bl_idname, text='WarCraft 3 Limit Mesh Size')


def register():
    bpy.utils.register_class(preferences.WarCraft3Preferences)
    bpy.utils.register_class(operators.WarCraft3OperatorImportMDX)
    bpy.utils.register_class(operators.WarCraft3OperatorImportMDXBatch)
    bpy.types.INFO_MT_file_import.append(menu_import_mdx)
    bpy.utils.register_class(operators.WarCraft3OperatorLimitMeshSize)
    bpy.types.VIEW3D_MT_object.append(menu_object)
    bpy.utils.register_class(operators.WarCraft3OperatorAddSequenceToArmature)
    bpy.utils.register_class(operators.WarCraft3OperatorRemoveSequenceToArmature)
    bpy.utils.register_class(operators.WarCraft3OperatorUpdateBoneSettings)
    bpy.utils.register_class(types.WarCraft3ArmatureSequenceList)
    bpy.utils.register_class(types.WarCraft3ArmatureProperties)
    types.WarCraft3ArmatureProperties.bpy_type.warcraft_3 = bpy.props.PointerProperty(type=types.WarCraft3ArmatureProperties)
    bpy.utils.register_class(types.WarCraft3BoneProperties)
    types.WarCraft3BoneProperties.bpy_type.warcraft_3 = bpy.props.PointerProperty(type=types.WarCraft3BoneProperties)
    bpy.utils.register_class(ui.WarCraft3PanelArmature)
    bpy.utils.register_class(ui.WarCraft3PanelBone)


def unregister():
    bpy.types.INFO_MT_file_import.remove(menu_import_mdx)
    bpy.types.VIEW3D_MT_object.remove(menu_object)
    bpy.utils.unregister_class(operators.WarCraft3OperatorLimitMeshSize)
    bpy.utils.unregister_class(operators.WarCraft3OperatorImportMDXBatch)
    bpy.utils.unregister_class(operators.WarCraft3OperatorImportMDX)
    bpy.utils.unregister_class(ui.WarCraft3PanelBone)
    bpy.utils.unregister_class(ui.WarCraft3PanelArmature)
    del types.WarCraft3BoneProperties.bpy_type.warcraft_3
    bpy.utils.unregister_class(types.WarCraft3BoneProperties)
    del types.WarCraft3ArmatureProperties.bpy_type.warcraft_3
    bpy.utils.unregister_class(types.WarCraft3ArmatureProperties)
    bpy.utils.unregister_class(types.WarCraft3ArmatureSequenceList)
    bpy.utils.unregister_class(operators.WarCraft3OperatorUpdateBoneSettings)
    bpy.utils.unregister_class(operators.WarCraft3OperatorRemoveSequenceToArmature)
    bpy.utils.unregister_class(operators.WarCraft3OperatorAddSequenceToArmature)
    bpy.utils.unregister_class(preferences.WarCraft3Preferences)
