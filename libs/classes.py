import os
debugMode = os.path.isfile('debug' or 'DEBUG')
import time
import yaml
import ctypes
import asyncio
import subprocess

from libs.consts import paths as p
from libs.consts import consts as c

from colorama import init as colorama_init
colorama_init()
from colorama import Fore as fg
from colorama import Style as st
########################################################################################

#=======================================================================================
#                            .d888 
#                           d88P"  
#                           888    
#  .d8888b .d88b.  88888b.  888888 
# d88P"   d88""88b 888 "88b 888    
# 888     888  888 888  888 888    
# Y88b.   Y88..88P 888  888 888    
#  "Y8888P "Y88P"  888  888 888  
class conf():
	def load(category = False) -> object:
		"""
		Loads config from a `.yaml` file.
		### Input:
		> @category: `string`, optional &rarr; lets you choose a section of settings from the `.yaml` file instead of loading all of it.
		---
		### Returns:
		> **Any** &rarr; a full `.yaml` config or only a part of it if `category` was provided.
		"""
		if category:
			with open(p.CONFIG, 'r') as config:
				full = yaml.safe_load(config)
				return full[category]
		else:
			with open(p.CONFIG, 'r') as config:
				return yaml.safe_load(config)
	#//

	def filter(category, filter) -> list[ dict[str, str|bool] ]:
		"""
		Loads a section of a `.yaml` config file and filters it by property/value.\n
		For example filtering a @category `app` by property `enabled` will output a `dict`\n
		that only contains elements from category `app` where `enabled` property has a value of `True`.
		### Input:
		> @category: `string` &rarr; chooses a section of settings from the yaml file to filter on.
		> @filter: `string` &rarr; sets a property for filtering. Checks for existence, so "`property: False`" will be skipped, but "`property: True`", and "`property: "Some text.`" will be collected by the filter.
		---
		### Returns:
		> **list** &rarr; List of key/value pairs from the `.yaml` config file for which the filter returns `True`.
		"""
		config = conf.load(category)
		filtered = list(())
		for i in config:
			if i[filter]:
				filtered.append(i)
		return filtered
	#//
#//
#=======================================================================================



#=======================================================================================
#      888          888                        
#      888          888                        
#      888          888                        
#  .d88888  .d88b.  88888b.  888  888  .d88b.  
# d88" 888 d8P  Y8b 888 "88b 888  888 d88P"88b 
# 888  888 88888888 888  888 888  888 888  888 
# Y88b 888 Y8b.     888 d88P Y88b 888 Y88b 888 
#  "Y88888  "Y8888  88888P"   "Y88888  "Y88888 
#                                          888 
#                                     Y8b d88P 
#                                      "Y88P"  
class debug():
	def alert(text, title = "Attention", style = "0") -> object | None:
		"""
		### Input:
		> @text: `string` \n
		> @title: `string`, defaults to "Attention" \n
		> @style: `string`, defaults to `0` &rarr; choose style from `0` to `6` for window styles: \n
			0 : OK
			1 : OK 	| Cancel
			2 : Abort 	| Retry 	| Ignore
			3 : Yes 	| No 		| Cancel
			4 : Yes 	| No
			5 : Retry 	| Cancel
			6 : Cancel 	| Try Again	| Continue
		---
		### Returns:
		> a MsgBox similar to the one in AutoHotkey.
		"""
		if debugMode:
			return ctypes.windll.user32.MessageBoxW(0, text, title, style)
	#//

	
	def pause(text = False, breathe = False) -> None:
		"""
		Pauses execution until `ENTER` is pressed.
		### Input:
		> @text: `string` &rarr; Additional text you want printed before the pause.\n
		> @breathe: `boolean`, defaults to `False` &rarr; Controls whether there will be empty lines surrounding the @text.
		"""
		if debugMode:
			if breathe:
				print('')
			if text:
				print(f"{fg.LIGHTRED_EX}[ PAUSE -> {fg.LIGHTBLACK_EX}{time.strftime("%H:%M:%S", time.localtime())}{fg.LIGHTRED_EX} ]{fg.LIGHTBLACK_EX}::    {st.RESET_ALL}{text}")
			input(f"{fg.LIGHTRED_EX}[ PAUSE -> {fg.LIGHTBLACK_EX}{time.strftime("%H:%M:%S", time.localtime())}{fg.LIGHTRED_EX} ]{fg.LIGHTBLACK_EX}::    {st.RESET_ALL}////////////// Press {fg.YELLOW}<{fg.LIGHTRED_EX}{st.BRIGHT}ENTER{st.RESET_ALL}{fg.YELLOW}>{st.RESET_ALL} to continue...")
			if breathe:
				print('')
	#//
#//
#=======================================================================================



#=======================================================================================
#          888    d8b 888          
#          888    Y8P 888          
#          888        888          
# 888  888 888888 888 888 .d8888b  
# 888  888 888    888 888 88K      
# 888  888 888    888 888 "Y8888b. 
# Y88b 888 Y88b.  888 888      X88 
#  "Y88888  "Y888 888 888  88888P' 
class utils():
	def uprint(args, printType = False) -> None:
		"""
        Prints formatted messages to the console based on `printType`.
        ### Input:
        > @args: `Any` &rarr; The message or object to print. \n
        > @printType: `string` (optional) &rarr; Determines the type of message to print: \n
            `Any` : General message (green). \n
            debug : Debug message (cyan), only prints if `debugMode` is enabled. \n
            warn : Warning message (yellow). \n
            info : Info message (light magenta).
        """
		match printType:
			case 'debug':
				if debugMode:
					print(f"{fg.CYAN}[ DEBUG -> {fg.LIGHTBLACK_EX}{time.strftime("%H:%M:%S", time.localtime())}{fg.CYAN} ]{fg.LIGHTBLACK_EX}::    {st.RESET_ALL}", end='')
					print(args)
			case 'warn':
				print(f"{fg.YELLOW}[  WARN -> {fg.LIGHTBLACK_EX}{time.strftime("%H:%M:%S", time.localtime())}{fg.YELLOW} ]{fg.LIGHTBLACK_EX}::    {st.RESET_ALL}", end='')
				print(args)
			case 'info':
				print(f"{fg.LIGHTMAGENTA_EX}[  INFO -> {fg.LIGHTBLACK_EX}{time.strftime("%H:%M:%S", time.localtime())}{fg.LIGHTMAGENTA_EX} ]{fg.LIGHTBLACK_EX}::    {st.RESET_ALL}", end='')
				print(args)
			case 'error':
				print(f"{fg.LIGHTRED_EX}[ ERROR -> {fg.LIGHTBLACK_EX}{time.strftime("%H:%M:%S", time.localtime())}{fg.LIGHTRED_EX} ]{fg.LIGHTBLACK_EX}::    {st.RESET_ALL}", end='')
				print(args)
			case _:
				print(f"{fg.GREEN}[ {fg.LIGHTBLACK_EX}{time.strftime("%H:%M:%S", time.localtime())}{fg.GREEN} ]{fg.LIGHTBLACK_EX}::    {st.RESET_ALL}", end='')
				print(args)
	#//
#//
#=======================================================================================



#=======================================================================================
#  8888b.  88888b.  88888b.  
#     "88b 888 "88b 888 "88b 
# .d888888 888  888 888  888 
# 888  888 888 d88P 888 d88P 
# "Y888888 88888P"  88888P"  
#          888      888      
#          888      888      
#          888      888      
class app():
	async def run(inputVar)-> dict[str, str]:
		"""
		Runs an app.
		### Input:
		> @inputVar: App object &rarr; `{ "name": "App Name", "path": "C:\\path\\to\\app.exe", ... }`
		---
		### Returns:
		> **dict** &rarr; `{ "name": "App Name" }`
		"""
		subprocess.Popen(inputVar['path'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
		return {"name": inputVar['name']}
	#//

	def check(inputVar) -> list[ dict[str, str|bool] ]:
		"""
		Checks if an app is running.
		### Input:
		> @inputVar: App object &rarr; `{ "name": "App Name", "path": "C:\\path\\to\\app.exe", ... }`
		---
		### Returns:
		> **dict** &rarr; `{ "name": "#n App Name", "status": True | False }`
		"""
		if isinstance(inputVar, dict):
			fullInput = inputVar
			process = inputVar['path'].split('\\')[-1]
		elif isinstance(inputVar, str):
			process = str(inputVar)
			if process.endswith('.exe'):
				fullInput = {'name': process.split('.')[0]}

		command = 'tasklist /FI "IMAGENAME eq ' + process + '"'
		tasklist = str(subprocess.check_output(command))
		if process in tasklist:
			result = {"name": fullInput['name'], "status": True}
			utils.uprint(result, 'debug')
			return result['status']
		else:
			result = {"name": fullInput['name'], "status": False}
			utils.uprint(result, 'debug')
			return result['status']
	#//

	def kill(inputVar) -> None:
		"""
		Terminates an app. Checks config whether the app needs to be forced to close.
		### Input:
		> @inputVar: App object &rarr; `{ "name": "App Name", "path": "C:\\path\\to\\app.exe" ... }`
		---
		### Returns:
		> StdOut of `taskkill` command.
		"""
		if inputVar['forceKill']:
			forceKill = "/F "
		else:
			forceKill = ""

		exe = str(inputVar['path']).split('\\')[-1]
		catchOutput = subprocess.call("taskkill " + forceKill + "/IM " + exe, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
		utils.uprint(f"{exe}"+" stopped." if catchOutput == 0 else "", 'debug')
	#//

	def checkAll(inputVar) -> list[ dict[str, bool] ]:
		"""
		Checks all apps found in `config.yaml` whether they are currently running.
		### Input:
		> @inputVar: App[**s**] object &rarr; `[ { "name": "#n App Name", "path": "C:\\path\\to\\app.exe" } ... ]`
		---
		### Returns:
		> **list of *inputVar*** &rarr; `[ { "name": "#n App Name", "status": True | False } ... ]`
		"""
		checkedApps = list(())
		tasklist = str(subprocess.check_output('tasklist'))
		for i in inputVar:
			process = i['path'].split('\\')[-1]
			if process in tasklist:
				checkedApps.append({"name": i['name'], "status": True})
			else:
				checkedApps.append({"name": i['name'], "status": False})
		utils.uprint(checkedApps, 'debug')
		return checkedApps
	#//
#//
#=======================================================================================



#=======================================================================================
#  .d88b.   8888b.  88888b.d88b.   .d88b.  
# d88P"88b     "88b 888 "888 "88b d8P  Y8b 
# 888  888 .d888888 888  888  888 88888888 
# Y88b 888 888  888 888  888  888 Y8b.     
#  "Y88888 "Y888888 888  888  888  "Y8888  
#      888                                 
# Y8b d88P                                 
#  "Y88P"                                  
class game():
	def checkVr() -> bool:
		"""
		Checks if VR is currently running.
		### Returns:
		> **Boolean**
		"""
		process = 'vrmonitor.exe'
		command = 'tasklist /FI "IMAGENAME eq ' + process + '"'
		tasklist = str(subprocess.check_output(command))
		if process in tasklist:
			utils.uprint("VR is running.", 'debug')
			return True
		else:
			utils.uprint("VR is NOT running.", 'debug')
			return False
	#//

	async def oculusASWoff(oculusCLIpath) -> None:
		"""
		***ASYNCHRONOUS, REMEMBER TO AWAIT()*** \n
		Turns off Oculus ASW using the `OculusDebugToolCLI.exe`.
		### Inputs:
		> @oculusCLIpath: `string` &rarr; Full path to the `OculusDebugToolCLI.exe`.
		"""
		if os.path.isfile(p.OCULUS_ASW):
			os.remove(p.OCULUS_ASW)
		with open(p.OCULUS_ASW, 'w') as file:
			file.write(
				'server:asw.off \n' \
				'exit'
			)
		cliString = f'powershell timeout 10 /nobreak; & \"{oculusCLIpath}\" -f \"{p.OCULUS_ASW}\"'
		subprocess.Popen(cliString)
	#//

	def setup(vrStatus) -> None:
		"""
		Sets up some things before launching Elite Dangerous.
		### Input:
		> @vrStatus: `Boolean` &rarr; Can receive input from `game.checkVr()`.
		"""
		if conf.load('settings')['vrCompatible']:
			vrConf = conf.load('vrSettings')
			vrStatus = game.checkVr()
			if vrStatus:
				# Check if user wants to turn off Oculus ASW (it tends to absolutely s**t itself on loading screens in ED if you stream the game through SteamVR)
				if vrConf['oculusASWoff']:
					asyncio.run(game.oculusASWoff(vrConf['oculusCLIpath']))

			# Check if user wants to change video settings for ED for VR / Non-VR
			if vrConf['edOptionsFolderCopy']:
				# If VR is running
				if vrStatus:
					subprocess.Popen(f'robocopy \"{p.ED_OPTIONS_BACKUP}\\vr-ed-options\" \"{vrConf['edOptionsFolderPath']}\" \"*\" /NFL /NDL /NJH /NJS /nc /ns /np /IS /IT /IM')
				# If VR is not running (desktop mode)
				else:
					subprocess.Popen(f"robocopy \"{p.paths.ED_OPTIONS_BACKUP}\\nonvr-ed-options\" \"{vrConf['edOptionsFolderPath']}\" \"*\" /NFL /NDL /NJH /NJS /nc /ns /np /IS /IT /IM")
	#//

	async def launch(vrStatus) -> bool:
		"""
		Launches Elite Dangerous normally or in VR, depending on `vrStatus`.
		### Input:
		> @vrStatus: `Boolean` &rarr; Can receive input from `game.checkVr()`.
		---
		### Returns:
		> **Boolean** &rarr; `True` if Elite launched in VR, `False` if in desktop mode.
		"""
		if vrStatus:
			subprocess.Popen('start steam://launch/359320/vr', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
			launchedVr = True
		else:
			subprocess.Popen('start steam://rungameid/359320', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
			launchedVr = False
		return launchedVr
	#//

	def awaitGameStart(gameExe) -> dict[str, bool]:
		"""
		Waits for Elite to start.
		### Input:
		> @gameExe: `string` &rarr; Name of the Elite Dangerous executable.
		---
		### Returns:
		> **dict** &rarr; `{"gameStarted": True | False}`
		"""
		timeout = conf.load('settings')['gameStartTimeout']
		utils.uprint('Trying to launch the game...')
		i = 1
		while not app.check(gameExe):
			if i == timeout:
				print("\r                                     ")
				utils.uprint("Game took too long to respond - closing.", 'error')
				return {"gameStarted": False}
			else:
				countdown = timeout-i
				print(f"\rAwaiting game start for {countdown} seconds... ", end='')
				i += 1
				utils.uprint(i, 'debug')
				time.sleep(1)
		if not i == timeout:
			utils.uprint("Game started!")
			if conf.load('settings')['vrCompatible']:
				vrConf = conf.load('vrSettings')
				vrStatus = game.checkVr()
				if vrStatus:
					if vrConf['oculusASWoff']:
						asyncio.run(game.oculusASWoff(vrConf['oculusCLIpath']))
			return {"gameStarted": True}
	#//

	def awaitGameEnd(gameExe) -> dict[str, bool]:
		"""
		Waits for Elite to close.
		### Input:
		> @gameExe: `string` &rarr; Name of the Elite Dangerous executable.
		---
		### Returns:
		> **dict** &rarr; `{"gameStopped": True}`
		"""
		if app.check(gameExe):
			utils.uprint("Awaiting game close...")
			while app.check(gameExe):
				time.sleep(1)
			utils.uprint("Game closed.")
			return {"gameStopped": True}
		return {"gameStopped": False}
	#//
#//
#=======================================================================================
