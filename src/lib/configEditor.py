#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Fri Dec 16 03:13:38 2011

import wx, wx.richtext
import project
import sys, os, re
from copy import deepcopy
from handlerSubsystem import *

# begin wxGlade: extracode
# end wxGlade

def drawParamConfigPane(target, paramList):
    list_sizer = wx.BoxSizer(wx.VERTICAL)
    param_controls = {}
    for p in paramList:
        print "name: %s, type: %s, default: %s" % (p.name, p.type, p.default)
        #SetToolTip(wx.ToolTip("click to hide")
        item_sizer = wx.BoxSizer(wx.HORIZONTAL)
        param_label = wx.StaticText(target, -1, "%s:" % p.name) 
        # TODO: add in different data types, min/max
        if p.type is not None:
            if p.default is not None:
                param_controls[p] = wx.TextCtrl(target, -1, p.default)
            else:
                param_controls[p] = wx.TextCtrl(target, -1, "")

        param_info_label = wx.StaticText(target, -1, "(%s)" % p.des)
        item_sizer = wx.BoxSizer(wx.HORIZONTAL)
        item_sizer.Add(param_label, 0, wx.ALL, 5)
        item_sizer.Add(param_controls[p], 1, wx.ALL, 5)
        item_sizer.Add(param_info_label, 0, wx.ALL, 5)
        list_sizer.Add(item_sizer, 0, wx.EXPAND, 0)
        #self.Bind(wx.EVT_BUTTON, self.onClickConfigure, self.handler_buttons[htype])
        #self.Bind(wx.EVT_COMBOBOX, self.onChangeHandler, self.handler_combos[htype])

    target.SetSizer(list_sizer)


class handlerConfigDialog(wx.Dialog):
    def __init__(self, parent, *args, **kwds):
        # begin wxGlade: handlerConfigDialog.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.label_info = wx.StaticText(self, -1, "info")
        self.static_line_2 = wx.StaticLine(self, -1)
        self.panel_configs = wx.ScrolledWindow(self, -1, style=wx.SUNKEN_BORDER|wx.TAB_TRAVERSAL)
        self.button_defaults = wx.Button(self, -1, "Reset to Defaults")
        self.button_OK = wx.Button(self, wx.ID_OK, "")
        self.button_1 = wx.Button(self, wx.ID_CANCEL, "")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.onClickDefaults, self.button_defaults)
        # end wxGlade

        self.proj = parent.proj
        self.hsub = parent.hsub

    def __set_properties(self):
        # begin wxGlade: handlerConfigDialog.__set_properties
        self.SetTitle("Configure XXXhandler")
        self.label_info.SetFont(wx.Font(10, wx.DEFAULT, wx.ITALIC, wx.NORMAL, 0, ""))
        self.panel_configs.SetScrollRate(10, 10)
        self.button_OK.SetDefault()
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: handlerConfigDialog.__do_layout
        sizer_10 = wx.BoxSizer(wx.VERTICAL)
        sizer_26 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_10.Add(self.label_info, 0, wx.ALL|wx.EXPAND, 5)
        sizer_10.Add(self.static_line_2, 0, wx.EXPAND, 0)
        sizer_10.Add(self.panel_configs, 1, wx.EXPAND, 0)
        sizer_26.Add(self.button_defaults, 0, wx.ALL, 5)
        sizer_26.Add((20, 20), 1, 0, 0)
        sizer_26.Add(self.button_OK, 0, wx.ALL, 5)
        sizer_26.Add(self.button_1, 0, wx.ALL, 5)
        sizer_10.Add(sizer_26, 0, wx.EXPAND, 0)
        self.SetSizer(sizer_10)
        sizer_10.Fit(self)
        self.Layout()
        # end wxGlade

    def _handler2dialog(self, handler):
        self.SetTitle("Configure %s.%s" % (handler.type, handler.name))
        methodObj = [m for m in handler.methods if m.name == '__init__'][0]

        drawParamConfigPane(self.panel_configs, methodObj.para)
        self.label_info.SetLabel(methodObj.comment)
        self.panel_configs.Layout()
        # FIXME: this is a sizing hack, because I can't figure out how to get Fit() to work
        a = self.panel_configs.GetSizer().GetMinSize()
        b = self.GetSizer().GetMinSize()
        self.SetSize((max(a[0],b[0]),a[1]+b[1]))
        self.Refresh()
        

    def onClickDefaults(self, event): # wxGlade: handlerConfigDialog.<event_handler>
        print "Event handler `onClickDefaults' not implemented"
        event.Skip()

# end of class handlerConfigDialog


class simSetupDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: simSetupDialog.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.THICK_FRAME
        wx.Dialog.__init__(self, *args, **kwds)
        self.sizer_22_staticbox = wx.StaticBox(self, -1, "Initial Conditions")
        self.sizer_1_staticbox = wx.StaticBox(self, -1, "Execution Environment")
        self.sizer_27_staticbox = wx.StaticBox(self, -1, "Experiment Settings")
        self.sizer_28_staticbox = wx.StaticBox(self, -1, "Experiment Configurations:")
        self.list_box_experiment_name = wx.ListBox(self, -1, choices=[])
        self.button_cfg_new = wx.Button(self, wx.ID_NEW, "")
        self.button_cfg_import = wx.Button(self, -1, "Import...")
        self.button_cfg_delete = wx.Button(self, wx.ID_DELETE, "")
        self.label_9 = wx.StaticText(self, -1, "Experiment Name: ")
        self.text_ctrl_sim_experiment_name = wx.TextCtrl(self, -1, "")
        self.label_2 = wx.StaticText(self, -1, "Custom Propositions:")
        self.list_box_init_customs = wx.CheckListBox(self, -1, choices=["1", "2"])
        self.label_2_copy = wx.StaticText(self, -1, "Action Propositions:")
        self.list_box_init_actions = wx.CheckListBox(self, -1, choices=["3", "4"])
        self.label_1 = wx.StaticText(self, -1, "Robots:")
        self.list_box_robots = wx.ListBox(self, -1, choices=[])
        self.button_addrobot = wx.Button(self, -1, "Add robot...")
        self.button_2 = wx.Button(self, -1, "Configure robot...")
        self.button_3 = wx.Button(self, -1, "Remove robot")
        self.button_4 = wx.Button(self, -1, "Edit proposition mapping...")
        self.button_sim_apply = wx.Button(self, wx.ID_APPLY, "")
        self.button_sim_ok = wx.Button(self, wx.ID_OK, "")
        self.button_sim_cancel = wx.Button(self, wx.ID_CANCEL, "")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_LISTBOX, self.onSimLoad, self.list_box_experiment_name)
        self.Bind(wx.EVT_BUTTON, self.onConfigNew, self.button_cfg_new)
        self.Bind(wx.EVT_BUTTON, self.onConfigImport, self.button_cfg_import)
        self.Bind(wx.EVT_BUTTON, self.onConfigDelete, self.button_cfg_delete)
        self.Bind(wx.EVT_TEXT, self.onSimNameEdit, self.text_ctrl_sim_experiment_name)
        self.Bind(wx.EVT_BUTTON, self.onClickAddRobot, self.button_addrobot)
        self.Bind(wx.EVT_BUTTON, self.onClickConfigureRobot, self.button_2)
        self.Bind(wx.EVT_BUTTON, self.onClickRemoveRobot, self.button_3)
        self.Bind(wx.EVT_BUTTON, self.onClickEditMapping, self.button_4)
        self.Bind(wx.EVT_BUTTON, self.onClickApply, self.button_sim_apply)
        self.Bind(wx.EVT_BUTTON, self.onClickOK, self.button_sim_ok)
        # end wxGlade

        self.Bind(wx.EVT_CHECKLISTBOX, self.onCheckProp, self.list_box_init_customs)
        self.Bind(wx.EVT_CHECKLISTBOX, self.onCheckProp, self.list_box_init_actions)

        if len(sys.argv) < 2:
            print "You must specify a specification file."
            print "Usage: %s [spec_file]" % sys.argv[0]
            sys.exit(2)

        # Load project

        self.proj = project.Project()
        self.proj.loadProject(sys.argv[1])

        # Initialize handler subsystem
        
        self.hsub = HandlerSubsystem(self.proj)

        # Set up the list of configs
        self.list_box_experiment_name.Clear()
        
        self.hsub.loadAllConfigFiles()

        current_config = self.proj.spec_data['SETTINGS']['currentExperimentName'][0]

        for cfg in self.hsub.configs:
            self.list_box_experiment_name.Append(cfg.name, cfg)
            if cfg.name == current_config:
                self.list_box_experiment_name.SetStringSelection(cfg.name)
                self._cfg2dialog(cfg)

        # Check for case where no config files are present
        if self.list_box_experiment_name.GetCount() == 0:
            # Create blank default config
            cfg = ConfigObject()
            # TODO: Check for existing untitleds and add a number at the end (steal from reged)
            cfg.name = "Untitled configuration"
            self.hsub.config_parser.configs.append(cfg)
            self.list_box_experiment_name.Append(cfg.name, cfg)
            self._cfg2dialog(cfg)

        # Check for case where a non-existent config file is referenced in the spec file
        if current_config not in [c.name for c in self.hsub.configs]:
            print "WARNING: Cannot find config '%s' as referenced in spec file.  Ignoring." % current_config
            self.list_box_experiment_name.Select(0)
            self._cfg2dialog(self.list_box_experiment_name.GetClientData(0))

    def __set_properties(self):
        # begin wxGlade: simSetupDialog.__set_properties
        self.SetTitle("Configure Execution")
        self.SetSize((935, 508))
        self.text_ctrl_sim_experiment_name.SetMinSize((300, 27))
        self.list_box_init_customs.SetSelection(0)
        self.list_box_init_actions.SetSelection(0)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: simSetupDialog.__do_layout
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_12 = wx.BoxSizer(wx.VERTICAL)
        sizer_13 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_27 = wx.StaticBoxSizer(self.sizer_27_staticbox, wx.VERTICAL)
        sizer_1 = wx.StaticBoxSizer(self.sizer_1_staticbox, wx.HORIZONTAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_22 = wx.StaticBoxSizer(self.sizer_22_staticbox, wx.VERTICAL)
        sizer_23 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_17_copy = wx.BoxSizer(wx.VERTICAL)
        sizer_17 = wx.BoxSizer(wx.VERTICAL)
        sizer_30 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_29 = wx.BoxSizer(wx.VERTICAL)
        sizer_28 = wx.StaticBoxSizer(self.sizer_28_staticbox, wx.VERTICAL)
        sizer_29_copy = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6.Add((20, 20), 0, 0, 0)
        sizer_29.Add((20, 20), 0, 0, 0)
        sizer_28.Add((20, 10), 0, 0, 0)
        sizer_28.Add(self.list_box_experiment_name, 1, wx.EXPAND, 0)
        sizer_28.Add((20, 20), 0, 0, 0)
        sizer_29_copy.Add(self.button_cfg_new, 0, 0, 0)
        sizer_29_copy.Add((10, 20), 0, 0, 0)
        sizer_29_copy.Add(self.button_cfg_import, 0, 0, 0)
        sizer_29_copy.Add((10, 20), 0, 0, 0)
        sizer_29_copy.Add(self.button_cfg_delete, 0, 0, 0)
        sizer_28.Add(sizer_29_copy, 0, wx.EXPAND, 0)
        sizer_28.Add((20, 10), 0, 0, 0)
        sizer_29.Add(sizer_28, 1, wx.EXPAND, 0)
        sizer_6.Add(sizer_29, 1, wx.EXPAND, 0)
        sizer_6.Add((20, 20), 0, 0, 0)
        sizer_12.Add((20, 20), 0, 0, 0)
        sizer_30.Add(self.label_9, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_30.Add((20, 20), 0, 0, 0)
        sizer_30.Add(self.text_ctrl_sim_experiment_name, 0, 0, 0)
        sizer_12.Add(sizer_30, 0, wx.EXPAND, 0)
        sizer_12.Add((20, 20), 0, 0, 0)
        sizer_23.Add((5, 20), 0, 0, 0)
        sizer_17.Add(self.label_2, 0, 0, 0)
        sizer_17.Add(self.list_box_init_customs, 1, wx.EXPAND, 0)
        sizer_23.Add(sizer_17, 1, wx.EXPAND, 0)
        sizer_23.Add((20, 20), 0, 0, 0)
        sizer_17_copy.Add(self.label_2_copy, 0, 0, 0)
        sizer_17_copy.Add(self.list_box_init_actions, 1, wx.EXPAND, 0)
        sizer_23.Add(sizer_17_copy, 1, wx.EXPAND, 0)
        sizer_23.Add((5, 20), 0, 0, 0)
        sizer_22.Add(sizer_23, 5, wx.EXPAND, 0)
        sizer_27.Add(sizer_22, 1, wx.ALL|wx.EXPAND, 10)
        sizer_3.Add(self.label_1, 0, 0, 0)
        sizer_3.Add(self.list_box_robots, 1, wx.EXPAND, 0)
        sizer_2.Add(sizer_3, 1, wx.EXPAND, 0)
        sizer_2.Add((20, 20), 0, 0, 0)
        sizer_4.Add(self.button_addrobot, 0, wx.BOTTOM, 5)
        sizer_4.Add(self.button_2, 0, wx.BOTTOM, 5)
        sizer_4.Add(self.button_3, 0, 0, 0)
        sizer_4.Add((20, 60), 0, 0, 0)
        sizer_4.Add(self.button_4, 0, 0, 0)
        sizer_2.Add(sizer_4, 1, wx.EXPAND, 0)
        sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)
        sizer_27.Add(sizer_1, 0, wx.ALL|wx.EXPAND, 10)
        sizer_12.Add(sizer_27, 1, wx.EXPAND, 0)
        sizer_13.Add(self.button_sim_apply, 0, 0, 0)
        sizer_13.Add((10, 20), 0, 0, 0)
        sizer_13.Add(self.button_sim_ok, 0, 0, 0)
        sizer_13.Add((10, 20), 0, 0, 0)
        sizer_13.Add(self.button_sim_cancel, 0, 0, 0)
        sizer_13.Add((10, 10), 0, 0, 0)
        sizer_12.Add(sizer_13, 0, wx.ALIGN_RIGHT, 0)
        sizer_12.Add((20, 10), 0, 0, 0)
        sizer_6.Add(sizer_12, 2, wx.EXPAND, 0)
        sizer_6.Add((20, 20), 0, 0, 0)
        self.SetSizer(sizer_6)
        self.Layout()
        self.Centre()
        # end wxGlade

    def _cfg2dialog(self, cfg):
        self.text_ctrl_sim_experiment_name.SetValue(cfg.name)

        # Set up the initial actions checklist as appropriate
        self.list_box_init_actions.Set([])
        for i, action in enumerate(self.proj.all_actuators):
            self.list_box_init_actions.Insert(action, i)
            if action in cfg.initial_truths:
                self.list_box_init_actions.Check(i)

        # Set up the initial customs checklist as appropriate
        self.list_box_init_customs.Set([])
        for i, custom in enumerate(self.proj.all_customs):
            self.list_box_init_customs.Insert(custom, i)
            if custom in cfg.initial_truths:
                self.list_box_init_customs.Check(i)

        # Set up the robots list
        self.list_box_robots.Set([])
        for i, robot in enumerate(cfg.robots):
            self.list_box_robots.Insert(robot.name, i, robot)

        if len(cfg.robots) > 0:
            self.list_box_robots.Select(0)

    def onSimLoad(self, event): # wxGlade: simSetupDialog.<event_handler>
        cfg = event.GetClientData()
        if cfg is not None:
            self._cfg2dialog(cfg)
        event.Skip()

    def onConfigNew(self, event): # wxGlade: simSetupDialog.<event_handler>
        # Create blank default config
        cfg = ConfigObject()

        # TODO: Check for existing untitleds and add a number at the end (steal from reged)
        cfg.name = "Untitled configuration"
        self.hsub.config_parser.configs.append(cfg)

        self.list_box_experiment_name.Append(cfg.name, cfg)
        self.list_box_experiment_name.Select(self.list_box_experiment_name.GetCount()-1)
        self._cfg2dialog(cfg)
        event.Skip()

    def onConfigImport(self, event): # wxGlade: simSetupDialog.<event_handler>
        fileName = wx.FileSelector("Import Config File", default_extension="config",
                                  wildcard="Experiment config files (*.config)|*.config",
                                  flags = wx.OPEN | wx.FILE_MUST_EXIST)
        if fileName == "": return

        # import the config file
        cfg = self.hsub.config_parser.loadConfigFile(fileName)        
        self.hsub.config_parser.configs.append(cfg)
        self.list_box_experiment_name.Append(cfg.name, cfg)
        self.list_box_experiment_name.Select(self.list_box_experiment_name.GetCount()-1)
        self._cfg2dialog(cfg)

        event.Skip()

    def onConfigDelete(self, event): # wxGlade: simSetupDialog.<event_handler>
        if self.list_box_experiment_name.GetSelection() == -1:
            return

        numel = self.list_box_experiment_name.GetCount()
        if numel > 1:  # don't allow deletion of final remaining element
            # TODO: gray out button when no action possible
            pos = self.list_box_experiment_name.GetSelection()
            self.list_box_experiment_name.Delete(pos)
            self.hsub.config_parser.configs.pop(pos)

            if pos == numel - 1:
                # If the very last element was deleted, move the selection up one
                newpos = pos - 1
            else:
                newpos = pos

            self.list_box_experiment_name.Select(newpos)
            self._cfg2dialog(self.list_box_experiment_name.GetClientData(newpos))

        event.Skip()

    def onSimNameEdit(self, event): # wxGlade: simSetupDialog.<event_handler>
        pos = self.list_box_experiment_name.GetSelection()
        self.list_box_experiment_name.GetClientData(pos).name = event.GetString()
        self.list_box_experiment_name.SetString(pos, event.GetString())
        event.Skip()

    def onClickAddRobot(self, event): # wxGlade: simSetupDialog.<event_handler>
        dlg = addRobotDialog(self, None, -1, "")
        if dlg.ShowModal() != wx.ID_CANCEL:
            obj = self._getSelectedConfigObject()
            obj.robots += [dlg.robot]
            self._cfg2dialog(obj)
        dlg.Destroy()
        event.Skip()

    def onClickConfigureRobot(self, event): # wxGlade: simSetupDialog.<event_handler>
        # TODO: gray out button when no action possible
        if self.list_box_robots.GetSelection() == -1:
            return

        dlg = addRobotDialog(self, None, -1, "")

        pos = self.list_box_robots.GetSelection()
        r = self.list_box_robots.GetClientData(pos)
        dlg._robot2dialog(r)
        if dlg.ShowModal() != wx.ID_CANCEL:
            r = dlg.robot
            obj = self._getSelectedConfigObject()
            self._cfg2dialog(obj)
        dlg.Destroy()
        event.Skip()

    def onClickRemoveRobot(self, event): # wxGlade: simSetupDialog.<event_handler>
        if self.list_box_robots.GetSelection() == -1:
            return

        numel = self.list_box_robots.GetCount()
        obj = self._getSelectedConfigObject()

        # TODO: gray out button when no action possible
        if numel > 0:
            pos = self.list_box_robots.GetSelection()
            #self.list_box_robots.Delete(pos)
            obj.robots.pop(pos)
            self._cfg2dialog(obj)

            if pos == numel - 1:
                # If the very last element was deleted, move the selection up one
                newpos = pos -1
            else:
                newpos = pos

            if pos != -1:
                self.list_box_robots.Select(newpos)

        event.Skip()

    def onClickEditMapping(self, event): # wxGlade: simSetupDialog.<event_handler>
        dlg = propMappingDialog(self, None, -1, "")
        obj = self._getSelectedConfigObject()
        dlg._mapping2dialog(obj.prop_mapping)
        if dlg.ShowModal() != wx.ID_CANCEL:
            obj.prop_mapping = dlg.mapping
        dlg.Destroy()
        event.Skip()

    def onClickApply(self, event): # wxGlade: simSetupDialog.<event_handler>
        print "Event handler `onClickApply' not implemented!"
        event.Skip()

    def onClickOK(self, event): # wxGlade: simSetupDialog.<event_handler>
        for j in xrange(self.list_box_experiment_name.GetCount()):
            self.list_box_experiment_name.GetClientData(j).saveConfigFile()
        self.Destroy()


    def _getSelectedConfigObject(self):
        pos = self.list_box_experiment_name.GetSelection()
        obj = self.list_box_experiment_name.GetClientData(pos)
        return obj

    def onCheckProp(self, event): # wxGlade: simSetupDialog.<event_handler>
        obj = event.GetEventObject()
        i = event.GetInt()
        newstate = obj.IsChecked(i)
        name = obj.GetString(i)

        obj = self._getSelectedConfigObject()

        if newstate == True:
            obj.initial_truths += [name]
        else:
            obj.initial_truths.remove(name)

        event.Skip()

# end of class simSetupDialog


class addRobotDialog(wx.Dialog):
    def __init__(self, parent, *args, **kwds):
        # begin wxGlade: addRobotDialog.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.label_3 = wx.StaticText(self, -1, "Robot type:")
        self.combo_box_robottype = wx.ComboBox(self, -1, choices=[], style=wx.CB_DROPDOWN)
        self.label_4 = wx.StaticText(self, -1, "Robot name:")
        self.text_ctrl_robotname = wx.TextCtrl(self, -1, "")
        self.static_line_1 = wx.StaticLine(self, -1)
        self.button_7 = wx.Button(self, wx.ID_CANCEL, "")
        self.button_6 = wx.Button(self, wx.ID_OK, "")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_COMBOBOX, self.onChooseRobot, self.combo_box_robottype)
        self.Bind(wx.EVT_TEXT, self.onEditRobotName, self.text_ctrl_robotname)
        self.Bind(wx.EVT_BUTTON, self.onClickOK, self.button_6)
        # end wxGlade

        self.proj = parent.proj
        self.hsub = parent.hsub
        self.robot = RobotObject()

        self.handler_labels = {}
        self.handler_combos = {}
        self.handler_buttons = {}

        self.hsub.loadAllHandlers()
        self.hsub.loadAllRobots()
        
        for htype in self.robot.handlers.keys():
            self.handler_labels[htype] = wx.StaticText(self, -1, "%s:" % htype) 
            if htype in self.hsub.handler_parser.handler_robotSpecific_type: 
                print htype, self.hsub.handler_dic[htype]
                # TODO: use correct robot
                self.handler_combos[htype] = wx.ComboBox(self, -1, choices=[h.name for h in self.hsub.handler_dic[htype]["nao"]], style=wx.CB_DROPDOWN)
            else:
                self.handler_combos[htype] = wx.ComboBox(self, -1, choices=[h.name for h in self.hsub.handler_dic[htype]], style=wx.CB_DROPDOWN)
            self.handler_buttons[htype] = wx.Button(self, -1, "Configure...")
            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(self.handler_labels[htype], 0, wx.ALL, 2)
            sizer.Add(self.handler_combos[htype], 1, wx.ALL, 2)
            sizer.Add(self.handler_buttons[htype], 0, wx.ALL, 2)
            self.sizer_9.Add(sizer, 0, wx.EXPAND, 0)
            self.Bind(wx.EVT_BUTTON, self.onClickConfigure, self.handler_buttons[htype])
            self.Bind(wx.EVT_COMBOBOX, self.onChangeHandler, self.handler_combos[htype])

        self.Layout()

        # Set up the list of robot types
        self.combo_box_robottype.Clear()

        for r in self.hsub.robots:
            self.combo_box_robottype.Append(r.type)
            if r.type == self.robot.type:
                self.combo_box_robottype.SetStringSelection(r)

    def __set_properties(self):
        # begin wxGlade: addRobotDialog.__set_properties
        self.SetTitle("Add/Configure Robot")
        self.SetSize((388, 410))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: addRobotDialog.__do_layout
        sizer_5 = wx.BoxSizer(wx.VERTICAL)
        sizer_11 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_9 = wx.BoxSizer(wx.VERTICAL)
        sizer_8 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_7 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_7.Add(self.label_3, 0, wx.ALL, 5)
        sizer_7.Add(self.combo_box_robottype, 1, wx.ALL, 5)
        sizer_5.Add(sizer_7, 0, wx.EXPAND, 0)
        sizer_8.Add(self.label_4, 0, wx.ALL, 5)
        sizer_8.Add(self.text_ctrl_robotname, 1, wx.ALL, 5)
        sizer_5.Add(sizer_8, 0, wx.EXPAND, 0)
        sizer_5.Add(self.static_line_1, 0, wx.EXPAND, 0)
        sizer_5.Add(sizer_9, 1, wx.EXPAND, 0)
        sizer_5.Add((20, 20), 1, wx.EXPAND, 0)
        sizer_11.Add((20, 20), 1, wx.EXPAND, 0)
        sizer_11.Add(self.button_7, 0, wx.ALL, 5)
        sizer_11.Add(self.button_6, 0, wx.ALL, 5)
        sizer_5.Add(sizer_11, 0, wx.EXPAND, 0)
        self.SetSizer(sizer_5)
        self.Layout()
        # end wxGlade
        self.sizer_9 = sizer_9

    def _robot2dialog(self, robot):
        self.robot = robot
        self.combo_box_robottype.SetStringSelection(self.robot.type)
        self.text_ctrl_robotname.SetValue(self.robot.name)
        for htype, h in self.robot.handlers.iteritems():
            # select the appropriate handler
            # TODO: what should the correct behavior be if it doesn't exist in the list of handlers already?
            if h is not None:
                self.handler_combos[htype].SetStringSelection(h.name)
            else:   
                self.handler_combos[htype].SetValue("")

    def onClickConfigure(self, event):
        src = event.GetEventObject()
        
        # Figure out which "Configure..." button was pressed
        for htype, b in self.handler_buttons.iteritems():
            if src is b:
                # TODO: gray out button when no action possible
                if self.handler_combos[htype].GetValue() == "":
                    return

                dlg = handlerConfigDialog(self, None, -1, "")
                hname = self.handler_combos[htype].GetValue()
                rname = self.robot.type

                if htype in self.hsub.handler_parser.handler_robotSpecific_type: 
                    hobj = [h for h in self.hsub.handler_dic[htype][rname] if h.name == hname][0]
                else:
                    hobj = [h for h in self.hsub.handler_dic[htype] if h.name == hname][0]

                dlg._handler2dialog(hobj)

                if dlg.ShowModal() != wx.ID_CANCEL:
                    #r = dlg.robot
                    #self._cfg2dialog(obj)
                    pass
                dlg.Destroy()
                break


        event.Skip()

    def onChangeHandler(self, event):
        src = event.GetEventObject()
        
        # Figure out which handler was changed
        for htype, b in self.handler_combos.iteritems():
            if src is b:
                #print "handler for %s is now %s" % (htype, src.GetValue())
                # TODO: this will erase any previous config settings...
                self.robot.handlers[htype] = src.GetValue()
                break

        event.Skip()

    def onClickOK(self, event): # wxGlade: addRobotDialog.<event_handler>
        event.Skip()

    def onChooseRobot(self, event): # wxGlade: addRobotDialog.<event_handler>
        #self.robot.name = event.GetString()
        #self.robot.type = event.GetString()
        self.robot = deepcopy([r for r in self.hsub.robots if r.type == event.GetString()][0])
        self._robot2dialog(self.robot)
        event.Skip()

    def onEditRobotName(self, event): # wxGlade: addRobotDialog.<event_handler>
        self.robot.name = event.GetString()
        event.Skip()

# end of class addRobotDialog


class propMappingDialog(wx.Dialog):
    def __init__(self, parent, *args, **kwds):
        # begin wxGlade: propMappingDialog.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.THICK_FRAME
        wx.Dialog.__init__(self, *args, **kwds)
        self.label_6 = wx.StaticText(self, -1, "Propositions:")
        self.list_box_props = wx.ListBox(self, -1, choices=[], style=wx.LB_SINGLE|wx.LB_ALWAYS_SB)
        self.label_11 = wx.StaticText(self, -1, "Continuous controller mapping:")
        self.text_ctrl_mapping = wx.richtext.RichTextCtrl(self, -1, "")
        self.button_8 = wx.Button(self, -1, u"Edit\n  ↓")
        self.button_9 = wx.Button(self, -1, u"        ↑\nInsert/Apply")
        self.label_7 = wx.StaticText(self, -1, "Robots:")
        self.list_box_robots = wx.ListBox(self, -1, choices=[])
        self.label_8 = wx.StaticText(self, -1, "Sensors/Actuators:")
        self.list_box_functions = wx.ListBox(self, -1, choices=[])
        self.label_10 = wx.StaticText(self, -1, "Parameters:")
        self.button_11 = wx.Button(self, wx.ID_CANCEL, "")
        self.button_10 = wx.Button(self, wx.ID_OK, "")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_LISTBOX, self.onSelectProp, self.list_box_props)
        self.Bind(wx.EVT_TEXT, self.onEditMapping, self.text_ctrl_mapping)
        self.Bind(wx.EVT_BUTTON, self.onClickEdit, self.button_8)
        self.Bind(wx.EVT_BUTTON, self.onClickApply, self.button_9)
        self.Bind(wx.EVT_LISTBOX, self.onSelectRobot, self.list_box_robots)
        self.Bind(wx.EVT_LISTBOX, self.onSelectHandler, self.list_box_functions)
        self.Bind(wx.EVT_BUTTON, self.onClickOK, self.button_10)
        # end wxGlade

        self.text_ctrl_mapping.Bind(wx.EVT_TEXT, self.onEditMapping)
        self.text_ctrl_mapping.Bind(wx.EVT_LEFT_UP, self.onClickMapping)
        #self.Bind(wx.EVT_LEFT_UP, self.onClickMapping, self.text_ctrl_mapping)
        #self.text_ctrl_mapping.Bind(wx.EVT_LEFT_DOWN, self.onClickMapping)
        self.text_ctrl_mapping.Bind(wx.EVT_KEY_UP, self.onClickMapping)
        self.text_ctrl_mapping.Bind(wx.EVT_KEY_DOWN, self.onClickMapping)

        self.proj = parent.proj
        self.robots = parent._getSelectedConfigObject().robots

        # Set up the list of robots

        for r in self.robots:
            self.list_box_robots.Append("%s (%s)" % (r.name, r.type))

        # Set up the list of props
        self.list_box_props.Clear()
        
        self.list_box_props.Append("=== Sensors ===")

        for p in self.proj.all_sensors:
            self.list_box_props.Append(p)

        self.list_box_props.Append("=== Actuators ===")

        for p in self.proj.all_actuators:
            self.list_box_props.Append(p)

        self.mapping = None

    def _mapping2dialog(self, mapping):
        self.mapping = deepcopy(mapping)

    def __set_properties(self):
        # begin wxGlade: propMappingDialog.__set_properties
        self.SetTitle("Proposition Mapping")
        self.SetSize((836, 616))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: propMappingDialog.__do_layout
        sizer_14 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_16 = wx.BoxSizer(wx.VERTICAL)
        sizer_25 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_19 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_24 = wx.BoxSizer(wx.VERTICAL)
        sizer_21 = wx.BoxSizer(wx.VERTICAL)
        sizer_20 = wx.BoxSizer(wx.VERTICAL)
        sizer_18 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_15 = wx.BoxSizer(wx.VERTICAL)
        sizer_15.Add(self.label_6, 0, wx.LEFT|wx.RIGHT|wx.TOP, 5)
        sizer_15.Add(self.list_box_props, 1, wx.ALL|wx.EXPAND, 5)
        sizer_14.Add(sizer_15, 1, wx.EXPAND, 0)
        sizer_16.Add(self.label_11, 0, wx.ALL, 5)
        sizer_16.Add(self.text_ctrl_mapping, 1, wx.ALL|wx.EXPAND, 5)
        sizer_18.Add((20, 20), 1, wx.EXPAND, 0)
        sizer_18.Add(self.button_8, 0, wx.ALL, 5)
        sizer_18.Add((40, 20), 0, 0, 0)
        sizer_18.Add(self.button_9, 0, wx.ALL, 5)
        sizer_18.Add((20, 20), 1, wx.EXPAND, 0)
        sizer_16.Add(sizer_18, 0, wx.EXPAND, 0)
        sizer_20.Add(self.label_7, 0, wx.ALL, 5)
        sizer_20.Add(self.list_box_robots, 1, wx.ALL|wx.EXPAND, 5)
        sizer_19.Add(sizer_20, 1, wx.EXPAND, 0)
        sizer_21.Add(self.label_8, 0, wx.ALL, 5)
        sizer_21.Add(self.list_box_functions, 1, wx.ALL|wx.EXPAND, 5)
        sizer_19.Add(sizer_21, 1, wx.EXPAND, 0)
        sizer_24.Add(self.label_10, 0, wx.ALL, 5)
        sizer_19.Add(sizer_24, 1, wx.EXPAND, 0)
        sizer_16.Add(sizer_19, 5, wx.EXPAND, 0)
        sizer_25.Add((20, 20), 1, wx.EXPAND, 0)
        sizer_25.Add(self.button_11, 0, wx.ALL, 5)
        sizer_25.Add(self.button_10, 0, wx.ALL, 5)
        sizer_16.Add(sizer_25, 0, wx.EXPAND, 0)
        sizer_14.Add(sizer_16, 2, wx.EXPAND, 0)
        self.SetSizer(sizer_14)
        self.Layout()
        # end wxGlade

    def onSelectProp(self, event): # wxGlade: propMappingDialog.<event_handler>
        # If you've selected a header, not a proposition, then gray out the edit box
        if event.GetString().startswith("==="):
            self.text_ctrl_mapping.SetValue("")
            self.text_ctrl_mapping.Enable(False)
        else:
            self.text_ctrl_mapping.Enable(True)
            if event.GetString() in self.mapping:
                self.text_ctrl_mapping.SetValue(self.mapping[event.GetString()])
            else:
                self.text_ctrl_mapping.SetValue("")
        event.Skip()

    def onClickEdit(self, event): # wxGlade: propMappingDialog.<event_handler>
        print "Event handler `onClickEdit' not implemented!"
        event.Skip()

    def onClickApply(self, event): # wxGlade: propMappingDialog.<event_handler>
        print "Event handler `onClickApply' not implemented!"
        event.Skip()

    def onSelectRobot(self, event): # wxGlade: propMappingDialog.<event_handler>
        print "Event handler `onSelectRobot' not implemented!"
        event.Skip()

    def onSelectHandler(self, event): # wxGlade: propMappingDialog.<event_handler>
        print "Event handler `onSelectHandler' not implemented!"
        event.Skip()

    def onClickOK(self, event): # wxGlade: propMappingDialog.<event_handler>
        print "Event handler `onClickOK' not implemented!"
        event.Skip()

    def onClickMapping(self, event):
        event.Skip()

        if event.GetEventType() in [wx.wxEVT_KEY_DOWN, wx.wxEVT_KEY_UP] and \
           event.GetKeyCode() not in [wx.WXK_LEFT, wx.WXK_RIGHT, wx.WXK_UP, wx.WXK_DOWN, wx.WXK_HOME, wx.WXK_END, \
                                      wx.WXK_NUMPAD_LEFT, wx.WXK_NUMPAD_RIGHT, wx.WXK_NUMPAD_UP, wx.WXK_NUMPAD_DOWN]:
            return
        
        # Check to see if we're clicking or keying to a keyword
        s = self.text_ctrl_mapping.GetValue()
        i = self.text_ctrl_mapping.GetInsertionPoint()

        p = re.compile(r"(?P<robot>\w+)\.(?P<type>\w+)\.(?P<name>\w+)\((?P<args>[^\)]*)\)")
        m_local = None

        for m in p.finditer(s):
            if i > m.start() and i < m.end():
                m_local = m 
                break 

        if m_local is None:
            return
        else:
            m = m_local

        # Make sure the robot name is valid
            
        corresponding_robots = [n for n in self.list_box_robots.GetItems() if n.startswith(m.group("robot"))]

        if len(corresponding_robots) != 1:
            print "WARNING: No unique robot corresponding to name '%s'." % m.group("robot")
            return

        # Force selection of the entire keyword, and place insertion caret as appropriate
        self.text_ctrl_mapping.SetSelection(m.start(),m.end())
        if event.GetEventType() in [wx.wxEVT_KEY_DOWN, wx.wxEVT_KEY_UP]:
            if event.GetKeyCode() in [wx.WXK_LEFT, wx.WXK_HOME, wx.WXK_UP, wx.WXK_NUMPAD_LEFT, wx.WXK_NUMPAD_UP]:
                self.text_ctrl_mapping.MoveCaret(m.start()-1)
            elif event.GetKeyCode() in [wx.WXK_RIGHT, wx.WXK_END, wx.WXK_DOWN, wx.WXK_NUMPAD_RIGHT, wx.WXK_NUMPAD_DOWN]:
                self.text_ctrl_mapping.MoveCaret(m.end()-1)

        # Load detailed view of keyword below
            
        self.list_box_robots.SetStringSelection(corresponding_robots[0])
        #self.list_box_robots.SetStringSelection(corresponding_robots[0])
        #self.list_box_robots.SetStringSelection(corresponding_robots[0])

        event.Skip()

    def onEditMapping(self, event): # wxGlade: propMappingDialog.<event_handler>
        if not self.text_ctrl_mapping.IsEnabled() or \
           self.text_ctrl_mapping.GetValue() == "":
            return

        prop_name = self.list_box_props.GetStringSelection()
        self.mapping[prop_name] = self.text_ctrl_mapping.GetValue()

        event.Skip()

# end of class propMappingDialog


if __name__ == "__main__":
    SimConfigEditor = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    SimSetupDialog = simSetupDialog(None, -1, "")
    SimConfigEditor.SetTopWindow(SimSetupDialog)
    SimSetupDialog.Show()
    SimConfigEditor.MainLoop()
