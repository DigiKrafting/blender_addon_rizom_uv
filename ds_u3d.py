# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy, math

from subprocess import Popen
from os import system, path, makedirs

def ds_u3d_get_export_path():

    _export_path = bpy.path.abspath('//') + bpy.context.user_preferences.addons[__package__].preferences.option_export_folder + '\\'

    if not path.exists(_export_path):
        makedirs(_export_path)

    return _export_path

def ds_u3d_obj_filename(self, context):

    _object_name = bpy.context.scene.objects.active.name
    _export_path = ds_u3d_get_export_path()
    _export_file = _export_path + _object_name + '.obj'

    if not bpy.context.user_preferences.addons[__package__].preferences.option_save_before_export:
        bpy.ops.wm.save_mainfile()

    return _export_file

def ds_u3d_obj_export(self, context):

    _export_file = ds_u3d_obj_filename(self, context)

    bpy.ops.object.mode_set(mode='OBJECT')
    
    bpy.ops.export_scene.obj(filepath=_export_file, check_existing=False, use_selection=True, axis_forward='-Z', axis_up='Y', use_normals=True, use_uvs=True, use_materials=True, global_scale = 1.0)

    return _export_file

class ds_u3d_obj_export_execute(bpy.types.Operator):

    bl_idname = "ds_u3d.obj_export"
    bl_label = "Export OBJ."

    def execute(self, context):

        _export_file = ds_u3d_obj_export(self, context)

        return {'FINISHED'}

class ds_u3d_export(bpy.types.Operator):

    bl_idname = "ds_u3d.export"
    bl_label = "Unfold3D (OBJ)"

    def execute(self, context):

        _export_file = ds_u3d_obj_export(self, context)

        Popen([bpy.context.user_preferences.addons[__package__].preferences.option_u3d_exe,_export_file])

        return {'FINISHED'}

class ds_u3d_import(bpy.types.Operator):

    bl_idname = "ds_u3d.import"
    bl_label = "Unfold3D (OBJ)"

    def execute(self, context):

        obj_selected = bpy.context.object
        bpy.ops.object.mode_set(mode='OBJECT')

        bpy.ops.import_scene.obj(filepath = ds_u3d_obj_filename(self, context), axis_forward='-Z', axis_up='Y', use_edges=True, use_smooth_groups=True, use_split_objects=True, use_split_groups=True, use_groups_as_vgroups=False, use_image_search=False, split_mode='OFF', global_clamp_size=0.0)
        obj_imported =  bpy.context.selected_objects[0]

        obj_imported.select = True
        obj_selected.select = True
        bpy.context.scene.objects.active = obj_imported

        bpy.ops.object.join_uvs()
        
        #bpy.ops.object.data_transfer(data_type='UV',vert_mapping='TOPOLOGY',edge_mapping='TOPOLOGY',loop_mapping='TOPOLOGY',poly_mapping='TOPOLOGY', mix_mode='REPLACE')
        #bpy.ops.object.data_transfer(data_type='SEAM',vert_mapping='TOPOLOGY',edge_mapping='TOPOLOGY',loop_mapping='TOPOLOGY',poly_mapping='TOPOLOGY', mix_mode='REPLACE')

        obj_selected.select = False
        
        bpy.ops.object.delete()

        bpy.context.scene.objects.active = obj_selected
        obj_selected.select = True

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.uv.seams_from_islands(mark_seams=False, mark_sharp=False)
        bpy.ops.object.mode_set(mode='OBJECT')

        return {'FINISHED'}

def ds_u3d_menu_func_export(self, context):
    self.layout.operator(ds_u3d_export.bl_idname)

def ds_u3d_menu_func_import(self, context):
    self.layout.operator(ds_u3d_import.bl_idname)

def ds_u3d_toolbar_btn_import(self, context):
    self.layout.operator('ds_u3d.import',text="U3D",icon="IMPORT")

def ds_u3d_toolbar_btn_export(self, context):
    self.layout.operator('ds_u3d.export',text="U3D",icon="EXPORT")

def register():

    from bpy.utils import register_class

    register_class(ds_u3d_obj_export_execute)

    register_class(ds_u3d_import)
    register_class(ds_u3d_export)

    if bpy.context.user_preferences.addons[__package__].preferences.option_display_type=='Buttons':
    
        bpy.types.INFO_HT_header.append(ds_u3d_toolbar_btn_export)
        bpy.types.INFO_HT_header.append(ds_u3d_toolbar_btn_import)

    bpy.types.INFO_MT_file_export.append(ds_u3d_menu_func_export)
    bpy.types.INFO_MT_file_import.append(ds_u3d_menu_func_import)

def unregister():

    from bpy.utils import unregister_class

    if bpy.context.user_preferences.addons[__package__].preferences.option_display_type=='Buttons':

        bpy.types.INFO_HT_header.remove(ds_u3d_toolbar_btn_import)
        bpy.types.INFO_HT_header.remove(ds_u3d_toolbar_btn_export)

    bpy.types.INFO_MT_file_import.remove(ds_u3d_menu_func_import)
    bpy.types.INFO_MT_file_export.remove(ds_u3d_menu_func_export)

    unregister_class(ds_u3d_obj_export_execute)

    unregister_class(ds_u3d_import)
    unregister_class(ds_u3d_export)


