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

bl_info = {
        "name": "Unfold3D",
        "description": "Unfold3D Tools",
        "author": "Digiography.Studio",
        "version": (0, 0, 1),
        "blender": (2, 79, 0),
        "location": "Info Toolbar, File -> Import, File -> Export",
        "wiki_url":    "https://github.com/Digiography/blender_addon_unfold3d/wiki",
        "tracker_url": "https://github.com/Digiography/blender_addon_unfold3d/issues",
        "category": "System",
}

import bpy

from . import ds_u3d

class ds_u3d_addon_prefs(bpy.types.AddonPreferences):

        bl_idname = __package__

        option_u3d_exe = bpy.props.StringProperty(
                name="Unfold3D Executable",
                subtype='FILE_PATH',
                default=r"C:\Program Files\Rizom Lab\Unfold3D VS RS 2017.0\unfold3d.exe",
        )     
        option_export_folder = bpy.props.StringProperty(
                name="Export Folder Name",
                default="eXport",
        )  
        option_save_before_export = bpy.props.BoolProperty(
                name="Save Before Export",
                default=True,
        )     
        options_display_types = [('Buttons', "Buttons", "Buttons"),('Menu', "Menu", "Menu"),('Hide', "Hide", "Hide"),]        
        option_display_type = bpy.props.EnumProperty(
                items=options_display_types,
                name="Display Type",
                default='Buttons',
        )
        def draw(self, context):

                layout = self.layout

                box=layout.box()
                box.prop(self, 'option_display_type')
                box.prop(self, 'option_u3d_exe')
                box=layout.box()
                box.prop(self, 'option_export_folder')
                box.label('Automatically created as a sub folder relative to the saved .blend file. * Do NOT include any "\\".',icon='INFO')
                box.prop(self, 'option_save_before_export')

class ds_u3d_prefs_open(bpy.types.Operator):

    bl_idname = "ds_u3d.prefs_open"
    bl_label = "Open Preferences"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
 
    def execute(self, context):
        
        bpy.ops.screen.userpref_show('INVOKE_DEFAULT')

        return {'FINISHED'}

class ds_u3d_menu(bpy.types.Menu):

    bl_label = " " + bl_info['name']
    bl_idname = "ds_u3d.menu"

    def draw(self, context):
            
        layout = self.layout

        self.layout.operator('ds_u3d.export',icon="EXPORT")
        self.layout.operator('ds_u3d.import',icon="IMPORT")

def draw_ds_u3d_menu(self, context):

        layout = self.layout
        layout.menu(ds_u3d_menu.bl_idname,icon="COLLAPSEMENU")

def register():

        from bpy.utils import register_class

        register_class(ds_u3d_addon_prefs)
        register_class(ds_u3d_prefs_open)

        if bpy.context.user_preferences.addons[__package__].preferences.option_display_type=='Menu':
                register_class(ds_u3d_menu)
                bpy.types.INFO_HT_header.append(draw_ds_u3d_menu)

        ds_u3d.register()

def unregister():

        from bpy.utils import unregister_class

        if bpy.context.user_preferences.addons[__package__].preferences.option_display_type=='Menu':

                bpy.types.INFO_HT_header.remove(draw_ds_u3d_menu)
                unregister_class(ds_u3d_menu)

        ds_u3d.unregister()

        unregister_class(ds_u3d_addon_prefs)
        unregister_class(ds_u3d_prefs_open)

if __name__ == "__main__":

	register()