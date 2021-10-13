#!/usr/bin/env python3

# ----------------------------------- Services - Services Menus GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def services_menu_right_click_import_func():

    global Gtk, Gdk, os, subprocess

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk
    import os
    import subprocess


    global ServicesGUI
    import ServicesGUI


# ----------------------------------- Services - Services Menus GUI Function (the code of this module in order to avoid running them during module import and defines "Services" tab menu/popover GUI objects and functions/signals) -----------------------------------
def services_menu_right_click_gui_func():

    # Define builder and get all objects (Services tab right click menu) from GUI file.
    builder = Gtk.Builder()
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/ServicesMenuRightClick.ui")


    # ********************** Define object names for Services tab right click menu **********************
    global menu6101m
    global menuitem6101m, menuitem6102m, menuitem6103m, menuitem6104m, menuitem6105m, menuitem6106m, checkmenuitem6107m, menuitem6108m
    global menuitem6109m

    # ********************** Get object names for Services tab right click menu **********************
    menu6101m = builder.get_object('menu6101m')
    menuitem6101m = builder.get_object('menuitem6101m')
    menuitem6102m = builder.get_object('menuitem6102m')
    menuitem6103m = builder.get_object('menuitem6103m')
    menuitem6104m = builder.get_object('menuitem6104m')
    menuitem6105m = builder.get_object('menuitem6105m')
    menuitem6106m = builder.get_object('menuitem6106m')
    checkmenuitem6107m = builder.get_object('checkmenuitem6107m')
    menuitem6108m = builder.get_object('menuitem6108m')
    menuitem6109m = builder.get_object('menuitem6109m')

    # ********************** Define object functions for Services tab right click menu **********************
    def on_menu6101m_show(widget):
        pass

    def on_menuitem6101m_activate(widget):                                                    # "Start" item on the right click menu
        service_name = ServicesGUI.selected_service_name
        try:
            (subprocess.check_output("systemctl start " + service_name, shell=True).strip()).decode()
        except subprocess.CalledProcessError:
            pass

    def on_menuitem6102m_activate(widget):                                                    # "Stop" item on the right click menu
        service_name = ServicesGUI.selected_service_name
        try:
            (subprocess.check_output("systemctl stop " + service_name, shell=True).strip()).decode()
        except subprocess.CalledProcessError:
            pass

    def on_menuitem6103m_activate(widget):                                                    # "Restart" item on the right click menu
        service_name = ServicesGUI.selected_service_name
        try:
            (subprocess.check_output("systemctl restart " + service_name, shell=True).strip()).decode()
        except subprocess.CalledProcessError:
            pass

    def on_menuitem6104m_activate(widget):                                                    # "Reload" item on the right click menu
        service_name = ServicesGUI.selected_service_name
        try:
            (subprocess.check_output("systemctl reload " + service_name, shell=True).strip()).decode()
        except subprocess.CalledProcessError:
            pass

    def on_menuitem6105m_activate(widget):                                                    # "Enable" item on the right click menu
        service_name = ServicesGUI.selected_service_name
        try:
            (subprocess.check_output("systemctl enable " + service_name, shell=True).strip()).decode()
        except subprocess.CalledProcessError:
            pass

    def on_menuitem6106m_activate(widget):                                                    # "Disable" item on the right click menu
        service_name = ServicesGUI.selected_service_name
        try:
            (subprocess.check_output("systemctl disable " + service_name, shell=True).strip()).decode()
        except subprocess.CalledProcessError:
            pass

    def on_checkmenuitem6107m_toggled(widget):                                                # "Mask" item on the right click menu
        service_name = ServicesGUI.selected_service_name
        try:
            if checkmenuitem6107m.get_active() == True:
                (subprocess.check_output("systemctl mask " + service_name, shell=True).strip()).decode()
            if checkmenuitem6107m.get_active() == False:
                (subprocess.check_output("systemctl unmask " + service_name, shell=True).strip()).decode()
        except subprocess.CalledProcessError:
            pass

    def on_menuitem6108m_activate(widget):                                                    # "Copy Name" item on the right click menu
        service_name = ServicesGUI.selected_service_name
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_text(service_name, -1)
        clipboard.store()                                                                     # Stores copied text in the clipboard. Therefore text stays in the clipboard after application has quit.

    def on_menuitem6109m_activate(widget):                                                    # "Details" item on the right click menu
        if 'ServicesDetailsGUI' not in globals():                                             # Check if "ServicesDetailsGUI" module is imported. Therefore it is not reimported for every click on "Details" menu item on the right click menu if "ServicesDetailsGUI" name is in globals().
            global ServicesDetailsGUI, ServicesDetails
            import ServicesDetailsGUI, ServicesDetails
            ServicesDetailsGUI.services_details_gui_import_function()
            ServicesDetailsGUI.services_details_gui_function()
            ServicesDetails.services_details_import_func()
        ServicesDetailsGUI.window6101w.show()
        ServicesDetails.services_details_foreground_thread_run_func()

    # ********************** Connect signals to GUI objects for Services tab right click menu **********************
    menu6101m.connect("show", on_menu6101m_show)
    menuitem6101m.connect("activate", on_menuitem6101m_activate)
    menuitem6102m.connect("activate", on_menuitem6102m_activate)
    menuitem6103m.connect("activate", on_menuitem6103m_activate)
    menuitem6104m.connect("activate", on_menuitem6104m_activate)
    global checkmenuitem6107m_handler_id
    checkmenuitem6107m_handler_id = checkmenuitem6107m.connect("toggled", on_checkmenuitem6107m_toggled)    # Handler id is defined in order to block signals of the checkmenuitem. Because checkmenuitem is set as "activated/deactivated" appropriate with relevant service status when right click and mouse button release action is finished. This action triggers unwanted event signals.
    menuitem6108m.connect("activate", on_menuitem6108m_activate)
    menuitem6109m.connect("activate", on_menuitem6109m_activate)


# ----------------------------------- Services - Set Checkmenuitems (acivates/deactivates checkmenuitem (Enable/Disable checkbox for service status (enabled/disabled, masked/unmasked)) on the popup menu when right click operation is performed on service row on the treeview) -----------------------------------
def services_set_checkmenuitem_func():

    service_name = ServicesGUI.selected_service_name
    service_status = subprocess.check_output("systemctl show " + service_name + " --property=UnitFileState", shell=True).decode().strip().split("=")[1]
    with checkmenuitem6107m.handler_block(checkmenuitem6107m_handler_id):
        if service_status == "masked":
            checkmenuitem6107m.set_active(True)
        if service_status != "masked":
            checkmenuitem6107m.set_active(False)