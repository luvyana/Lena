import bpy
import os
from enum import Enum

# Panel

MAIN_PANEL_ID = "DENA_PT_Panel"
NODES_PANEL_ID = "Dena_PT_Nodes"

bl_info = {
    "name": "Dena",
    "author": "Ogulcan Tokar",
    "description": "Tool for creating node sockets",
    "blender": (3, 0, 0),
    "version": (0, 0, 1),
    "location": "Node Editor > Sidebar > Dena",
    "warning": "",
    "support": "COMMUNITY",
    "category": "Material"
}


class NodeSockets(Enum):
    # Useful for Materials
    NodeSocketColor = "NodeSocketColor"
    NodeSocketInt = "NodeSocketInt"
    NodeSocketIntFactor = "NodeSocketIntFactor"
    NodeSocketFloat = "NodeSocketFloat"
    NodeSocketFloatAngle = "NodeSocketFloatAngle"
    NodeSocketFloatDistance = "NodeSocketFloatDistance"
    NodeSocketFloatFactor = "NodeSocketFloatFactor"
    NodeSocketFloatPercentage = "NodeSocketFloatPercentage"
    NodeSocketFloatTime = "NodeSocketFloatTime"
    NodeSocketFloatTimeAbsolute = "NodeSocketFloatTimeAbsolute"
    NodeSocketFloatUnsigned = "NodeSocketFloatUnsigned"
    NodeSocketIntPercentage = "NodeSocketIntPercentage"
    NodeSocketIntUnsigned = "NodeSocketIntUnsigned"
    NodeSocketVector = "NodeSocketVector"
    NodeSocketVectorAcceleration = "NodeSocketVectorAcceleration"
    NodeSocketVectorDirection = "NodeSocketVectorDirection"
    NodeSocketVectorEuler = "NodeSocketVectorEuler"
    NodeSocketVectorTranslation = "NodeSocketVectorTranslation"
    NodeSocketVectorVelocity = "NodeSocketVectorVelocity"
    NodeSocketVectorXYZ = "NodeSocketVectorXYZ"
    NodeSocketShader = "NodeSocketShader"

    # Rest
    NodeSocketObject = "NodeSocketObject"
    NodeSocketTexture = "NodeSocketTexture"
    NodeSocketGeometry = "NodeSocketGeometry"
    NodeSocketImage = "NodeSocketImage"
    NodeSocketBool = "NodeSocketBool"
    NodeSocketString = "NodeSocketString"
    NodeSocketMaterial = "NodeSocketMaterial"
    NodeSocketCollection = "NodeSocketCollection"


NODE_SOCKET_ITEMS = [(socket.value, socket.name.replace("NodeSocket", ""), "") for socket in NodeSockets]


class PanelClass:
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = __name__.capitalize()


class DE_PT_Main(PanelClass, bpy.types.Panel):
    bl_idname = MAIN_PANEL_ID
    bl_label = __name__.capitalize()

    def draw(self, context):
        layout = self.layout


class DE_PT_EditSockets(PanelClass, bpy.types.Panel):
    bl_parent_id = MAIN_PANEL_ID
    bl_label = "Sockets"
    bl_order = 1

    def draw(self, context):
        layout = self.layout

        addon_prefs = context.preferences.addons[__name__].preferences
        context = bpy.context

        if context.space_data.type != 'NODE_EDITOR' or not context.active_node:
            layout.label(text="Not in Node Editor or no active node.")
            return

        if not context.active_node.type == "GROUP":
            layout.enabled = False

        layout.prop(addon_prefs, "socket_name", text="Name")
        layout.prop(addon_prefs, "socket_type", text="Type ")
        layout.prop(addon_prefs, "socket_in_out", expand=True)
        layout.operator("dena.add_socket", text="Add Socket")


# Operator
class DE_OT_add_socket(bpy.types.Operator):
    bl_idname = "dena.add_socket"
    bl_label = "Dena Add Socket"

    def execute(self, context):

        # Get the preferences for this add-on
        addon_prefs = context.preferences.addons[__name__].preferences

        # Get the preferences for this add-on
        selected_type = addon_prefs.socket_type
        selected_in_out = addon_prefs.socket_in_out
        selected_name = addon_prefs.socket_name
        selected_node_ctx = context.active_node

        # Get the name of the node tree
        node_tree_name = selected_node_ctx.node_tree.name

        # Get the node tree
        selected_node = bpy.data.node_groups.get(node_tree_name)

        # Add a new socket to the node
        if selected_in_out == "INPUT":
            selected_node.inputs.new(selected_type, selected_name)
        else:
            selected_node.outputs.new(selected_type, selected_name)

        return {"FINISHED"}


# Preferences
class DE_DenaPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    socket_type: bpy.props.EnumProperty(
        items=NODE_SOCKET_ITEMS,
        name="Node Sockets",
        description="Choose a node socket type",
        default="NodeSocketColor"
    )

    socket_in_out: bpy.props.EnumProperty(
        items=[
            ("INPUT", "Input", ""),
            ("OUTPUT", "Output", "")
        ],
        name="Input/Output",
        description="Choose a node socket type",
        default="INPUT"
    )

    socket_name: bpy.props.StringProperty(
        name="Socket Name",
        description="Choose a node socket type",
        default=""
    )


classes = (
    DE_PT_Main,
    DE_PT_EditSockets,
    DE_OT_add_socket,
    DE_DenaPreferences
)


register, unregister = bpy.utils.register_classes_factory(classes)
