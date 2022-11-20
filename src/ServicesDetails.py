#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('GLib', '2.0')
gi.require_version('Pango', '1.0')
from gi.repository import Gtk, GLib, Pango

import os
import subprocess
import time
from datetime import datetime

from locale import gettext as _tr

from Config import Config
from Services import Services
from Performance import Performance
from MainWindow import MainWindow


class ServicesDetails:

    def __init__(self):

        # Window GUI
        self.window_gui()


    def window_gui(self):
        """
        Generate window GUI.
        """

        # Window
        self.service_details_window = Gtk.Window()
        self.service_details_window.set_default_size(500, 435)
        self.service_details_window.set_title(_tr("Service Details"))
        self.service_details_window.set_icon_name("system-monitoring-center")
        self.service_details_window.set_transient_for(MainWindow.main_window)
        self.service_details_window.set_modal(True)
        self.service_details_window.set_hide_on_close(True)

        # Grid
        self.main_grid = Gtk.Grid()
        self.service_details_window.set_child(self.main_grid)

        # Notebook
        notebook = Gtk.Notebook()
        notebook.set_margin_top(10)
        notebook.set_margin_bottom(10)
        notebook.set_margin_start(10)
        notebook.set_margin_end(10)
        notebook.set_hexpand(True)
        notebook.set_vexpand(True)
        self.main_grid.attach(notebook, 0, 0, 1, 1)

        # Tab pages and ScrolledWindow
        # "Summary" tab
        tab_title_label = Gtk.Label()
        tab_title_label.set_label(_tr("Summary"))
        self.scrolledwindow_summary_tab = Gtk.ScrolledWindow()
        notebook.append_page(self.scrolledwindow_summary_tab, tab_title_label)
        # "Dependencies" tab
        tab_title_label = Gtk.Label()
        tab_title_label.set_label(_tr("Dependencies"))
        self.scrolledwindow_dependencies_tab = Gtk.ScrolledWindow()
        notebook.append_page(self.scrolledwindow_dependencies_tab, tab_title_label)

        # "Summary" tab GUI
        self.summary_tab_gui()
        # "Dependencies" tab GUI
        self.dependencies_tab_gui()

        # GUI signals
        self.gui_signals()


    def summary_tab_gui(self):
        """
        Generate "Summary" tab GUI objects.
        """

        # Viewport
        viewport = Gtk.Viewport()
        self.scrolledwindow_summary_tab.set_child(viewport)

        # Grid
        grid = Gtk.Grid()
        grid.set_margin_top(10)
        grid.set_margin_bottom(10)
        grid.set_margin_start(10)
        grid.set_margin_end(10)
        grid.set_column_spacing(10)
        grid.set_row_spacing(5)
        viewport.set_child(grid)

        # Label "Name"
        label = Gtk.Label()
        label.set_label(_tr("Name"))
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 0, 1, 1)

        # Label - Separator "Name"
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 1, 0, 1, 1)

        # Label - Variable "Name"
        self.name_label = Gtk.Label()
        self.name_label.set_selectable(True)
        self.name_label.set_label("--")
        self.name_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.name_label.set_halign(Gtk.Align.START)
        grid.attach(self.name_label, 2, 0, 1, 1)

        # Label "Description"
        label = Gtk.Label()
        label.set_label(_tr("Description"))
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 1, 1, 1)

        # Label - Separator "Description"
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 1, 1, 1, 1)

        # Label - Variable "Description"
        self.description_label = Gtk.Label()
        self.description_label.set_selectable(True)
        self.description_label.set_label("--")
        self.description_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.description_label.set_halign(Gtk.Align.START)
        grid.attach(self.description_label, 2, 1, 1, 1)

        # Label "Unit File State - Preset"
        label = Gtk.Label()
        label.set_label(_tr("Unit File State - Preset"))
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 2, 1, 1)

        # Label - Separator "Unit File State - Preset"
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 1, 2, 1, 1)

        # Label - Variable "Name"
        self.unit_file_state_label = Gtk.Label()
        self.unit_file_state_label.set_selectable(True)
        self.unit_file_state_label.set_label("--")
        self.unit_file_state_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.unit_file_state_label.set_halign(Gtk.Align.START)
        grid.attach(self.unit_file_state_label, 2, 2, 1, 1)

        # Label "Load State"
        label = Gtk.Label()
        label.set_label(_tr("Load State"))
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 3, 1, 1)

        # Label - Separator "Load State"
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 1, 3, 1, 1)

        # Label - Variable "Load State"
        self.load_state_label = Gtk.Label()
        self.load_state_label.set_selectable(True)
        self.load_state_label.set_label("--")
        self.load_state_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.load_state_label.set_halign(Gtk.Align.START)
        grid.attach(self.load_state_label, 2, 3, 1, 1)

        # Label "Active State"
        label = Gtk.Label()
        label.set_label(_tr("Active State"))
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 4, 1, 1)

        # Label - Separator "Active State"
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 1, 4, 1, 1)

        # Label - Variable "Active State"
        self.active_state_label = Gtk.Label()
        self.active_state_label.set_selectable(True)
        self.active_state_label.set_label("--")
        self.active_state_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.active_state_label.set_halign(Gtk.Align.START)
        grid.attach(self.active_state_label, 2, 4, 1, 1)

        # Label "Sub-State"
        label = Gtk.Label()
        label.set_label(_tr("Sub-State"))
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 5, 1, 1)

        # Label - Separator "Sub-State"
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 1, 5, 1, 1)

        # Label - Variable "Sub-State"
        self.sub_state_label = Gtk.Label()
        self.sub_state_label.set_selectable(True)
        self.sub_state_label.set_label("--")
        self.sub_state_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.sub_state_label.set_halign(Gtk.Align.START)
        grid.attach(self.sub_state_label, 2, 5, 1, 1)

        # Label "Path"
        label = Gtk.Label()
        label.set_label(_tr("Path"))
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 6, 1, 1)

        # Label - Separator "Path"
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 1, 6, 1, 1)

        # Label - Variable "Path"
        self.path_label = Gtk.Label()
        self.path_label.set_selectable(True)
        self.path_label.set_label("--")
        self.path_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.path_label.set_halign(Gtk.Align.START)
        grid.attach(self.path_label, 2, 6, 1, 1)

        # Label "Documentation"
        label = Gtk.Label()
        label.set_label(_tr("Documentation"))
        label.set_halign(Gtk.Align.START)
        label.set_valign(Gtk.Align.START)
        grid.attach(label, 0, 7, 1, 1)

        # Label - Separator "Documentation"
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        label.set_valign(Gtk.Align.START)
        grid.attach(label, 1, 7, 1, 1)

        # Label - Variable "Documentation"
        self.documentation_label = Gtk.Label()
        self.documentation_label.set_selectable(True)
        self.documentation_label.set_label("--")
        self.documentation_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.documentation_label.set_halign(Gtk.Align.START)
        grid.attach(self.documentation_label, 2, 7, 1, 1)

        # Label "Triggered By"
        label = Gtk.Label()
        label.set_label(_tr("Triggered By"))
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 8, 1, 1)

        # Label - Separator "Triggered By"
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 1, 8, 1, 1)

        # Label - Variable "Triggered By"
        self.triggered_by_label = Gtk.Label()
        self.triggered_by_label.set_selectable(True)
        self.triggered_by_label.set_label("--")
        self.triggered_by_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.triggered_by_label.set_halign(Gtk.Align.START)
        grid.attach(self.triggered_by_label, 2, 8, 1, 1)

        # Label "Main PID"
        label = Gtk.Label()
        label.set_label(_tr("Main PID"))
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 9, 1, 1)

        # Label - Separator "Main PID"
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 1, 9, 1, 1)

        # Label - Variable "Main PID"
        self.main_pid_label = Gtk.Label()
        self.main_pid_label.set_selectable(True)
        self.main_pid_label.set_label("--")
        self.main_pid_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.main_pid_label.set_halign(Gtk.Align.START)
        grid.attach(self.main_pid_label, 2, 9, 1, 1)

        # Label "Main Process Start Time"
        label = Gtk.Label()
        label.set_label(_tr("Main Process Start Time"))
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 10, 1, 1)

        # Label - Separator "Main Process Start Time"
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 1, 10, 1, 1)

        # Label - Variable "Main Process Start Time"
        self.main_process_start_time_label = Gtk.Label()
        self.main_process_start_time_label.set_selectable(True)
        self.main_process_start_time_label.set_label("--")
        self.main_process_start_time_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.main_process_start_time_label.set_halign(Gtk.Align.START)
        grid.attach(self.main_process_start_time_label, 2, 10, 1, 1)

        # Label "Main Process End Time"
        label = Gtk.Label()
        label.set_label(_tr("Main Process End Time"))
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 11, 1, 1)

        # Label - Separator "Main Process End Time"
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 1, 11, 1, 1)

        # Label - Variable "Main Process End Time"
        self.main_process_end_time_label = Gtk.Label()
        self.main_process_end_time_label.set_selectable(True)
        self.main_process_end_time_label.set_label("--")
        self.main_process_end_time_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.main_process_end_time_label.set_halign(Gtk.Align.START)
        grid.attach(self.main_process_end_time_label, 2, 11, 1, 1)

        # Label "Type"
        label = Gtk.Label()
        label.set_label(_tr("Type"))
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 12, 1, 1)

        # Label - Separator "Type"
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 1, 12, 1, 1)

        # Label - Variable "Type"
        self.type_label = Gtk.Label()
        self.type_label.set_selectable(True)
        self.type_label.set_label("--")
        self.type_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.type_label.set_halign(Gtk.Align.START)
        grid.attach(self.type_label, 2, 12, 1, 1)

        # Label "Memory (RSS)"
        label = Gtk.Label()
        label.set_label(_tr("Memory (RSS)"))
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 13, 1, 1)

        # Label - Separator "Memory (RSS)"
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 1, 13, 1, 1)

        # Label - Variable "Memory (RSS)"
        self.memory_rss_label = Gtk.Label()
        self.memory_rss_label.set_selectable(True)
        self.memory_rss_label.set_label("--")
        self.memory_rss_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.memory_rss_label.set_halign(Gtk.Align.START)
        grid.attach(self.memory_rss_label, 2, 13, 1, 1)


    def dependencies_tab_gui(self):
        """
        Generate "Dependencies" tab GUI objects.
        """

        # Viewport
        viewport = Gtk.Viewport()
        self.scrolledwindow_dependencies_tab.set_child(viewport)

        # Grid
        grid = Gtk.Grid()
        grid.set_margin_top(10)
        grid.set_margin_bottom(10)
        grid.set_margin_start(10)
        grid.set_margin_end(10)
        grid.set_column_spacing(10)
        grid.set_row_spacing(5)
        viewport.set_child(grid)

        # Label "Requires"
        label = Gtk.Label()
        label.set_label(_tr("Requires"))
        label.set_halign(Gtk.Align.START)
        label.set_valign(Gtk.Align.START)
        grid.attach(label, 0, 0, 1, 1)

        # Label - Separator "Requires"
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        label.set_valign(Gtk.Align.START)
        grid.attach(label, 1, 0, 1, 1)

        # Label - Variable "Requires"
        self.requires_label = Gtk.Label()
        self.requires_label.set_selectable(True)
        self.requires_label.set_label("--")
        self.requires_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.requires_label.set_halign(Gtk.Align.START)
        grid.attach(self.requires_label, 2, 0, 1, 1)

        # Label "Conflicts"
        label = Gtk.Label()
        label.set_label(_tr("Conflicts"))
        label.set_halign(Gtk.Align.START)
        label.set_valign(Gtk.Align.START)
        grid.attach(label, 0, 1, 1, 1)

        # Label - Separator "Conflicts"
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        label.set_valign(Gtk.Align.START)
        grid.attach(label, 1, 1, 1, 1)

        # Label - Variable "Conflicts"
        self.conflicts_label = Gtk.Label()
        self.conflicts_label.set_selectable(True)
        self.conflicts_label.set_label("--")
        self.conflicts_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.conflicts_label.set_halign(Gtk.Align.START)
        grid.attach(self.conflicts_label, 2, 1, 1, 1)

        # Label "After"
        label = Gtk.Label()
        label.set_label(_tr("After"))
        label.set_halign(Gtk.Align.START)
        label.set_valign(Gtk.Align.START)
        grid.attach(label, 0, 2, 1, 1)

        # Label - Separator "After"
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        label.set_valign(Gtk.Align.START)
        grid.attach(label, 1, 2, 1, 1)

        # Label - Variable "After"
        self.after_label = Gtk.Label()
        self.after_label.set_selectable(True)
        self.after_label.set_label("--")
        self.after_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.after_label.set_halign(Gtk.Align.START)
        grid.attach(self.after_label, 2, 2, 1, 1)

        # Label "Before"
        label = Gtk.Label()
        label.set_label(_tr("Before"))
        label.set_halign(Gtk.Align.START)
        label.set_valign(Gtk.Align.START)
        grid.attach(label, 0, 3, 1, 1)

        # Label - Separator "Before"
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        label.set_valign(Gtk.Align.START)
        grid.attach(label, 1, 3, 1, 1)

        # Label - Variable "Before"
        self.before_label = Gtk.Label()
        self.before_label.set_selectable(True)
        self.before_label.set_label("--")
        self.before_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.before_label.set_halign(Gtk.Align.START)
        grid.attach(self.before_label, 2, 3, 1, 1)


    def gui_signals(self):
        """
        Connect GUI signals.
        """

        # Window signals
        self.service_details_window.connect("close-request", self.on_service_details_window_delete_event)
        self.service_details_window.connect("show", self.on_service_details_window_show)


    def on_service_details_window_delete_event(self, widget):
        """
        Called when window close button (X) is clicked.
        """

        self.update_window_value = 0
        self.service_details_window.hide()
        return True


    def on_service_details_window_show(self, widget):
        """
        Run code after window is shown.
        """

        try:
            # Delete "update_interval" variable in order to let the code to run initial function.
            # Otherwise, data from previous service (if it was viewed) will be used.
            del self.update_interval
        except AttributeError:
            pass

        # This value is checked for repeating the function for getting the service data.
        self.update_window_value = 1

        self.services_details_run_func()


    # ----------------------------------- Services - Services Details Function (the code of this module in order to avoid running them during module import and defines "Services" tab GUI objects and functions/signals) -----------------------------------
    def services_details_initial_func(self):

        # Define data unit conversion function objects in for lower CPU usage.
        self.performance_define_data_unit_converter_variables_func = Performance.performance_define_data_unit_converter_variables_func
        self.performance_data_unit_converter_func = Performance.performance_data_unit_converter_func

        # Define data unit conversion variables before they are used.
        self.performance_define_data_unit_converter_variables_func()

        # Get right clicked service name.
        self.selected_service_name = Services.selected_service_name

        # Get system boot time (will be used for appending to process start times to get process start times as date time.)
        with open("/proc/stat") as reader:
            stat_lines = reader.read().split("\n")
        for line in stat_lines:
            if "btime " in line:
                self.system_boot_time = int(line.split()[1].strip())

        # These lists are defined in order to make these texts translatable to other languages. String names are capitalized here as they are capitalized in the code by using ".capitalize()" in order to use translated strings.
        service_state_list = [_tr("Enabled"), _tr("Disabled"), _tr("Masked"), _tr("Unmasked"), _tr("Static"), _tr("Generated"), _tr("Enabled-runtime"), _tr("Indirect"), _tr("Active"), _tr("Inactive"), _tr("Loaded"), _tr("Dead"), _tr("Exited"), _tr("Running")]
        services_other_text_list = [_tr("Yes"), _tr("No")]


    # ----------------------------------- Services - Services Details Foreground Function -----------------------------------
    def services_details_loop_func(self):

        services_memory_data_precision = Config.services_memory_data_precision
        services_memory_data_unit = Config.services_memory_data_unit

        selected_service_name = Services.selected_service_name

        # Get all information of the service.
        command_list = ["systemctl", "show", selected_service_name]
        if Config.environment_type == "flatpak":
            command_list = ["flatpak-spawn", "--host"] + command_list
        systemctl_show_lines = (subprocess.check_output(command_list, shell=False)).decode().strip().split("\n")

        # Initial value of the variables. These values will be used if they could not be detected.
        selected_service_type = "-"
        selected_service_main_pid = "-"
        selected_service_exec_main_start_times_stamp_monotonic = "-"
        selected_service_exec_main_exit_times_stamp_monotonic ="-"
        selected_service_memory_current = "-"
        selected_service_requires = "-"
        selected_service_conflicts = "-"
        selected_service_after = "-"
        selected_service_before = "-"
        selected_service_triggered_by = "-"
        selected_service_documentation = "-"
        selected_service_description = "-"
        selected_service_active_state = "-"
        selected_service_load_state = "-"
        selected_service_sub_state = "-"
        selected_service_fragment_path = "-"
        selected_service_unit_file_state = "-"
        selected_service_unit_file_preset = "-"

        for line in systemctl_show_lines:
            if "Type=" in line:
                selected_service_type = _tr(line.split("=")[1].capitalize())
                # Skip to next loop if searched line ("Type=") is found in order to avoid redundant line search.
                continue
            if "MainPID=" in line:
                selected_service_main_pid = line.split("=")[1]
                continue
            if "ExecMainStartTimestampMonotonic=" in line:
                line_split = line.split("=")[1]
                if line_split != "0":
                    # Time is read from the service file (in microseconds), divided by 1000000 in order to obtain time in seconds and appended to system boot time for getting service start time. Because time data is get as "elapsed time after system boot" from the file.
                    selected_service_exec_main_start_times_stamp_monotonic = int(line.split("=")[1])/1000000 + self.system_boot_time
                    selected_service_exec_main_start_times_stamp_monotonic = datetime.fromtimestamp(selected_service_exec_main_start_times_stamp_monotonic).strftime("%d.%m.%Y %H:%M:%S")
                if line_split == "0":
                    selected_service_exec_main_start_times_stamp_monotonic = "-"
                continue
            if "ExecMainExitTimestampMonotonic=" in line:
                line_split = line.split("=")[1]
                if line_split != "0":
                    # Time is read from the service file (in microseconds), divided by 1000000 in order to obtain time in seconds and appended to system boot time for getting service start time. Because time data is get as "elapsed time after system boot" from the file.
                    selected_service_exec_main_exit_times_stamp_monotonic = int(line.split("=")[1])/1000000 + self.system_boot_time
                    selected_service_exec_main_exit_times_stamp_monotonic = datetime.fromtimestamp(selected_service_exec_main_exit_times_stamp_monotonic).strftime("%d.%m.%Y %H:%M:%S")
                if line_split == "0":
                    selected_service_exec_main_exit_times_stamp_monotonic = "-"
                continue
            if "MemoryCurrent=" in line:
                selected_service_memory_current = line.split("=")[1]
                if selected_service_memory_current == "-" or selected_service_memory_current == "[not set]":
                    selected_service_memory_current = "-"
                else:
                    try:
                        selected_service_memory_current = f'{self.performance_data_unit_converter_func("data", "none", int(selected_service_memory_current), services_memory_data_unit, services_memory_data_precision)}'
                    except Exception:
                        selected_service_memory_current = "-"
                continue
            if "Requires=" in line:
                selected_service_requires = sorted(line.split("=")[1].split())
                continue
            if "Conflicts=" in line:
                selected_service_conflicts = sorted(line.split("=")[1].split())
                continue
            if "After=" in line:
                selected_service_after = sorted(line.split("=")[1].split())
                continue
            if "Before=" in line:
                selected_service_before = sorted(line.split("=")[1].split())
                continue
            if "TriggeredBy=" in line:
                selected_service_triggered_by = line.split("=")[1]
                continue
            if "Documentation=" in line:
                selected_service_documentation = line.split("=")[1].split()
                # Convert string into multi-line string if there are more than one documentation information.
                selected_service_documentation_scratch = []
                for documentation in selected_service_documentation:
                    selected_service_documentation_scratch.append(documentation.strip('"'))
                selected_service_documentation = selected_service_documentation_scratch
                continue
            if "Description=" in line:
                selected_service_description = line.split("=")[1]
                continue
            if "ActiveState=" in line:
                selected_service_active_state = _tr(line.split("=")[1].capitalize())
                continue
            if "LoadState=" in line:
                selected_service_load_state = _tr(line.split("=")[1].capitalize())
                continue
            if "SubState=" in line:
                selected_service_sub_state = _tr(line.split("=")[1].capitalize())
                continue
            if "FragmentPath=" in line:
                selected_service_fragment_path = line.split("=")[1]
                continue
            if "UnitFileState=" in line:
                selected_service_unit_file_state = _tr(line.split("=")[1].capitalize())
                continue
            if "UnitFilePreset=" in line:
                selected_service_unit_file_preset = _tr(line.split("=")[1].capitalize())
                continue


        # Set label text by using service data
        self.name_label.set_text(self.selected_service_name)
        self.description_label.set_text(selected_service_description)
        self.unit_file_state_label.set_text(f'{selected_service_unit_file_state} - {selected_service_unit_file_preset}')
        self.load_state_label.set_text(selected_service_load_state)
        self.active_state_label.set_text(selected_service_active_state)
        self.sub_state_label.set_text(selected_service_sub_state)
        self.path_label.set_text(selected_service_fragment_path)
        self.documentation_label.set_text(',\n'.join(selected_service_documentation))
        self.triggered_by_label.set_text(selected_service_triggered_by)
        self.main_pid_label.set_text(selected_service_main_pid)
        self.main_process_start_time_label.set_text(selected_service_exec_main_start_times_stamp_monotonic)
        self.main_process_end_time_label.set_text(selected_service_exec_main_exit_times_stamp_monotonic)
        self.type_label.set_text(selected_service_type)
        self.memory_rss_label.set_text(selected_service_memory_current)
        self.requires_label.set_text(',\n'.join(selected_service_requires))
        self.conflicts_label.set_text(',\n'.join(selected_service_conflicts))
        self.after_label.set_text(',\n'.join(selected_service_after))
        self.before_label.set_text(',\n'.join(selected_service_before))


    # ----------------------------------- Services Details - Run Function -----------------------------------
    # "*args" is used in order to prevent "" warning and obtain a repeated function by using "GLib.timeout_source_new()". "GLib.timeout_source_new()" is used instead of "GLib.timeout_add()" to be able to change the update interval and run the loop again without waiting ending the previous update interval.
    def services_details_run_func(self, *args):

        if hasattr(ServicesDetails, "update_interval") == False:
            GLib.idle_add(self.services_details_initial_func)

        # Destroy GLib source for preventing it repeating the function.
        try:
            self.main_glib_source.destroy()
        # "try-except" is used in order to prevent errors if this is first run of the function.
        except AttributeError:
            pass
        self.update_interval = Config.update_interval
        self.main_glib_source = GLib.timeout_source_new(self.update_interval * 1000)

        if self.update_window_value == 1:
            GLib.idle_add(self.services_details_loop_func)
            self.main_glib_source.set_callback(self.services_details_run_func)
            # Attach GLib.Source to MainContext. Therefore it will be part of the main loop until it is destroyed. A function may be attached to the MainContext multiple times.
            self.main_glib_source.attach(GLib.MainContext.default())


ServicesDetails = ServicesDetails()

