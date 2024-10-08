# -*- coding: utf-8 -*-
#
####################################################
#
# PRISM - Pipeline for animation and VFX projects
#
# www.prism-pipeline.com
#
# contact: contact@prism-pipeline.com
#
####################################################
#
#
# Copyright (C) 2016-2023 Richard Frangenberg
# Copyright (C) 2023 Prism Software GmbH
#
# Licensed under GNU LGPL-3.0-or-later
#
# This file is part of Prism.
#
# Prism is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Prism is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Prism.  If not, see <https://www.gnu.org/licenses/>.


import os
import platform

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

from PrismUtils.Decorators import err_catcher_plugin as err_catcher


class Prism_Fusion_externalAccess_Functions(object):
	def __init__(self, core, plugin):
		self.core = core
		self.plugin = plugin
		###
		self.core.registerCallback(
			"userSettings_saveSettings",
			self.userSettings_saveSettings,
			plugin=self.plugin,
		)
		self.core.registerCallback(
			"userSettings_loadSettings",
			self.userSettings_loadSettings,
			plugin=self.plugin,
		)
		self.core.registerCallback(
			"getPresetScenes", 
			self.getPresetScenes, 
			plugin=self.plugin
		)
		ssheetPath = os.path.join(
			self.pluginDirectory,
			"UserInterfaces",
			"FusionStyleSheet"
		)
		self.core.registerStyleSheet(ssheetPath)

		self.core.registerCallback(
			"getIconPathForFileType", self.getIconPathForFileType, plugin=self
			)
		

	@err_catcher(name=__name__)
	def userSettings_loadUI(self, origin, tab):
		origin.gb_bldInstallDevTools = QGroupBox("Install Prism Developer Menu With Plugin")
		lo_bldAutoSave = QVBoxLayout()
		origin.gb_bldInstallDevTools.setLayout(lo_bldAutoSave)
		origin.gb_bldInstallDevTools.setCheckable(True)
		origin.gb_bldInstallDevTools.setChecked(False)

		tab.layout().addWidget(origin.gb_bldInstallDevTools)
		# origin.gb_bldAutoSave = QGroupBox("Auto save renderings")
		# lo_bldAutoSave = QVBoxLayout()
		# origin.gb_bldAutoSave.setLayout(lo_bldAutoSave)
		# origin.gb_bldAutoSave.setCheckable(True)
		# origin.gb_bldAutoSave.setChecked(False)

		# origin.chb_bldRperProject = QCheckBox("use path only for current project")

		# w_bldAutoSavePath = QWidget()
		# lo_bldAutoSavePath = QHBoxLayout()
		# origin.le_bldAutoSavePath = QLineEdit()
		# b_bldAutoSavePath = QPushButton("...")

		# lo_bldAutoSavePath.setContentsMargins(0, 0, 0, 0)
		# b_bldAutoSavePath.setMinimumSize(40, 0)
		# b_bldAutoSavePath.setMaximumSize(40, 1000)
		# b_bldAutoSavePath.setFocusPolicy(Qt.NoFocus)
		# b_bldAutoSavePath.setContextMenuPolicy(Qt.CustomContextMenu)
		# w_bldAutoSavePath.setLayout(lo_bldAutoSavePath)
		# lo_bldAutoSavePath.addWidget(origin.le_bldAutoSavePath)
		# lo_bldAutoSavePath.addWidget(b_bldAutoSavePath)

		# lo_bldAutoSave.addWidget(origin.chb_bldRperProject)
		# lo_bldAutoSave.addWidget(w_bldAutoSavePath)
		# tab.layout().addWidget(origin.gb_bldAutoSave)

		# if hasattr(self.core, "projectPath") and self.core.projectPath is not None:
		# 	origin.le_bldAutoSavePath.setText(self.core.projectPath)

		# b_bldAutoSavePath.clicked.connect(
		# 	lambda: origin.browse(
		# 		windowTitle="Select render save path", uiEdit=origin.le_bldAutoSavePath
		# 	)
		# )
		# b_bldAutoSavePath.customContextMenuRequested.connect(
		# 	lambda: self.core.openFolder(origin.le_bldAutoSavePath.text())
		# )
	
	@err_catcher(name=__name__)
	def userSettings_saveSettings(self, origin, settings):
		if "Fusion" not in settings:
			settings["Fusion"] = {}

		bsPath = self.core.fixPath(origin.le_bldAutoSavePath.text())
		if not bsPath.endswith(os.sep):
			bsPath += os.sep

		if origin.chb_bldRperProject.isChecked():
			if os.path.exists(self.core.prismIni):
				k = "autosavepath_%s" % self.core.projectName
				settings["Fusion"][k] = bsPath
		else:
			settings["Fusion"]["autosavepath"] = bsPath

		settings["Fusion"]["autosaverender"] = origin.gb_bldAutoSave.isChecked()
		settings["Fusion"][
			"autosaveperproject"
		] = origin.chb_bldRperProject.isChecked()

	@err_catcher(name=__name__)
	def userSettings_loadSettings(self, origin, settings):
		if "Fusion" in settings:
			if "autosaverender" in settings["Fusion"]:
				origin.gb_bldAutoSave.setChecked(settings["Fusion"]["autosaverender"])

			if "autosaveperproject" in settings["Fusion"]:
				origin.chb_bldRperProject.setChecked(
					settings["Fusion"]["autosaveperproject"]
				)

			pData = "autosavepath_%s" % getattr(self.core, "projectName", "")
			if pData in settings["Fusion"]:
				if origin.chb_bldRperProject.isChecked():
					origin.le_bldAutoSavePath.setText(settings["Fusion"][pData])

			if "autosavepath" in settings["Fusion"]:
				if not origin.chb_bldRperProject.isChecked():
					origin.le_bldAutoSavePath.setText(
						settings["Fusion"]["autosavepath"]
					)

	@err_catcher(name=__name__)
	def getPresetScenes(self, presetScenes):
		presetDir = os.path.join(self.pluginDirectory, "Presets")
		scenes = self.core.entities.getPresetScenesFromFolder(presetDir)
		presetScenes += scenes
		
	@err_catcher(name=__name__)
	def getAutobackPath(self, origin):
		autobackpath = ""
		if platform.system() == "Windows":
			autobackpath = os.path.join(
				self.core.getWindowsDocumentsPath(), "Fusion"
			)

		fileStr = "Fusion Scene File ("
		for i in self.sceneFormats:
			fileStr += "*%s " % i

		fileStr += ")"

		return autobackpath, fileStr
	

    #   Adds custom icon for Fusion auto-backup files
	@err_catcher(name=__name__)
	def getIconPathForFileType(self, extension):
		if extension == ".autocomp":
			icon = os.path.join(self.pluginDirectory, "UserInterfaces", "Fusion-Autosave.ico")
			return icon

		return None


	@err_catcher(name=__name__)
	def copySceneFile(self, origin, origFile, targetPath, mode="copy"):
		pass
