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
        "name": "DKS RizomUV",
        "description": "RizomUV Bridge",
        "author": "DigiKrafting.Studio",
        "version": (0, 5, 0),
        "blender": (2, 80, 0),
        "location": "Info Toolbar, File -> Import, File -> Export",
        "wiki_url":    "https://github.com/DigiKrafting/blender_addon_rizom_uv/wiki",
        "tracker_url": "https://github.com/DigiKrafting/blender_addon_rizom_uv/issues",
        "category": "Import-Export",
}

import bpy
from bpy.utils import register_class, unregister_class
from . import dks_ruv

class dks_ruv_addon_prefs(bpy.types.AddonPreferences):

        bl_idname = __package__

        option_ruv_exe : bpy.props.StringProperty(
                name="RizomUV Executable",
                subtype='FILE_PATH',
                default=r"C:\Program Files\Rizom Lab\RizomUV VS RS 2018.0\rizomuv.exe",
        )     
        option_export_folder : bpy.props.StringProperty(
                name="Export Folder Name",
                default="eXport",
        )  
        option_save_before_export : bpy.props.BoolProperty(
                name="Save Before Export",
                default=True,
        )     
        option_display_type : bpy.props.EnumProperty(
                items=[('Buttons', "Buttons", "Use Buttons"),('Menu', "Menu", "Append a Menu to Main Menu"),('Hide', "Import/Export", "Use only Import/Export Menu's"),],
                name="Display Type",
                default='Buttons',
        )
        def draw(self, context):

                layout = self.layout

                box=layout.box()
                box.prop(self, 'option_display_type')
                box.prop(self, 'option_ruv_exe')
                box=layout.box()
                box.prop(self, 'option_export_folder')
                box.label(text='Automatically created as a sub folder relative to the saved .blend file. * Do NOT include any "\\".',icon='INFO')
                box.prop(self, 'option_save_before_export')

class dks_ruv_menu(bpy.types.Menu):

    bl_label = " " + bl_info['name']
    bl_idname = "dks_ruv.menu"

    def draw(self, context):
            
        layout = self.layout

        self.layout.operator('dks_ruv.export',icon="EXPORT")
        self.layout.operator('dks_ruv.import',icon="IMPORT")

def dks_draw_ruv_menu(self, context):

        layout = self.layout
        layout.menu(dks_ruv_menu.bl_idname,icon="COLLAPSEMENU")

def dks_ruv_menu_func_export(self, context):
    self.layout.operator("dks_ruv.export")

def dks_ruv_menu_func_import(self, context):
    self.layout.operator("dks_ruv.import")

def dks_ruv_draw_btns(self, context):
    
    if context.region.alignment != 'RIGHT':

        layout = self.layout
        row = layout.row(align=True)
        row.operator('dks_ruv.export',text="RUV",icon="EXPORT")
        row.operator('dks_ruv.import',text="RUV",icon="IMPORT")

classes = (
    dks_ruv_addon_prefs,
)

def register():

    for cls in classes:
        register_class(cls)

    dks_ruv.register()

    bpy.types.TOPBAR_MT_file_export.append(dks_ruv_menu_func_export)
    bpy.types.TOPBAR_MT_file_import.append(dks_ruv_menu_func_import)

    if bpy.context.preferences.addons[__package__].preferences.option_display_type=='Buttons':
    
        bpy.types.TOPBAR_HT_upper_bar.append(dks_ruv_draw_btns)

    elif bpy.context.preferences.addons[__package__].preferences.option_display_type=='Menu':

        register_class(dks_ruv_menu)
        bpy.types.TOPBAR_MT_editor_menus.append(dks_draw_ruv_menu)
        
def unregister():

    bpy.types.TOPBAR_MT_file_import.remove(dks_ruv_menu_func_import)
    bpy.types.TOPBAR_MT_file_export.remove(dks_ruv_menu_func_export)
    
    if bpy.context.preferences.addons[__package__].preferences.option_display_type=='Buttons':

        bpy.types.TOPBAR_HT_upper_bar.remove(dks_ruv_draw_btns)

    dks_ruv.unregister()

    for cls in reversed(classes):
        unregister_class(cls)

if __name__ == "__main__":

	register()